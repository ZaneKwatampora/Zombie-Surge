import pygame
from src.sound import sound_manager

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.animations = {
            "idle": (pygame.image.load('assets/images/player/player_idle/SteamMan_idle.png').convert_alpha(), 48, 48, 4),
            "walk": (pygame.image.load('assets/images/player/player_run/SteamMan_walk.png').convert_alpha(), 48, 48, 6),
            "run": (pygame.image.load('assets/images/player/player_run/SteamMan_run.png').convert_alpha(), 48, 48, 6),
            "hurt": (pygame.image.load('assets/images/player/player_hurt/SteamMan_hurt.png').convert_alpha(), 48, 48, 3),
            "die": (pygame.image.load('assets/images/player/player_death/SteamMan_death.png').convert_alpha(), 48, 48, 6),
            "attack": (pygame.image.load('assets/images/player/player_attack/SteamMan_attack1.png').convert_alpha(), 48, 48, 6),
        }

        self.state = "idle"
        self.sprite_sheet, self.frame_width, self.frame_height, self.num_frames = self.animations[self.state]

        self.frames = []
        self.load_frames()

        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))
        self.facing_right = True

        self.base_speed = 4
        self.speed_bonus = 0
        self.animation_timer = 0
        self.animation_cooldown = 150

        self.is_hurt = False
        self.is_dead = False
        self.is_attacking = False
        self.death_animation_done = False
        self.ready_to_level_up = False

        self.hurt_timer = 0
        self.hurt_cooldown = 600
        self.attack_cooldown = 1000
        self.attack_timer = 0
        self.attack_damage = 10 

        self.health = 100
        self.max_health = 100
        self.exp = 0
        self.level = 1
        self.exp_to_next = 100


        self.current_movement_sound = None

    def load_frames(self):
        self.frames = []
        for frame_index in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(frame_index * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            self.frames.append(pygame.transform.scale(frame, (self.frame_width * 1.2, self.frame_height * 1.2)))

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.sprite_sheet, self.frame_width, self.frame_height, self.num_frames = self.animations[self.state]
            self.load_frames()
            self.current_frame = 0
            self.animation_timer = 0

    def move(self, keys):
        moving = False

        shift_multiplier = 2 if keys[pygame.K_LSHIFT] else 1
        current_speed = (self.base_speed + self.speed_bonus) * shift_multiplier

        if keys[pygame.K_w]:
            self.rect.y -= current_speed
            moving = True
        if keys[pygame.K_s]:
            self.rect.y += current_speed
            moving = True
        if keys[pygame.K_a]:
            self.rect.x -= current_speed
            self.facing_right = False
            moving = True
        if keys[pygame.K_d]:
            self.rect.x += current_speed
            self.facing_right = True
            moving = True

        return moving

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_cooldown:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % self.num_frames
            self.image = self.frames[self.current_frame]

            if self.is_dead and self.state == "die" and self.current_frame == self.num_frames - 1:
                self.death_animation_done = True

    def attack(self):
        if not self.is_dead and not self.is_attacking:
            self.is_attacking = True
            self.attack_timer = 0
            self.set_state("attack")
            sound_manager.play_sound("player_attack", volume=0.3)

    def take_damage(self, amount):
        if not self.is_dead and not self.is_hurt:
            self.health -= amount
            if self.health <= 0:
                self.health = 0
                self.is_dead = True
                self.set_state("die")
            else:
                self.is_hurt = True
                self.hurt_timer = 0
                self.set_state("hurt")

    def handle_movement_sound(self, sound_name):
        if self.current_movement_sound != sound_name:
            self.stop_movement_sound()
            sound_manager.play_sound(sound_name, volume=0.5, loop=True)
            self.current_movement_sound = sound_name

    def stop_movement_sound(self):
        if self.current_movement_sound:
            sound_manager.stop_sound(self.current_movement_sound)
            self.current_movement_sound = None

    def gain_exp(self, amount):
        self.exp += amount
        if self.exp >= self.exp_to_next:
            self.level_up()
            
    def level_up(self):
        self.exp -= self.exp_to_next
        self.level += 1
        self.exp_to_next = int(self.exp_to_next * 1.5)
        sound_manager.play_sound("level_up", volume=0.4)
        self.ready_to_level_up = True

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if self.is_dead:
            self.set_state("die")
            self.stop_movement_sound()
        elif self.is_hurt:
            self.hurt_timer += dt
            if self.hurt_timer >= self.hurt_cooldown:
                self.is_hurt = False
        elif self.is_attacking:
            self.attack_timer += dt
            if self.attack_timer >= self.attack_cooldown:
                self.is_attacking = False
        else:
            moving = self.move(keys)
            if moving:
                if keys[pygame.K_LSHIFT]:
                    self.set_state("run")
                    self.handle_movement_sound('player_run')
                else:
                    self.set_state("walk")
                    self.handle_movement_sound('player_walk')
            else:
                self.set_state("idle")
                self.stop_movement_sound()

        self.animate(dt)

    def draw(self, surface):
        image_to_draw = self.image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        surface.blit(image_to_draw, self.rect)
        self.draw_health_bar(surface)

    def draw_health_bar(self, surface):
        bar_width = 60
        bar_height = 8
        health_ratio = self.health / self.max_health

        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.top - 15

        # health
        pygame.draw.rect(surface, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(surface, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))

        # experience
        exp_ratio = self.exp / self.exp_to_next
        exp_bar_y = bar_y + bar_height + 2
        pygame.draw.rect(surface, (50, 50, 50), (bar_x, exp_bar_y, bar_width, 4))
        pygame.draw.rect(surface, (0, 150, 255), (bar_x, exp_bar_y, bar_width * exp_ratio, 4))


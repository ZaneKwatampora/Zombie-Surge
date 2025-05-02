import pygame
from src.sound import sound_manager

class Zombie(pygame.sprite.Sprite):
    def __init__(self, x, y, target):
        super().__init__()
        
        self.target = target
        self.state = None
        self.health = 100
        self.max_health = 100
        self.speed = 0.8
        self.attack_range = 30
        self.attacking = False
        self.is_dead = False
        self.death_animation_done = False
        self.damage = 5
        self.animation_timer = 0
        self.animation_cooldown = 150
        self.facing_right = True

        self.animations = {
            'idle': (pygame.image.load("assets/images/zombie/zombie_idle/Idle.png").convert_alpha(), 96, 96, 8),
            'walk': (pygame.image.load("assets/images/zombie/zombie_run/Walk.png").convert_alpha(), 96, 96, 8),
            'attack': (pygame.image.load("assets/images/zombie/zombie_attack/Attack_1.png").convert_alpha(), 96, 96, 5),
            'dead': (pygame.image.load("assets/images/zombie/zombie_death/Dead.png").convert_alpha(), 96, 96, 5),
        }

        self.frames = []
        self.current_frame = 0

        self.set_state('walk')

        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))

    def set_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.sprite_sheet, self.frame_width, self.frame_height, self.num_frames = self.animations[self.state]
            self.load_frames()
            self.current_frame = 0
            self.animation_timer = 0

    def load_frames(self):
        self.frames = []
        for frame_index in range(self.num_frames):
            frame = self.sprite_sheet.subsurface(
                pygame.Rect(frame_index * self.frame_width, 0, self.frame_width, self.frame_height)
            )
            scaled_frame = pygame.transform.scale(frame, (int(self.frame_width * 0.7), int(self.frame_height * 0.7)))
            self.frames.append(scaled_frame)

    def update(self, dt):
        if self.is_dead:
            self.set_state('dead')
        else:
            distance = self.rect.centerx - self.target.rect.centerx, self.rect.centery - self.target.rect.centery
            distance_sq = distance[0]**2 + distance[1]**2

            if distance_sq <= self.attack_range**2:
                self.set_state('attack')
                self.attacking = True
            else:
                self.set_state('walk')
                self.attacking = False
                direction = pygame.Vector2(self.target.rect.center) - pygame.Vector2(self.rect.center)
                if direction.length() > 0:
                    direction = direction.normalize()
                    self.rect.centerx += direction.x * self.speed
                    self.rect.centery += direction.y * self.speed

            if self.target.rect.centerx < self.rect.centerx:
                self.facing_right = False
            else:
                self.facing_right = True

        self.animate(dt)

    def animate(self, dt):
        self.animation_timer += dt
        if self.animation_timer >= self.animation_cooldown:
            self.animation_timer = 0
            self.current_frame += 1

            if self.current_frame >= len(self.frames):
                if self.state == 'dead':
                    self.death_animation_done = True
                    self.current_frame = len(self.frames) - 1
                else:
                    self.current_frame = 0

                    if self.attacking and not self.is_dead:
                        self.target.take_damage(self.damage)
                        sound_manager.play_sound('zombie_attack', volume=0.3)

            self.image = self.frames[self.current_frame]
            
            if not self.facing_right:
                self.image = pygame.transform.flip(self.frames[self.current_frame], True, False)
            else:
                self.image = self.frames[self.current_frame]

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def take_damage(self, amount):
        if not self.is_dead:
            self.health -= amount
            if self.health <= 0:
                self.is_dead = True
                sound_manager.play_sound('zombie_die', volume=0.3)

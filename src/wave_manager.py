import pygame
from sound import sound_manager
from zombie.zombie import Zombie
import random  
from settings import WIDTH, HEIGHT
from exp import ExpOrb

class WaveManager:
    def __init__(self, player):
        self.player = player
        self.round_num = 1
        self.enemies = pygame.sprite.Group()
        self.preparation_time = 0
        self.wave_complete = False
        self.exp_orbs = pygame.sprite.Group()

    def start_round(self):
        zombie_count = 3 + (self.round_num - 1) * 5
        self.enemies.empty()

        for i in range(zombie_count):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            zombie = Zombie(x, y, self.player)

            zombie.speed += 0.3 * self.round_num
            zombie.health += 100 * self.round_num
            zombie.damage += 10 * self.round_num
            self.enemies.add(zombie)

        print(f"Round {self.round_num}: {len(self.enemies)} zombies spawned")

        sound_manager.play_sound("round_start", volume=0.7)
        self.preparation_time = 0

    def update(self, dt):
        if not self.player.is_dead:
            if len(self.enemies) == 0:
                if not self.wave_complete:
                    self.wave_complete = True
                    self.preparation_time = 10

            if self.wave_complete:
                self.preparation_time -= dt / 1000
                if self.preparation_time <= 0:
                    self.round_num += 1
                    self.start_round()
                    self.wave_complete = False

        for enemy in list(self.enemies):
            enemy.update(dt)
            if enemy.is_dead and enemy.death_animation_done:
                orb = ExpOrb(enemy.rect.centerx, enemy.rect.centery)
                self.exp_orbs.add(orb)
                self.enemies.remove(enemy)

        if self.player.is_attacking:
            for enemy in self.enemies:
                if self.player.rect.colliderect(enemy.rect.inflate(2, 2)):
                    enemy.take_damage(10)
        
        self.exp_orbs.update(self.player)

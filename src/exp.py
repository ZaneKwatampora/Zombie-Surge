import pygame
from sound import sound_manager

class ExpOrb(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        original_image = pygame.image.load('assets/images/exp_orb.png').convert_alpha()
        self.image = pygame.transform.smoothscale(original_image, (16, 16))
        self.rect = self.image.get_rect(center=(x, y))
        self.exp_value = 10

    def update(self, player):
        if self.rect.colliderect(player.rect):
            player.gain_exp(self.exp_value)
            sound_manager.sounds["exp_pickup"].set_volume(0.6)
            sound_manager.sounds["exp_pickup"].play()
            self.kill()
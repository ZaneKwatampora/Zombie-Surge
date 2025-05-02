import pygame

class LevelUp:
    def __init__(self, screen, player):
        self.screen = screen
        self.player = player
        self.base_images = {
            'damage': pygame.image.load('assets/images/upgrade_cards/Damage-upgrade.png').convert_alpha(),
            'health': pygame.image.load('assets/images/upgrade_cards/Health.png').convert_alpha(),
            'speed': pygame.image.load('assets/images/upgrade_cards/Speed.png').convert_alpha(),
        }
        self.card_data = {}
        self.visible = False

        screen_width, screen_height = self.screen.get_size()
        spacing = 50
        self.card_size = (200, 290)  # Increased size
        total_width = len(self.base_images) * self.card_size[0] + (len(self.base_images) - 1) * spacing
        start_x = (screen_width - total_width) // 2

        for i, (key, img) in enumerate(self.base_images.items()):
            scaled_img = pygame.transform.scale(img, self.card_size)
            x = start_x + i * (self.card_size[0] + spacing)
            y = screen_height // 2 - self.card_size[1] // 2
            rect = scaled_img.get_rect(topleft=(x, y))
            self.card_data[key] = {
                'image': scaled_img,
                'rect': rect,
                'hovered': False
            }

    def draw(self):
        if self.visible:
            overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            mouse_pos = pygame.mouse.get_pos()
            for name, data in self.card_data.items():
                rect = data['rect']
                if rect.collidepoint(mouse_pos):
                    data['hovered'] = True
                    enlarged_size = (int(self.card_size[0] * 1.15), int(self.card_size[1] * 1.15))
                    enlarged = pygame.transform.scale(data['image'], enlarged_size)
                    enlarged_rect = enlarged.get_rect(center=rect.center)
                    self.screen.blit(enlarged, enlarged_rect)
                    pygame.draw.rect(self.screen, (255, 255, 0), enlarged_rect, 3)
                else:
                    data['hovered'] = False
                    self.screen.blit(data['image'], rect)
                    pygame.draw.rect(self.screen, (200, 200, 200), rect, 2)

    def handle_event(self, event):
        if not self.visible:
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            for name, data in self.card_data.items():
                if data['rect'].collidepoint(event.pos):
                    self.apply_upgrade(name)
                    self.visible = False
                    self.player.ready_to_level_up = False

    def apply_upgrade(self, name):
        print(f"Applying upgrade: {name}")
        if name == 'damage':
            self.player.attack_damage += 5
        elif name == 'health':
            self.player.max_health += 20
            self.player.health = self.player.max_health
        elif name == 'speed':
            self.player.speed_bonus += 0.5
        print(f"New stats - Damage: {self.player.attack_damage}, Health: {self.player.health}, Speed: {self.player.base_speed + self.player.speed_bonus}")

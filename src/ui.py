import pygame

class UIManager:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def draw_game_over(self):
        overlay = pygame.Surface(self.screen.get_size())
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        restart_text = self.small_font.render("Press R to Restart", True, (255, 255, 255))
        exit_text = self.small_font.render("Press E to Exit", True, (255, 255, 255))

        screen_center = self.screen.get_rect().center
        self.screen.blit(game_over_text, (screen_center[0] - game_over_text.get_width() // 2, screen_center[1] - 50))
        self.screen.blit(restart_text, (screen_center[0] - restart_text.get_width() // 2, screen_center[1] + 20))
        self.screen.blit(exit_text, (screen_center[0] - exit_text.get_width() // 2, screen_center[1] + 60))

    def draw_wave_info(self, round_num, preparation_time):
        wave_text = self.small_font.render(f"Round {round_num}", True, (255, 255, 255))
        self.screen.blit(wave_text, (10, 10))

        if preparation_time > 0:
            prep_text = self.small_font.render(f"Next wave in {int(preparation_time)}s", True, (255, 255, 255))
            self.screen.blit(prep_text, (10, 40))

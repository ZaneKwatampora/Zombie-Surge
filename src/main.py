import pygame
import sys
from settings import WIDTH, HEIGHT, FPS, BACKGROUND_COLOR
from player.player import Player
from zombie.zombie import Zombie
from sound import sound_manager
from ui import UIManager
from wave_manager import WaveManager

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Zombie Surge")
    clock = pygame.time.Clock()

    sound_manager.play_background_music(
        "assets/sounds/forest-atmosphere-localization-poland-320813.mp3",
        volume=0.1,
        loop=-1
    )

    player = Player(WIDTH // 2, HEIGHT // 2)
    ui_manager = UIManager(screen)
    wave_manager = WaveManager(player)
    wave_manager.start_round()

    running = True
    game_over = False

    while running:
        dt = clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_SPACE:
                        player.attack()

                if game_over:
                    if event.key == pygame.K_r:
                        main()
                        return
                    elif event.key == pygame.K_e:
                        running = False

        screen.fill(BACKGROUND_COLOR)

        if not game_over:
            player.update(dt)
            wave_manager.update(dt)
            wave_manager.enemies.draw(screen)
            player.draw(screen)

            ui_manager.draw_wave_info(wave_manager.round_num, wave_manager.preparation_time)

            if player.is_dead and player.death_animation_done:
                game_over = True
                sound_manager.stop_background_music()
        else:
            ui_manager.draw_game_over()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

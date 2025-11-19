"""
Application entry: main menu, navigation to game and leaderboard.
"""

import pygame
from ui import draw_text
from leaderboard import show_leaderboard
from game import game_loop
from config import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT, WINDOW_TITLE


def main_menu() -> None:
    """
    Show the main menu and route to game or leaderboard.
    """
    pygame.init()
    screen = pygame.display.set_mode(DISPLAY)
    pygame.display.set_caption(WINDOW_TITLE)

    is_running = True
    while is_running:
        screen.fill((0, 0, 0))
        draw_text(screen, "3D Cube Stacking Game",
                  (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//4-50,
                   SCREEN_WIDTH//2+250, SCREEN_HEIGHT//4),
                  size=42, align="center")
        draw_text(screen, "Press SPACE to start",
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-50,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//2),
                  size=32, align="center")
        draw_text(screen, "Press L to view local leaderboard",
                  (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2,
                   SCREEN_WIDTH//2+250, SCREEN_HEIGHT//2+50),
                  size=28, align="center")
        draw_text(screen, "Press ESC to quit",
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2+75,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//2+125),
                  size=28, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop(main_menu_callback=main_menu)
                elif event.key == pygame.K_l:
                    show_leaderboard()
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

        pygame.display.flip()


if __name__ == "__main__":
    main_menu()

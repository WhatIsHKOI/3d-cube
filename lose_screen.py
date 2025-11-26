"""
Lose screen handling.
"""

import pygame
from ui import draw_text
from config import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT


def lose_screen(score: int, restart_callback, menu_callback):
    """
    Display the lose screen with options to restart or return to main menu.

    Parameters:
        score (int): Final score achieved before losing.
    """
    screen = pygame.display.set_mode(DISPLAY)
    is_running = True

    while is_running:
        screen.fill((0, 0, 0))
        draw_text(screen, "You Lose!", 
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//4-50,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//4),
                   size=42, align="center")
        draw_text(screen, f"Your Score: {score}", 
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2-50,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//2),
                   size=32, align="center")
        draw_text(screen, "Press SPACE to restart", 
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//2,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//2+50),
                   size=28, align="center")
        draw_text(screen, "Press ESC to return to main menu", 
                  (SCREEN_WIDTH//2-250, SCREEN_HEIGHT//2+75,
                   SCREEN_WIDTH//2+250, SCREEN_HEIGHT//2+125),
                   size=28, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    restart_callback(main_menu_callback=menu_callback)
                elif event.key == pygame.K_ESCAPE:
                    menu_callback()

        pygame.display.flip()

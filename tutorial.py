"""
Showing a tutorial screen for user.
"""

import pygame
from ui import draw_text
from config import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT

def show_tutorial(menu_callback) -> None:

    screen = pygame.display.set_mode(DISPLAY)
    is_running = True

    while is_running:
        screen.fill((0, 0, 0))
        draw_text(screen, "Stack the cubes as tall as you can.", 
                  (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//4-50,
                   SCREEN_WIDTH//2+400, SCREEN_HEIGHT//4),
                   size=42, align="center")
        draw_text(screen, f"Green cubes are normal cubes,", 
                  (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2-50,
                   SCREEN_WIDTH//2+400, SCREEN_HEIGHT//2),
                   size=28, align="center")
        draw_text(screen, "Red cubes occasionally change their speed,", 
                  (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2,
                   SCREEN_WIDTH//2+400, SCREEN_HEIGHT//2+50),
                   size=28, align="center")
        draw_text(screen, "Purple cubes occasionally teleports when moving.", 
                  (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2+50,
                   SCREEN_WIDTH//2+400, SCREEN_HEIGHT//2+100),
                   size=28, align="center")
        draw_text(screen, "Press space if you understand the rules.", 
                  (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2+125,
                   SCREEN_WIDTH//2+400, SCREEN_HEIGHT//2+175),
                   size=28, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    start_game_text = ["3", "2", "1", "START!"]
                    for round_text in start_game_text:
                        screen.fill((0, 0, 0))
                        draw_text(screen, round_text, 
                                (SCREEN_WIDTH//2-400, SCREEN_HEIGHT//2-50,
                                SCREEN_WIDTH//2+400, SCREEN_HEIGHT//2+50),
                                size=84, align="center")
                        pygame.display.flip()
                        pygame.time.wait(1000)
                    return
                elif event.key == pygame.K_ESCAPE:
                    menu_callback()
        
        pygame.display.flip()

    return
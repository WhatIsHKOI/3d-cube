"""
Leaderboard file I/O and display screen.
"""

import pygame
from typing import List
from ui import draw_text
from config import DISPLAY, SCREEN_WIDTH, SCREEN_HEIGHT, LEADERBOARD_FILE, MAX_DISPLAY_SCORES


def read_leaderboard(filename: str = LEADERBOARD_FILE) -> List[int]:
    """
    Read leaderboard scores from file.

    Parameters:
        filename (str): Path to leaderboard file.

    Returns:
        List[int]: List of scores (descending order assumed or enforced later).
    """
    scores = []
    try:
        with open(filename, "r") as f:
            count = int(f.readline().strip())
            for _ in range(count):
                line = f.readline()
                if not line:
                    break
                scores.append(int(line.strip()))
    except FileNotFoundError:
        # Initialize an empty file
        with open(filename, "w") as f:
            f.write("0\n")
    return scores


def write_leaderboard(scores: List[int], filename: str = LEADERBOARD_FILE) -> None:
    """
    Write leaderboard scores to file.

    Parameters:
        scores (List[int]): Scores to write (will be truncated/padded).
        filename (str): Path to leaderboard file.
    """
    scores = sorted(scores, reverse=True)
    with open(filename, "w") as f:
        f.write(str(max(MAX_DISPLAY_SCORES, len(scores))) + "\n")
        for i in range(max(MAX_DISPLAY_SCORES, len(scores))):
            s = scores[i] if i < len(scores) else 0
            f.write(str(s) + "\n")


def update_leaderboard(new_score: int, filename: str = LEADERBOARD_FILE) -> None:
    """
    Add a new score to leaderboard and persist it.

    Parameters:
        new_score (int): Player score to add.
        filename (str): Path to leaderboard file.
    """
    scores = read_leaderboard(filename)
    scores.append(new_score)
    write_leaderboard(scores, filename)


def show_leaderboard() -> None:
    """
    Display the local leaderboard screen.
    """
    screen = pygame.display.set_mode(DISPLAY)
    is_running = True

    while is_running:
        screen.fill((0, 0, 0))
        draw_text(screen, "Local Leaderboard",
                  (SCREEN_WIDTH//4-100, SCREEN_HEIGHT//4-50,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//4),
                  size=32, align="center")
        draw_text(screen, "Press ESC to return",
                  (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//4,
                   SCREEN_WIDTH//2+200, SCREEN_HEIGHT//4+50),
                  size=28, align="center")

        scores = read_leaderboard()
        for i, s in enumerate(sorted(scores, reverse=True)[:5], start=1):
            draw_text(screen, f"{i}. {s}",
                      (SCREEN_WIDTH//2-200, SCREEN_HEIGHT//4+i*50+50,
                       SCREEN_WIDTH//2+200, SCREEN_HEIGHT//4+i*50+100),
                      size=32, align="center")

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                is_running = False

        pygame.display.flip()

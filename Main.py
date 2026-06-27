import pygame
import os
import json
from screen.start import StartScreen
from screen.menu_level import LevelScreen
from screen.play import PlayScreen
from data.levels.Load_level import load_level

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "levels", "sudoku_board.json")) as f:
    sudoku_board = json.load(f)

SUDOKU_LEVEL = 3  # level nào có ô '@'

start_screen = StartScreen()
menu_level_screen = LevelScreen()
levels = [0,1,2,3,4,5,6]
for i in range(1, 4):
    lv, node = load_level(os.path.join(BASE_DIR, "data", "levels", f"level{i}.json"))
    board = sudoku_board if i == SUDOKU_LEVEL else None
    levels[i] = PlayScreen(lv, node, board_sudoku=board)
level = 0

# start
# menu level
# play
current_screen = "start"

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "start" :
                if start_screen.start_button.collidepoint(event.pos):
                    current_screen = "menu level"

            elif current_screen == "menu level":
                if menu_level_screen.back_button.collidepoint(event.pos):
                    current_screen = "start"

                for i, button in enumerate(menu_level_screen.level_buttons):
                    if button.collidepoint(event.pos):
                        level = i + 1
                        current_screen = "play"

        if current_screen == "play":
            result = levels[level].handle_event(event)
            if result == "start":          
                current_screen = "start"
            elif result == "menu level":
                current_screen = "menu level"
            elif result == "next_level":
                level = min(level + 1, len(levels) - 1)
                current_screen = "play"

    if current_screen == "start":
        start_screen.draw(screen)
    elif current_screen == "menu level":
        start_screen.draw(screen)
        menu_level_screen.draw(screen)
    elif current_screen == "play":
        levels[level].draw(screen)

    pygame.display.flip()

pygame.quit()
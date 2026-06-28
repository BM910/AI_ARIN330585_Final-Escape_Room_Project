import pygame
import os
import json
from screen.start import StartScreen
from screen.menu_level import LevelScreen
from screen.play import PlayScreen
from screen.and_or_solution import AndOrSolution   # thêm từ code hiện tại
from data.levels.Load_level import load_level

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()                         # thêm từ code hiện tại

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(BASE_DIR, "data", "levels", "sudoku_board.json")) as f:
    sudoku_board = json.load(f)
with open(os.path.join(BASE_DIR, "data", "levels", "connect_4_board.json")) as f:  # giữ lại từ GitHub
    connect4_board = json.load(f)

SUDOKU_LEVEL = 7
CONNECT_4_LEVEL = 8                                # giữ lại từ GitHub

start_screen = StartScreen()
menu_level_screen = LevelScreen()
levels = [0, 1, 2, 3, 4, 5, 6, 7 ,8]
for i in range(1, 9):
    lv, node = load_level(os.path.join(BASE_DIR, "data", "levels", f"level{i}.json"))
    s_board = sudoku_board if i == SUDOKU_LEVEL else None
    c_board = connect4_board if i == CONNECT_4_LEVEL else None  # giữ lại từ GitHub
    levels[i] = PlayScreen(lv, node, board_sudoku=s_board, board_connect4=c_board)  # giữ lại từ GitHub

level = 0
current_screen = "start"
and_or_screen = None                                # thêm từ code hiện tại

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # màn and_or xử lý event trước
        if current_screen == "and_or":
            result = and_or_screen.handle_event(event)
            if result == "play":
                current_screen = "play"
                and_or_screen = None
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "start":
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
            elif isinstance(result, tuple) and result[0] == "and_or":
                and_or_screen = AndOrSolution(result[1])
                current_screen = "and_or"

    # update auto-step khi nhấn Run
    if current_screen == "and_or" and and_or_screen:
        and_or_screen.update()

    # draw
    if current_screen == "start":
        start_screen.draw(screen)
    elif current_screen == "menu level":
        start_screen.draw(screen)
        menu_level_screen.draw(screen)
    elif current_screen == "play":
        levels[level].draw(screen)
    elif current_screen == "and_or":
        and_or_screen.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
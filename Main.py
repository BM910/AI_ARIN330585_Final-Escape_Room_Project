import pygame
from Screen.start import StartScreen
from Screen.menu_level import LevelScreen
from Screen.play import PlayScreen
from data.Node import Node


pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)

start_screen = StartScreen()
menu_level_screen = LevelScreen()
levels = [0,1,2,3,4,5,6]
for i in range(6):
    # Lấy node theo ...
    # node = Node(state, None, None, 0)
    levels[i+1] = PlayScreen(i)
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
                        level = i
                        current_screen = "play"

            elif current_screen == "play":
                result = levels[level].handle_event(event)

    if current_screen == "start":
        start_screen.draw(screen)
    elif current_screen == "menu level":
        start_screen.draw(screen)
        menu_level_screen.draw(screen)
    elif current_screen == "play":
        levels[level].draw(screen)

    pygame.display.flip()

pygame.quit()
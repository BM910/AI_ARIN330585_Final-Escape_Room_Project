import pygame
from StartScreen import StartScreen
from LevelScreen import LevelScreen
from PlayScreen import PlayScreen

pygame.init()

WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

start_screen = StartScreen()
level_screen = LevelScreen()
play_screen = PlayScreen()

current_screen = "start"

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            if current_screen == "start" :

                if start_screen.start_button.collidepoint(event.pos):
                    current_screen = "level"

            elif current_screen == "level":

                if level_screen.back_button.collidepoint(event.pos):
                    current_screen = "start"

                for i, button in enumerate(level_screen.level_buttons):
                    if button.collidepoint(event.pos):
                        print(f"Level {i+1}")

    if current_screen == "start":
        start_screen.draw(screen)

    if current_screen == "level":
        level_screen.draw(screen)

    if current_screen == "play":
        play_screen.draw(screen)

    pygame.display.flip()

pygame.quit()
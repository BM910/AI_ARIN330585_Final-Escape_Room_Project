import pygame

WIDTH, HEIGHT = 1000, 600

class StartScreen:
    def __init__(self):
        self.start_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50)

    def draw(self, screen):
        screen.fill((255, 255, 255))

        pygame.draw.rect(screen, (0, 128, 255), self.start_button)

        font = pygame.font.Font(None, 36)
        text = font.render("Start Game", True, (255, 255, 255))
        screen.blit(text, (WIDTH // 2 - 80, HEIGHT // 2 - 10))
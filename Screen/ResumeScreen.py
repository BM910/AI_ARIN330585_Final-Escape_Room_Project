import pygame

ROWS, COLS = 6, 6
CELL_SIZE = 50
WIDTH, HEIGHT = 1000, 600

class ResumeScreen:
    def __init__(self):
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

        self.rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 80, 200, 180)
        self.back_button = pygame.Rect(self.rect.left + 20, self.rect.top + 20, 60, 30)
        self.reset_button = pygame.Rect(self.rect.left + 20, self.rect.top + 60, 60, 30)
        self.exit_button = pygame.Rect(self.rect.left + 20, self.rect.top + 100, 60, 30)

    def draw(self, screen):
        self.overlay.fill((0, 0, 0, 180))
        screen.blit(self.overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.rect, border_radius=10)
        pygame.draw.rect(screen, (40, 40, 40), self.rect, 3, border_radius=10)

        font = pygame.font.Font(None, 36)
        text = font.render("Back", True, (40, 40, 40))
        screen.blit(text, self.back_button)

        text = font.render("Reset", True, (40, 40, 40))
        screen.blit(text, self.reset_button)

        text = font.render("Exit", True, (40, 40, 40))
        screen.blit(text, self.exit_button)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "return_game"
            elif self.reset_button.collidepoint(event.pos):
                return "reset"
            elif self.exit_button.collidepoint(event.pos):
                return "exit"
        return None
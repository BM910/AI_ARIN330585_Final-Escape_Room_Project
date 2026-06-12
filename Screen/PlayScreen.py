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
                return "back"
            elif self.reset_button.collidepoint(event.pos):
                return "reset"
            elif self.exit_button.collidepoint(event.pos):
                return "exit"
        return None


class PlayScreen:
    def __init__(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = (0, 0)

        self.resume_screen = ResumeScreen()
        self.resume_button = pygame.Rect(WIDTH - 120, HEIGHT - 70, 100, 50)
        self.check_resume = False

        self.list_events = {
            "back": self.back,
            "reset": self.reset,
            "exit": self.exit
        }

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.check_resume:
                if self.resume_button.collidepoint(event.pos):
                    self.check_resume = True
            else:
                result = self.resume_screen.handle_event(event)
                if result in self.list_events:
                    self.list_events[result]()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.player_pos += (self.player_pos[0] - 1, self.player_pos[1])
            elif event.key == pygame.K_DOWN:
                self.player_pos += (self.player_pos[0] + 1, self.player_pos[1])
            elif event.key == pygame.K_LEFT:
                self.player_pos += (self.player_pos[0], self.player_pos[1] - 1)
            elif event.key == pygame.K_RIGHT:
                self.player_pos += (self.player_pos[0], self.player_pos[1] + 1)

    def reset(self):
        self.grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        self.player_pos = (0, 0)

        self.check_resume = False

    def back(self):
        self.check_resume = False

    def exit(self):
        pass

    def draw(self, screen):
        screen.fill((255, 255, 255))

        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        player_rect = pygame.Rect(
            self.player_pos[1] * CELL_SIZE,
            self.player_pos[0] * CELL_SIZE,
            CELL_SIZE,
            CELL_SIZE
        )
        pygame.draw.rect(screen, (255, 0, 0), player_rect)
        pygame.draw.rect(screen, (0, 255, 0), self.resume_button)


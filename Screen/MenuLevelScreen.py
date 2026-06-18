import pygame

WIDTH, HEIGHT = 1000, 600

class LevelScreen:
    def __init__(self):
        self.popup = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 300)

        self.level_buttons = []
        button_size = 60  
        gap_x = 40        
        gap_y = 30        
        
        start_x = self.popup.x + 50  
        start_y = self.popup.y + 100 

        for i in range(6):
            row = i // 3  
            col = i % 3   
            x = start_x + col * (button_size + gap_x)
            y = start_y + row * (button_size + gap_y)
            self.level_buttons.append(pygame.Rect(x, y, button_size, button_size))

        self.back_button = pygame.Rect(self.popup.right - 45, self.popup.top + 15, 30, 30)

        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def draw(self, screen):
        self.overlay.fill((0, 0, 0, 180)) 
        screen.blit(self.overlay, (0, 0))

        pygame.draw.rect(screen, (255, 255, 255), self.popup, border_radius=15)
        pygame.draw.rect(screen, (40, 40, 40), self.popup, 3, border_radius=15) 

        font_title = pygame.font.Font(None, 40)
        font_text = pygame.font.Font(None, 32)


        title_text = font_title.render("SELECT LEVEL", True, (40, 40, 40))
        title_rect = title_text.get_rect(center=(self.popup.centerx, self.popup.top + 50))
        screen.blit(title_text, title_rect)

        for i, button in enumerate(self.level_buttons):
            pygame.draw.rect(screen, (0, 128, 255), button, border_radius=8)
            
            text = font_text.render(f"{i + 1}", True, (255, 255, 255))
            
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

        # --- 4. Vẽ nút Đóng (X) màu đỏ ---
        pygame.draw.rect(screen, (230, 50, 50), self.back_button, border_radius=5)
        
        font_close = pygame.font.Font(None, 24)
        close_text = font_close.render("X", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=self.back_button.center)
        screen.blit(close_text, close_rect)
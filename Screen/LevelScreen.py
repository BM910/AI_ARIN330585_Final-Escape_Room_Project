import pygame

WIDTH, HEIGHT = 1000, 600

class LevelScreen:
    def __init__(self):
        # 1. Bảng Popup chính (Rộng 400, Cao 300 - Căn giữa màn hình)
        # Tọa độ thực tế: X từ 300 đến 700, Y từ 150 đến 450
        self.popup = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 150, 400, 300)

        # 2. Danh sách 6 nút chọn Level (Chia làm 2 hàng, mỗi hàng 3 nút)
        # Tính toán dựa trên tọa độ gốc của Popup (self.popup.x và self.popup.y) để dễ quản lý
        self.level_buttons = []
        button_size = 60  # Tăng kích thước nút lên một chút cho dễ nhìn (60x60)
        gap_x = 40        # Khoảng cách ngang giữa các nút
        gap_y = 30        # Khoảng cách dọc giữa các hàng
        
        # Điểm bắt đầu vẽ nút đầu tiên bên trong popup
        start_x = self.popup.x + 50  
        start_y = self.popup.y + 100 

        for i in range(6):
            row = i // 3  # Hàng 0 hoặc Hàng 1
            col = i % 3   # Cột 0, 1 hoặc 2
            x = start_x + col * (button_size + gap_x)
            y = start_y + row * (button_size + gap_y)
            self.level_buttons.append(pygame.Rect(x, y, button_size, button_size))

        # 3. Nút Back (X) - Đặt ở góc trên cùng bên phải CỦA POPUP
        # Cách mép phải popup 45px và mép trên popup 15px
        self.back_button = pygame.Rect(self.popup.right - 45, self.popup.top + 15, 30, 30)

        # 4. Lớp phủ làm tối nền
        self.overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

    def draw(self, screen):
        # --- 1. Vẽ lớp phủ tối nền ---
        self.overlay.fill((0, 0, 0, 180)) # Tăng độ tối một chút (180) cho nổi bật popup
        screen.blit(self.overlay, (0, 0))

        # --- 2. Vẽ Bảng Popup (Có bo góc) ---
        pygame.draw.rect(screen, (255, 255, 255), self.popup, border_radius=15)
        pygame.draw.rect(screen, (40, 40, 40), self.popup, 3, border_radius=15) # Viền màu xám đậm

        # Khởi tạo Font chữ
        font_title = pygame.font.Font(None, 40)
        font_text = pygame.font.Font(None, 32)

        # Vẽ tiêu đề "SELECT LEVEL" cho Popup
        title_text = font_title.render("SELECT LEVEL", True, (40, 40, 40))
        title_rect = title_text.get_rect(center=(self.popup.centerx, self.popup.top + 50))
        screen.blit(title_text, title_rect)

        # --- 3. Vẽ các nút Level (Căn giữa chữ chuẩn xác) ---
        for i, button in enumerate(self.level_buttons):
            # Vẽ nút (Màu xanh dương, bo góc nhẹ)
            pygame.draw.rect(screen, (0, 128, 255), button, border_radius=8)
            
            # Tạo chữ số
            text = font_text.render(f"{i + 1}", True, (255, 255, 255))
            
            # CÁCH MỚI: Dùng get_rect(center=...) để chữ luôn nằm CHÍNH GIỮA nút dù font to hay nhỏ
            text_rect = text.get_rect(center=button.center)
            screen.blit(text, text_rect)

        # --- 4. Vẽ nút Đóng (X) màu đỏ ---
        pygame.draw.rect(screen, (230, 50, 50), self.back_button, border_radius=5)
        
        font_close = pygame.font.Font(None, 24)
        close_text = font_close.render("X", True, (255, 255, 255))
        close_rect = close_text.get_rect(center=self.back_button.center)
        screen.blit(close_text, close_rect)
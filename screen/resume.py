import pygame

WIDTH, HEIGHT = 1000, 600

PANEL_W, PANEL_H = 200, 190
PANEL_X = WIDTH  // 2 - PANEL_W // 2
PANEL_Y = HEIGHT // 2 - PANEL_H // 2

BTN_W, BTN_H = 160, 40
BTN_GAP = 12
BTN_X = PANEL_X + (PANEL_W - BTN_W) // 2
BTN_Y = PANEL_Y + 20

VIGNETTE_STEP   = 2
VIGNETTE_ALPHA  = 110
OVERLAY_ALPHA   = 90

PANEL_RADIUS    = 10
PANEL_BG        = (255, 255, 255)
PANEL_BORDER    = (40, 40, 40)
PANEL_BORDER_W  = 2

BTN_RADIUS      = 8
BTN_BORDER      = (40, 40, 40)
BTN_NORMAL_BG   = (245, 245, 245)
BTN_NORMAL_HOV  = (220, 220, 220)
BTN_NORMAL_FG   = (40, 40, 40)
BTN_DANGER_BG   = (255, 235, 235)
BTN_DANGER_HOV  = (255, 210, 210)
BTN_DANGER_FG   = (160, 40, 40)

FONT_NAME = "segoeui"
FONT_SIZE = 18


class ResumeScreen:
    def __init__(self):
        self.overlay  = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.vignette = self._make_vignette()

        self.rect = pygame.Rect(PANEL_X, PANEL_Y, PANEL_W, PANEL_H)

        self.back_button  = pygame.Rect(BTN_X, BTN_Y,                                BTN_W, BTN_H)
        self.reset_button = pygame.Rect(BTN_X, BTN_Y + BTN_H + BTN_GAP,              BTN_W, BTN_H)
        self.exit_button  = pygame.Rect(BTN_X, BTN_Y + (BTN_H + BTN_GAP) * 2,       BTN_W, BTN_H)

        self.font = None 

    def _make_vignette(self):
        surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        cx, cy = WIDTH // 2, HEIGHT // 2
        max_r  = (cx**2 + cy**2) ** 0.5

        for y in range(0, HEIGHT, VIGNETTE_STEP):
            for x in range(0, WIDTH, VIGNETTE_STEP):
                dist  = ((x - cx)**2 + (y - cy)**2) ** 0.5
                t     = min(dist / max_r, 1.0)
                alpha = int(VIGNETTE_ALPHA * t * t)
                surf.set_at((x,   y),   (0, 0, 0, alpha))
                surf.set_at((x+1, y),   (0, 0, 0, alpha))
                surf.set_at((x,   y+1), (0, 0, 0, alpha))
                surf.set_at((x+1, y+1), (0, 0, 0, alpha))
        return surf

    def _get_font(self):
        if self.font is None:
            self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE)
        return self.font

    def _draw_button(self, screen, rect, label, danger=False):
        hovered = rect.collidepoint(pygame.mouse.get_pos())

        if danger:
            bg    = BTN_DANGER_HOV if hovered else BTN_DANGER_BG
            color = BTN_DANGER_FG
        else:
            bg    = BTN_NORMAL_HOV if hovered else BTN_NORMAL_BG
            color = BTN_NORMAL_FG

        pygame.draw.rect(screen, bg,         rect, border_radius=BTN_RADIUS)
        pygame.draw.rect(screen, BTN_BORDER, rect, 1, border_radius=BTN_RADIUS)

        text = self._get_font().render(label, True, color)
        screen.blit(text, text.get_rect(center=rect.center))

    def draw(self, screen):
        self.overlay.fill((0, 0, 0, OVERLAY_ALPHA))
        screen.blit(self.overlay,  (0, 0))
        screen.blit(self.vignette, (0, 0))

        pygame.draw.rect(screen, PANEL_BG,     self.rect, border_radius=PANEL_RADIUS)
        pygame.draw.rect(screen, PANEL_BORDER, self.rect, PANEL_BORDER_W, border_radius=PANEL_RADIUS)

        self._draw_button(screen, self.back_button,  "Tiếp tục")
        self._draw_button(screen, self.reset_button, "Chơi lại")
        self._draw_button(screen, self.exit_button,  "Thoát", danger=True)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "return_game"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.back_button.collidepoint(event.pos):
                return "return_game"
            elif self.reset_button.collidepoint(event.pos):
                return "reset"
            elif self.exit_button.collidepoint(event.pos):
                return "exit"
        return None
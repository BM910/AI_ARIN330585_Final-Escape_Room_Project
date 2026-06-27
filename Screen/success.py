import pygame
from data.icons.navigation import ICON_MENU, ICON_NEXT, ICON_RESET
from data.icons.draw import draw_pixel_icon

WIDTH, HEIGHT = 1000, 600

BOX_W, BOX_H    = 360, 340
BOX_X           = (WIDTH  - BOX_W) // 2
BOX_Y           = (HEIGHT - BOX_H) // 2
BOX_RADIUS      = 16
BOX_BG          = (245, 245, 245)
BOX_BORDER      = (200, 200, 200)

BTN_W, BTN_H    = 90, 48
BTN_GAP         = 16
BTN_TOTAL_W     = BTN_W * 3 + BTN_GAP * 2
BTN_X_START     = BOX_X + (BOX_W - BTN_TOTAL_W) // 2
BTN_Y           = BOX_Y + BOX_H - BTN_H - 20
BTN_RADIUS      = 10

BTN_NORMAL_BG   = (240, 240, 240)
BTN_NORMAL_HOV  = (210, 210, 210)
BTN_NORMAL_FG   = (60,  60,  60)
BTN_NORMAL_BDR  = (160, 160, 160)

BTN_ACCENT_BG   = (210, 235, 255)
BTN_ACCENT_HOV  = (180, 220, 255)
BTN_ACCENT_FG   = (20,  80,  160)
BTN_ACCENT_BDR  = (100, 160, 220)

BTN_DANGER_BG   = (255, 230, 230)
BTN_DANGER_HOV  = (255, 200, 200)
BTN_DANGER_FG   = (160, 40,  40)
BTN_DANGER_BDR  = (200, 100, 100)

ICON_CIRCLE_BG  = (210, 240, 215)
ICON_CIRCLE_R   = 38
ICON_CY_OFFSET  = 100         
ICON_FG         = (40,  150,  80)

TITLE_TEXT      = "Level complete!"
TITLE_COLOR     = (30,  30,  30)
TITLE_SIZE      = 22
TITLE_Y_OFFSET  = 46           

DESC_TEXT       = "Well done — on to the next challenge."
DESC_COLOR      = (100, 100, 100)
DESC_SIZE       = 14
DESC_Y_OFFSET   = 76          

LEVEL_COLOR     = (150, 150, 150)
LEVEL_SIZE      = 13
LEVEL_Y_OFFSET  = 18           

FONT_NAME       = "segoeui"
FONT_EMOJI      = "segoeuiemoji"
FONT_SIZE_MAIN  = 18
FONT_SIZE_SMALL = 13
FONT_SIZE_ICON  = 22

VIGNETTE_STEP   = 2
VIGNETTE_ALPHA  = 110
OVERLAY_ALPHA   = 90


class SuccessScreen:
    def __init__(self, level):
        self.level = level

        self.overlay  = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        self.vignette = self._make_vignette()

        self.rect = pygame.Rect(BOX_X, BOX_Y, BOX_W, BOX_H)

        self.menu_button       = pygame.Rect(BTN_X_START,                        BTN_Y, BTN_W, BTN_H)
        self.reset_button      = pygame.Rect(BTN_X_START + BTN_W + BTN_GAP,      BTN_Y, BTN_W, BTN_H)
        self.next_level_button = pygame.Rect(BTN_X_START + (BTN_W + BTN_GAP) * 2, BTN_Y, BTN_W, BTN_H)

        self.font       = None
        self.font_small = None

    def _make_vignette(self):
        """Tạo lớp vignette: tối ở rìa, trong suốt ở giữa."""
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
            self.font = pygame.font.SysFont(FONT_NAME, FONT_SIZE_MAIN)
        return self.font

    def _get_font_small(self):
        if self.font_small is None:
            self.font_small = pygame.font.SysFont(FONT_NAME, FONT_SIZE_SMALL)
        return self.font_small

    def _draw_button(self, screen, rect, icon_matrix, accent=False, danger=False):
        hovered = rect.collidepoint(pygame.mouse.get_pos())

        if accent:
            bg, border, fg = (BTN_ACCENT_HOV if hovered else BTN_ACCENT_BG), BTN_ACCENT_BDR, BTN_ACCENT_FG
        elif danger:
            bg, border, fg = (BTN_DANGER_HOV if hovered else BTN_DANGER_BG), BTN_DANGER_BDR, BTN_DANGER_FG
        else:
            bg, border, fg = (BTN_NORMAL_HOV if hovered else BTN_NORMAL_BG), BTN_NORMAL_BDR, BTN_NORMAL_FG

        pygame.draw.rect(screen, bg,     rect, border_radius=BTN_RADIUS)
        pygame.draw.rect(screen, border, rect, 1, border_radius=BTN_RADIUS)

        draw_pixel_icon(screen, icon_matrix,
                        cx=rect.centerx,
                        cy=rect.centery,   
                        pixel_size=1,
                        color_main=fg)

    def draw(self, screen):
        self.overlay.fill((0, 0, 0, OVERLAY_ALPHA))
        screen.blit(self.overlay,  (0, 0))
        screen.blit(self.vignette, (0, 0))

        pygame.draw.rect(screen, BOX_BG,     self.rect, border_radius=BOX_RADIUS)
        pygame.draw.rect(screen, BOX_BORDER, self.rect, 1, border_radius=BOX_RADIUS)

        cx      = self.rect.centerx
        icon_cy = BOX_Y + ICON_CY_OFFSET

        lv_surf = pygame.font.SysFont(FONT_NAME, LEVEL_SIZE).render(
            f"LEVEL {self.level}", True, LEVEL_COLOR)
        screen.blit(lv_surf, lv_surf.get_rect(centerx=cx, top=BOX_Y + LEVEL_Y_OFFSET))

        pygame.draw.circle(screen, ICON_CIRCLE_BG, (cx, icon_cy), ICON_CIRCLE_R)
        trophy_surf = pygame.font.SysFont(FONT_EMOJI, ICON_CIRCLE_R).render("🏆", True, ICON_FG)
        screen.blit(trophy_surf, trophy_surf.get_rect(center=(cx, icon_cy)))

        title_surf = pygame.font.SysFont(FONT_NAME, TITLE_SIZE).render(TITLE_TEXT, True, TITLE_COLOR)
        screen.blit(title_surf, title_surf.get_rect(centerx=cx, top=icon_cy + TITLE_Y_OFFSET))

        desc_surf = pygame.font.SysFont(FONT_NAME, DESC_SIZE).render(DESC_TEXT, True, DESC_COLOR)
        screen.blit(desc_surf, desc_surf.get_rect(centerx=cx, top=icon_cy + DESC_Y_OFFSET))

        self._draw_button(screen, self.menu_button,       ICON_MENU)
        self._draw_button(screen, self.reset_button,      ICON_RESET)
        self._draw_button(screen, self.next_level_button, ICON_NEXT, accent=True)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            return "return_game"
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.next_level_button.collidepoint(event.pos):
                return "next_level"
            elif self.reset_button.collidepoint(event.pos):
                return "reset"
            elif self.menu_button.collidepoint(event.pos):
                return "menu level"
        return None
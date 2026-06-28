import pygame

CELL_SIZE = 80   # default; caller có thể truyền size khác qua param

KEY_COLORS = {
    'a': (255, 200,  40),
    'b': ( 80, 160, 255),
    'c': (120, 220,  80),
    'd': (220,  80, 220),
    'e': ( 80, 220, 200),
}

# ── PIXEL-ART DRAW HELPERS ──────────────────────────────────────────

def draw_floor(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (200, 195, 180), rect)
    pygame.draw.line(surf, (180, 175, 160), (x, y),     (x+w, y),   1)
    pygame.draw.line(surf, (180, 175, 160), (x, y),     (x,   y+h), 1)


def draw_brick(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (100, 50, 40), rect)
    pygame.draw.rect(surf, ( 60, 30, 25), rect, 2)
    pygame.draw.line(surf, (40, 20, 15), (x,        y+h//2), (x+w,      y+h//2), 2)
    pygame.draw.line(surf, (40, 20, 15), (x+w//3,   y),      (x+w//3,   y+h//2), 2)
    pygame.draw.line(surf, (40, 20, 15), (x+w*2//3, y+h//2), (x+w*2//3, y+h),    2)


def draw_door(surf, rect, ch):
    col = KEY_COLORS.get(ch.lower(), (150, 150, 150))
    x, y, w, h = rect
    pygame.draw.rect(surf, (40, 40, 40), rect)
    pygame.draw.rect(surf, col, (x+8, y+15, w-16, h-15))
    pygame.draw.circle(surf, col, (x+w//2, y+15), max(1, (w-16)//2))
    pygame.draw.circle(surf, (20, 20, 20), (x+w//2, y+h//2+5), max(1, w//16))
    f = pygame.font.SysFont("courier", max(10, w//4), bold=True)
    t = f.render(ch.upper(), True, (255, 255, 255))
    surf.blit(t, t.get_rect(center=(x+w//2, y+10)))


def draw_key(surf, rect, ch):
    col = KEY_COLORS.get(ch.lower(), (255, 215, 0))
    x, y, w, h = rect
    draw_floor(surf, rect)
    cx, cy = x+w//2, y+h//2
    r = max(4, w//10)
    pygame.draw.circle(surf, col, (cx-r, cy-r), r, max(1, r//2))
    pygame.draw.line(surf, col, (cx-r//2, cy-r//2), (cx+r*2, cy+r*2), max(1, r//3))
    pygame.draw.line(surf, col, (cx+r,    cy+r),    (cx+r*2, cy),     max(1, r//3))
    pygame.draw.line(surf, col, (cx+r*2,  cy+r*2),  (cx+r*3, cy+r),   max(1, r//3))
    f = pygame.font.SysFont("courier", max(10, w//4), bold=True)
    surf.blit(f.render(ch, True, (255, 255, 255)), (x+3, y+3))


def draw_energy(surf, rect, value):
    col  = (60, 200, 100) if value > 0 else (210, 70, 70)
    dark = (20,  90,  40) if value > 0 else (120, 20, 20)
    x, y, w, h = rect
    pygame.draw.rect(surf, dark, rect)
    cx, cy = x+w//2, y+h//2
    s = max(8, w//5)
    pts = [(cx, cy-s), (cx+s, cy), (cx, cy+s), (cx-s, cy)]
    pygame.draw.polygon(surf, col, pts)
    pygame.draw.polygon(surf, (255, 255, 255), pts, 1)
    sign = '+' if value > 0 else ''
    f = pygame.font.SysFont("courier", max(10, w//4), bold=True)
    t = f.render(f"{sign}{value}", True, (255, 255, 255))
    surf.blit(t, t.get_rect(center=(cx, cy)))


def draw_start(surf, rect):
    x, y, w, h = rect
    draw_floor(surf, rect)
    pygame.draw.rect(surf, (30, 160, 90),
                     (x+6, y+6, w-12, h-12), border_radius=max(2, w//12))
    f = pygame.font.SysFont("courier", max(12, w//3), bold=True)
    t = f.render("S", True, (220, 255, 220))
    surf.blit(t, t.get_rect(center=(x+w//2, y+h//2)))


def draw_exit(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (20, 20, 50), rect)
    cx, cy = x+w//2, y+h//2
    r = max(6, w//3)
    pygame.draw.circle(surf, ( 40,  80, 200), (cx, cy), r)
    pygame.draw.circle(surf, ( 80, 140, 255), (cx, cy), int(r*0.72))
    pygame.draw.circle(surf, (180, 220, 255), (cx, cy), int(r*0.36))
    pygame.draw.circle(surf, (255, 255, 255), (cx, cy), max(2, int(r*0.14)))
    f = pygame.font.SysFont("courier", max(9, w//5), bold=True)
    t = f.render("EXIT", True, (200, 230, 255))
    surf.blit(t, t.get_rect(center=(cx, cy + int(r*0.8))))


def draw_connect4_tile(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (60, 20, 90), rect)
    cx, cy = x+w//2, y+h//2
    r = max(4, w//3)
    pygame.draw.circle(surf, (180, 60, 220), (cx, cy), r, max(1, r//5))
    pygame.draw.line(surf, (180, 60, 220), (cx-r//2, cy), (cx+r//2, cy), max(1, r//8))
    pygame.draw.line(surf, (180, 60, 220), (cx, cy-r//2), (cx, cy+r//2), max(1, r//8))
    f = pygame.font.SysFont("courier", max(9, w//5), bold=True)
    t = f.render("C4", True, (255, 200, 255))
    surf.blit(t, t.get_rect(center=(cx, y + max(8, h//5))))


def draw_sudoku_tile(surf, rect):
    x, y, w, h = rect
    pygame.draw.rect(surf, (20, 60, 90), rect)
    f = pygame.font.SysFont("courier", max(12, w//3), bold=True)
    t = f.render("@", True, (120, 200, 255))
    surf.blit(t, t.get_rect(center=(x+w//2, y+h//2)))


def draw_random_tile(surf, rect):
    """Ô '+' — mũi tên 4 chiều dạng thập tự."""
    x, y, w, h = rect
    pygame.draw.rect(surf, (60, 20, 90), rect)
    cx, cy = x + w // 2, y + h // 2

    # Tỉ lệ theo kích thước ô — giữ toàn bộ hình trong rect
    arm   = int(w * 0.30)   # độ dài cánh tay tính từ tâm
    shaft = int(w * 0.10)   # nửa độ rộng thân
    head  = int(w * 0.16)   # nửa độ rộng đầu mũi tên
    tip   = int(w * 0.05)   # khoảng thụt vào ở góc đầu mũi tên

    COL   = (255, 109, 0)   # cam đậm

    def arrow_up():
        return [
            (cx - shaft, cy - tip),
            (cx - shaft, cy + arm - tip),
            (cx + shaft, cy + arm - tip),
            (cx + shaft, cy - tip),
        ]

    def arrow_down():
        return [
            (cx - shaft, cy + tip),
            (cx - shaft, cy - arm + tip),
            (cx + shaft, cy - arm + tip),
            (cx + shaft, cy + tip),
        ]

    def arrow_left():
        return [
            (cx + tip,        cy - shaft),
            (cx - arm + tip,  cy - shaft),
            (cx - arm + tip,  cy + shaft),
            (cx + tip,        cy + shaft),
        ]

    def arrow_right():
        return [
            (cx - tip,        cy - shaft),
            (cx + arm - tip,  cy - shaft),
            (cx + arm - tip,  cy + shaft),
            (cx - tip,        cy + shaft),
        ]

    # Thân thập tự (4 hình chữ nhật gộp lại thành hình +)
    pygame.draw.rect(surf, COL, (cx - shaft, cy - arm, shaft*2, arm*2))  # dọc
    pygame.draw.rect(surf, COL, (cx - arm, cy - shaft, arm*2, shaft*2))  # ngang

    # Đầu mũi tên — UP
    pygame.draw.polygon(surf, COL, [
        (cx,        cy - arm - head),
        (cx - head, cy - arm + tip),
        (cx + head, cy - arm + tip),
    ])
    # DOWN
    pygame.draw.polygon(surf, COL, [
        (cx,        cy + arm + head),
        (cx - head, cy + arm - tip),
        (cx + head, cy + arm - tip),
    ])
    # LEFT
    pygame.draw.polygon(surf, COL, [
        (cx - arm - head, cy),
        (cx - arm + tip,  cy - head),
        (cx - arm + tip,  cy + head),
    ])
    # RIGHT
    pygame.draw.polygon(surf, COL, [
        (cx + arm + head, cy),
        (cx + arm - tip,  cy - head),
        (cx + arm - tip,  cy + head),
    ])


def draw_robot(surf, rect):
    x, y, w, h = rect
    cx, cy = x+w//2, y+h//2
    a = max(3, w//8)
    pygame.draw.rect(surf, (50, 50,  50), (x+a*2,   y+a,   a,     h-a*2), border_radius=2)
    pygame.draw.rect(surf, (50, 50,  50), (x+w-a*3, y+a,   a,     h-a*2), border_radius=2)
    pygame.draw.rect(surf, (80, 180, 220), (cx-a*3, cy-a,  a*6,  a*2+2), border_radius=2)
    pygame.draw.rect(surf, (200, 220, 240), (cx-a*2, cy-a*3, a*4, a*2),   border_radius=2)
    pygame.draw.circle(surf, (255, 50, 100), (cx-a,  cy-a*2), max(1, a//2))
    pygame.draw.circle(surf, (255, 50, 100), (cx+a,  cy-a*2), max(1, a//2))


# ── UNIFIED CELL DISPATCHER ─────────────────────────────────────────

def draw_cell(surf, rect, value):
    """Vẽ một ô bản đồ dựa theo giá trị.
    rect = (px, py, cell_w, cell_h)
    """
    if value == '#':
        draw_brick(surf, rect)
    elif value == 'S':
        draw_start(surf, rect)
    elif value == 'E':
        draw_exit(surf, rect)
    elif value == '.':
        draw_floor(surf, rect)
    elif value == '@':
        draw_sudoku_tile(surf, rect)
    elif value == '$':
        draw_connect4_tile(surf, rect)
    elif value == '+':
        draw_random_tile(surf, rect)
    elif isinstance(value, int):
        draw_energy(surf, rect, value)
    elif isinstance(value, str) and value.islower():
        draw_key(surf, rect, value)
    elif isinstance(value, str) and value.isupper() and value not in ('S', 'E'):
        draw_door(surf, rect, value)
    else:
        draw_floor(surf, rect)
import pygame

CELL_SIZE = 80 

KEY_COLORS = {
    'a': (255, 200,  40),
    'b': ( 80, 160, 255),
    'c': (120, 220,  80),
    'd': (220,  80, 220),
    'e': ( 80, 220, 200),
}


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

    dw  = int(w * 0.50)
    dh  = int(h * 0.55)
    dx  = x + (w - dw) // 2
    dy  = y + int(h * 0.20)
    r   = dw // 2

    pygame.draw.rect(surf, col, (dx, dy + r, dw, dh))

    import math
    arc_pts = [(dx + r + int(r * math.cos(math.radians(a))),
                dy + r + int(r * math.sin(math.radians(a))))
               for a in range(180, 361, 5)]
    pygame.draw.polygon(surf, col, arc_pts)

    pygame.draw.line(surf, (20, 20, 20), (dx, dy + r),          (dx, dy + r + dh),      2) 
    pygame.draw.line(surf, (20, 20, 20), (dx, dy + r + dh),     (dx + dw, dy + r + dh), 2)
    pygame.draw.line(surf, (20, 20, 20), (dx + dw, dy + r + dh),(dx + dw, dy + r),      2) 
    pygame.draw.arc(surf, (20, 20, 20),
                    (dx, dy, dw, dw), math.radians(0), math.radians(180), 2)


    kx = dx + int(dw * 0.30)
    ky = dy + r + int(dh * 0.50)
    pygame.draw.circle(surf, (20, 20, 20), (kx, ky), max(2, w // 18))



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
    x, y, w, h = rect
    pygame.draw.rect(surf, (60, 20, 90), rect)
    cx, cy = x + w // 2, y + h // 2

    arm   = int(w * 0.30)
    shaft = int(w * 0.10)
    head  = int(w * 0.16)
    tip   = int(w * 0.05)
    COL   = (255, 109, 0) 

    pygame.draw.rect(surf, COL, (cx - shaft, cy - arm, shaft*2, arm*2))
    pygame.draw.rect(surf, COL, (cx - arm, cy - shaft, arm*2, shaft*2))

    # UP
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


def draw_key_bar(surf, keys, x, y, size=28):
    if not keys:
        return x

    gap = 6
    for ch in sorted(keys):
        col = KEY_COLORS.get(ch.lower(), (255, 215, 0))
        cx, cy = x + size//2, y + size//2

        pygame.draw.circle(surf, (40, 40, 50), (cx, cy), size//2)
        pygame.draw.circle(surf, col,           (cx, cy), size//2, 2)

        r  = max(3, size // 7)
        lw = max(1, size // 14)
        pygame.draw.circle(surf, col, (cx - r, cy - r), r, lw)
        pygame.draw.line(surf, col,
                         (cx - r + r//2, cy - r + r//2),
                         (cx + r*2,      cy + r*2), lw + 1)
        pygame.draw.line(surf, col,
                         (cx + r,   cy + r),
                         (cx + r*2, cy),      lw + 1)
        pygame.draw.line(surf, col,
                         (cx + r*2, cy + r*2),
                         (cx + r*3, cy + r),  lw + 1)

        f = pygame.font.SysFont("courier", max(8, size // 3), bold=True)
        t = f.render(ch.upper(), True, col)
        surf.blit(t, (x + 2, y + size - size//3 - 2))

        x += size + gap

    return x

def draw_cell(surf, rect, value):
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
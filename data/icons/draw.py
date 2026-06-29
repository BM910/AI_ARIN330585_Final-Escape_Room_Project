import pygame 

def draw_pixel_icon(screen, matrix, cx, cy, pixel_size, color_main, color_shadow=None):
    """Vẽ icon pixel từ ma trận 32x32 ra màn hình."""
    if color_shadow is None:
        color_shadow = tuple(max(0, c - 60) for c in color_main)

    rows = len(matrix)
    cols = len(matrix[0])

    ox = cx - (cols * pixel_size) // 2
    oy = cy - (rows * pixel_size) // 2

    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            if val == 0:
                continue
            color = color_main if val == 1 else color_shadow
            pygame.draw.rect(
                screen,
                color,
                (ox + c * pixel_size, oy + r * pixel_size, pixel_size, pixel_size)
            )
import pygame
import copy
import traceback
import threading
import time

from algorithms.breadth_first_search import bfs
from algorithms.depth_first_search import dfs_version_2
from algorithms.ucs import ucs
# ── CONFIG ────────────────────────────────────────────────────────────────────
WIDTH, HEIGHT = 1280, 760
CELL          = 56

PANEL_LEFT   = pygame.Rect(0, 0, 220, 640)
PANEL_CENTER = pygame.Rect(220, 0, 700, 640)
PANEL_RIGHT  = pygame.Rect(920, 0, 360, 640)
PANEL_BOTTOM = pygame.Rect(0, 640, 1280, 120)

BG   = (20, 20, 28)
PBG  = (35, 35, 45)
BDR  = (100, 255, 150)
TXT  = (220, 240, 220)

KEY_COLORS = {
    'a': (255, 60,  60),
    'b': (60,  150, 255),
    'c': (60,  255, 60),
    'd': (255, 100, 255),
}

# PHẦN NÀY THAY THUẬT TOÁN VÀO
# ── ALGO REGISTRY  fn(map, energy) → list[Node] | None ───────────────────────
ALGOS = {
    "BFS": bfs,
    "DFS": dfs_version_2,
    "UCS": ucs,
}

# ── DRAW HELPERS ──────────────────────────────────────────────────────────────
def _find_start(map_):
    for r, row in enumerate(map_):
        for c, v in enumerate(row):
            if v == 'S': return r, c
    return 0, 0

def draw_brick(surf, rect):
    pygame.draw.rect(surf, (100, 50, 40), rect)
    pygame.draw.rect(surf, (60,  30, 25), rect, 2)
    x, y, w, h = rect
    pygame.draw.line(surf, (40,20,15), (x,      y+h//2), (x+w,    y+h//2), 2)
    pygame.draw.line(surf, (40,20,15), (x+w//3, y),      (x+w//3, y+h//2), 2)
    pygame.draw.line(surf, (40,20,15), (x+w*2//3, y+h//2),(x+w*2//3, y+h), 2)

def draw_door(surf, rect, ch):
    col = KEY_COLORS.get(ch.lower(), (150,150,150))
    x, y, w, h = rect
    pygame.draw.rect(surf, (40,40,40), rect)
    pygame.draw.rect(surf, col, (x+8, y+15, w-16, h-15))
    pygame.draw.circle(surf, col, (x+w//2, y+15), (w-16)//2)
    pygame.draw.circle(surf, (20,20,20), (x+w//2, y+h//2+5), 5)
    f = pygame.font.SysFont("courier", 14, bold=True)
    t = f.render(ch, True, (255,255,255))
    surf.blit(t, t.get_rect(center=(x+w//2, y+10)))

def is_escaped(state):
    return state.map[state.x][state.y] == 'E'

def draw_key(surf, rect, ch):
    col = KEY_COLORS.get(ch.lower(), (255,215,0))
    x, y, w, h = rect
    cx, cy = x+w//2, y+h//2
    pygame.draw.circle(surf, col, (cx-10, cy-10), 8, 3)
    pygame.draw.line(surf, col, (cx-4, cy-4),   (cx+12, cy+12), 3)
    pygame.draw.line(surf, col, (cx+6, cy+6),   (cx+10, cy+2),  3)
    pygame.draw.line(surf, col, (cx+10, cy+10), (cx+14, cy+6),  3)
    f = pygame.font.SysFont("courier", 16, bold=True)
    surf.blit(f.render(ch, True, (255,255,255)), (x+5, y+5))

def draw_robot(surf, rect):
    x, y, w, h = rect
    cx, cy = x+w//2, y+h//2
    pygame.draw.rect(surf, (50,50,50),    (x+8,    y+10,  10, h-20), border_radius=4)
    pygame.draw.rect(surf, (50,50,50),    (x+w-18, y+10,  10, h-20), border_radius=4)
    pygame.draw.rect(surf, (80,180,220),  (cx-12,  cy-10, 24, 20),   border_radius=3)
    pygame.draw.rect(surf, (200,220,240), (cx-10,  cy-20, 20, 12),   border_radius=2)
    pygame.draw.circle(surf, (255,50,100), (cx-4, cy-15), 2)
    pygame.draw.circle(surf, (255,50,100), (cx+4, cy-15), 2)


# ── MAIN CLASS ────────────────────────────────────────────────────────────────
class AIReplayScreen:

    def __init__(self, start_map, energy=float('inf')):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Escape Room — AI Replay")
        self.clock  = pygame.time.Clock()

        self.ft  = pygame.font.SysFont("courier", 22, bold=True)
        self.fm  = pygame.font.SysFont("courier", 15, bold=True)
        self.fv  = pygame.font.SysFont("impact",  22)

        # Dữ liệu gốc — KHÔNG bao giờ thay đổi
        self.start_map    = copy.deepcopy(start_map)
        self.start_energy = energy
        self.rows = len(start_map)
        self.cols = len(start_map[0])
        self.ox   = PANEL_CENTER.x + (PANEL_CENTER.width  - self.cols * CELL) // 2
        self.oy   = PANEL_CENTER.y + (PANEL_CENTER.height - self.rows * CELL) // 2

        # Trạng thái hiển thị (reset được)
        self._reset_display()

        # Nút
        self.algo_btns = {}
        y = 70
        for name in ALGOS:
            self.algo_btns[name] = pygame.Rect(20, y, 180, 44)
            y += 56
        y += 10
        self.btn_run    = pygame.Rect(20, y,       180, 44); y += 54
        self.btn_reset  = pygame.Rect(20, y,       180, 44); y += 54
        self.btn_spdup  = pygame.Rect(20, y,        86, 38)
        self.btn_spddn  = pygame.Rect(114, y,       86, 38); y += 48
        self.btn_step   = pygame.Rect(20, y,       180, 38)

        self.selected = list(ALGOS.keys())[0]
        self.is_solving = False

    def _reset_display(self):
        """Về trạng thái ban đầu: robot tại 'S', map gốc, không có path."""
        sx, sy        = _find_start(self.start_map)
        self.cur_map  = copy.deepcopy(self.start_map)
        self.cur_x    = sx
        self.cur_y    = sy
        self.cur_e    = self.start_energy
        self.cur_keys = set()

        self.path_nodes   = []
        self.step_idx     = 0
        self.is_playing   = False
        self.last_tick    = 0
        self.delay        = 320
        self.logs         = ["Đã sẵn sàng."]
        self.result_str   = "Hiện chưa có kết quả."

    # ── algorithm ─────────────────────────────────────────────────────────────

    def _run_thread(self):
        self.is_solving = True
        name = self.selected
        self.logs.append(f"{name} đang tìm kiếm...")
        t0 = time.time()
        try:
            result  = ALGOS[name](copy.deepcopy(self.start_map), self.start_energy)
            elapsed = time.time() - t0
            nodes   = result if result else []

            if not nodes:
                self.result_str = f"{name} không tìm thấy đường đi."
                self.logs.append(self.result_str)
            else:
                self.path_nodes = nodes
                self.step_idx   = 0
                self.is_playing = True
                self._apply_node(nodes[0])
                actions = [str(n.action) for n in nodes if n.action]
                self.result_str = " -> ".join(actions) or "(no actions)"
                self.logs.append(f"Tìm thấy {len(nodes)-1} bước | {elapsed:.3f}s")
        except Exception as e:
            self.logs.append(f"[ERR] {e}")
            self.logs.append(traceback.format_exc().splitlines()[-1])
        self.is_solving = False

    def _apply_node(self, node):
        s = node.state
        self.cur_map  = copy.deepcopy(s.map)
        self.cur_x    = s.x
        self.cur_y    = s.y
        self.cur_e    = s.energy
        self.cur_keys = set(s.keys)

    def _step(self):
        if self.step_idx >= len(self.path_nodes):
            self.is_playing = False
            if is_escaped(self.path_nodes[-1].state):
                self.logs.append("Đã THOÁT KHỎI")
            else:
                self.logs.append("THẤT BẠI")
            self.logs.append("Kết thúc chuỗi được tìm thấy")
            return
        node = self.path_nodes[self.step_idx]
        self._apply_node(node)
        act = getattr(node, "action", None)
        keys = [str(k) for k in self.cur_keys if k]
        str_keys = ", ".join(keys) or " "
        self.logs.append(
            f"Bước {self.step_idx:02d}. {str(act) if act else 'START':<8}, E={self.cur_e}, K=[{str_keys}]")
        self.step_idx += 1

    # ── update ────────────────────────────────────────────────────────────────

    def update(self):
        if not self.is_playing or not self.path_nodes: return
        now = pygame.time.get_ticks()
        if now - self.last_tick > self.delay:
            self.last_tick = now
            self._step()

    # ── draw ──────────────────────────────────────────────────────────────────

    def _draw_cell(self, x, y, value):
        rect = pygame.Rect(x, y, CELL, CELL)
        pygame.draw.rect(self.screen, (40,45,55), rect)
        pygame.draw.rect(self.screen, (30,35,45), rect, 1)
        if value == '#':
            draw_brick(self.screen, rect)
        elif value == 'S':
            pygame.draw.rect(self.screen, (60,180,80), rect, border_radius=8)
            t = self.fm.render("S", True, (255,255,255))
            self.screen.blit(t, t.get_rect(center=rect.center))
        elif value == 'E':
            pygame.draw.rect(self.screen, (220,180,40), rect, border_radius=8)
            t = self.fm.render("EXIT", True, (0,0,0))
            self.screen.blit(t, t.get_rect(center=rect.center))
        elif value == '.':
            pass
        elif isinstance(value, str) and value.islower():
            draw_key(self.screen, rect, value)
        elif isinstance(value, str) and value.isupper():
            draw_door(self.screen, rect, value)
        elif isinstance(value, int):
            col = (50,200,80) if value > 0 else (220,50,50)
            pygame.draw.circle(self.screen, col, rect.center, 17)
            lbl = f"+{value}" if value > 0 else str(value)
            self.screen.blit(self.fv.render(lbl, True, (255,255,255)),
                             self.fv.render(lbl, True, (0,0,0)).get_rect(center=rect.center))

    def _btn(self, rect, label, bg, fg=(10,10,10), font=None):
        f = font or self.ft
        pygame.draw.rect(self.screen, bg,  rect, border_radius=6)
        pygame.draw.rect(self.screen, (80,80,80), rect, 2, border_radius=6)
        s = f.render(label, True, fg)
        self.screen.blit(s, s.get_rect(center=rect.center))

    def draw(self):
        self.screen.fill(BG)
        for p in [PANEL_LEFT, PANEL_CENTER, PANEL_RIGHT, PANEL_BOTTOM]:
            pygame.draw.rect(self.screen, PBG, p)
            pygame.draw.rect(self.screen, BDR, p, 2)

        # ── Panel trái ────────────────────────────────────────────
        self.screen.blit(self.ft.render("ALGORITHMS", True, TXT), (20, 20))
        for name, rect in self.algo_btns.items():
            sel = name == self.selected
            self._btn(rect, name,
                      (80,200,120) if sel else (55,65,85),
                      (10,20,10)   if sel else (220,220,220),
                      font=self.fm)

        # RUN / PAUSE / SOLVING
        if self.is_solving:
            run_bg, run_lbl = (130,110,40), "SOLVING..."
        elif self.is_playing:
            run_bg, run_lbl = (200,140,40), "PAUSE"
        else:
            run_bg, run_lbl = (60,130,210), "RUN"

        self._btn(self.btn_run,   run_lbl,  run_bg,       (255,255,255))
        self._btn(self.btn_reset, "RESET",  (180,70,70),  (255,255,255))
        self._btn(self.btn_spdup, "SPEED+", (80,160,100), font=self.fm)
        self._btn(self.btn_spddn, "SPEED-", (160,120,70), font=self.fm)

        step_en = bool(self.path_nodes) and not self.is_playing
        self._btn(self.btn_step, "STEP",
                  (70,100,160) if step_en else (40,42,50),
                  (220,230,255) if step_en else (80,82,90),
                  font=self.fm)

        self.screen.blit(self.fm.render(f"Delay: {self.delay}ms", True, TXT),
                         (20, self.btn_spddn.bottom + 6))
        total = len(self.path_nodes)
        self.screen.blit(self.fm.render(
            f"Step: {self.step_idx}/{total}" if total else "Step: -/-",
            True, (160,200,160)), (20, self.btn_step.bottom + 8))

        # ── Map ───────────────────────────────────────────────────
        for r in range(self.rows):
            for c in range(self.cols):
                self._draw_cell(self.ox + c*CELL, self.oy + r*CELL,
                                self.cur_map[r][c])
        draw_robot(self.screen, pygame.Rect(
            self.ox + self.cur_y * CELL,
            self.oy + self.cur_x * CELL, CELL, CELL))

        hud = (f"ENERGY: {self.cur_e}  |  "
               f"KEYS: {', '.join(sorted(self.cur_keys)) or 'None'}")
        self.screen.blit(self.fm.render(hud, True, (255,200,50)),
                         (PANEL_CENTER.x + 16, 12))

        # ── Log ───────────────────────────────────────────────────
        self.screen.blit(self.ft.render("TERMINAL LOG", True, TXT),
                         (PANEL_RIGHT.x + 12, 18))
        ly = 54
        for line in self.logs[-25:]:
            ok  = any(w in line.lower() for w in ("done","end","ready"))
            err = line.startswith("[ERR")
            col = (120,255,120) if ok else (255,100,100) if err else (185,205,225)
            self.screen.blit(self.fm.render(line, True, col),
                             (PANEL_RIGHT.x + 8, ly))
            ly += 22

        # ── Path bar ──────────────────────────────────────────────
        by = PANEL_BOTTOM.y
        self.screen.blit(self.ft.render("PATH:", True, (255,100,100)), (16, by+14))
        res = self.result_str[:185] if len(self.result_str) > 185 else self.result_str
        self.screen.blit(self.fm.render(res, True, (255,255,200)), (16, by+52))

        pygame.display.flip()

    # ── events ────────────────────────────────────────────────────────────────

    def handle_click(self, pos):
        for name, rect in self.algo_btns.items():
            if rect.collidepoint(pos):
                self.selected = name
                self.logs.append(f"Selected: {name}")
                return

        if self.btn_run.collidepoint(pos):
            if self.is_solving: return
            if self.is_playing:
                self.is_playing = False
                self.logs.append("Paused.")
            else:
                self._reset_display()
                threading.Thread(target=self._run_thread, daemon=True).start()
            return

        if self.btn_reset.collidepoint(pos):
            self._reset_display(); return

        if self.btn_spdup.collidepoint(pos):
            self.delay = max(80, self.delay - 40)
            self.logs.append(f"Delay -> {self.delay}ms"); return

        if self.btn_spddn.collidepoint(pos):
            self.delay = min(1200, self.delay + 40)
            self.logs.append(f"Delay -> {self.delay}ms"); return

        if self.btn_step.collidepoint(pos) and self.path_nodes and not self.is_playing:
            self._step()

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); return
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.handle_click(event.pos)
            self.update()
            self.draw()
            self.clock.tick(60)
import pygame
import sys
import threading
import time
import random
import copy

from algorithms.minimax_search import minimax_search
from algorithms.alpha_beta_search import alpha_beta_search
from algorithms.expectimax import expectimax


# ===================== HELPER FUNCTIONS =====================

def get_valid_cols(board):
    return [c for c in range(len(board[0])) if board[0][c] == 0]

def random_search(board):
    valid = get_valid_cols(board)
    if not valid: return 0, None
    return 0, random.choice(valid)

def get_next_turn(board):
    count_1 = count_2 = empty = 0
    for row in board:
        for cell in row:
            if cell == 1:   count_1 += 1
            elif cell == 2: count_2 += 1
            else:           empty   += 1
    if empty == 0: return None
    delta = count_1 - count_2
    if abs(delta) > 1: return None
    return 1 if delta <= 0 else 2

def is_terminal(board, turn):
    def c4(a, b, c, d): return a == b == c == d == turn
    rows, cols = len(board), len(board[0])
    for r in range(rows):
        for c in range(cols - 3):
            if c4(board[r][c], board[r][c+1], board[r][c+2], board[r][c+3]): return True
    for r in range(rows - 3):
        for c in range(cols):
            if c4(board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]): return True
    for r in range(rows - 3):
        for c in range(cols - 3):
            if c4(board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]): return True
    for r in range(3, rows):
        for c in range(cols - 3):
            if c4(board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]): return True
    return False

def generate_next_states(board, turn):
    result = []
    rows = len(board)
    for y in range(len(board[0])):
        for x in range(rows - 1, -1, -1):
            if board[x][y] == 0:
                ns = copy.deepcopy(board)
                ns[x][y] = turn
                result.append((ns, y))
                break
    return result

ALGO_MAP = {
    "Minimax":    minimax_search,
    "Alpha-Beta": alpha_beta_search,
    "Expectimax": expectimax,
}

# ===================== LAYOUT (tương đối, không hardcode cửa sổ) =====================

ROWS_B, COLS_B = 6, 7
SQ       = 72
RADIUS   = SQ // 2 - 5
LOG_W    = 260
BOARD_W  = COLS_B * SQ
BOARD_H  = ROWS_B * SQ
HEADER_H = SQ
TOTAL_W  = BOARD_W + LOG_W
TOTAL_H  = HEADER_H + BOARD_H

# Màu
C_BG         = (240, 244, 248)
C_BOARD      = (160, 180, 205)
C_EMPTY      = (255, 255, 255)
C_P1         = (210, 35,  35)
C_P2         = (25,  110, 225)
C_LOG_BG     = (225, 230, 238)
C_LOG_BORDER = (190, 205, 220)
C_TEXT       = (45,  55,  70)
C_TEXT_DIM   = (130, 145, 160)
C_AI_TIME    = (160, 90,  10)
C_HEADER_BG  = (215, 225, 235)
C_BTN        = (200, 215, 235)
C_BTN_HOV    = (170, 190, 215)
C_BTN_TXT    = (45,  55,  70)
C_BTN_SEL    = (80,  130, 200)
C_BTN_SEL_TXT= (255, 255, 255)
C_OVERLAY    = (0,   0,   0,   160)


class ConnectFour:
    def __init__(self, screen_w=1000, screen_h=600, offset_x=None, offset_y=None):
        self.screen_w = screen_w
        self.screen_h = screen_h
        # Căn giữa nếu không truyền offset
        self.ox = offset_x if offset_x is not None else (screen_w - TOTAL_W) // 2
        self.oy = offset_y if offset_y is not None else (screen_h - TOTAL_H) // 2

        self.font_sm = pygame.font.SysFont("segoeui", 13)
        self.font_md = pygame.font.SysFont("segoeui", 14, bold=True)
        self.font_hd = pygame.font.SysFont("segoeui", 17, bold=True)

        self.algorithms = list(ALGO_MAP.keys())
        self.algo_idx   = 0

        # --- Tính tọa độ nút (tuyệt đối trên screen) ---
        lx = self.ox + BOARD_W       # x bắt đầu log panel
        PAD, BTN_H = 10, 28

        total_algo_w = LOG_W - PAD * 2
        algo_btn_w   = (total_algo_w - PAD * 2) // 3
        self.btn_algo_rects = []
        for i in range(3):
            rx = lx + PAD + i * (algo_btn_w + PAD)
            self.btn_algo_rects.append(
                pygame.Rect(rx, self.oy + PAD, algo_btn_w, BTN_H)
            )

        half_w = (total_algo_w - PAD) // 2
        y2 = self.oy + PAD + BTN_H + PAD
        self.btn_start_rect   = pygame.Rect(lx + PAD,                   y2, half_w, BTN_H)
        self.btn_restart_rect = pygame.Rect(lx + PAD + half_w + PAD,    y2, half_w, BTN_H)
        self.btn_help_rect    = pygame.Rect(self.ox + BOARD_W - 36, self.oy + PAD, 26, 26)

        self.info_lines = [
            "Connect 4 — Thử thách trong hành trình!",
            "",
            "Agent (Đỏ)     : dùng thuật toán AI",
            "Enemy Bot (Xanh): đi ngẫu nhiên",
            "",
            "Chọn thuật toán → nhấn [Bắt đầu].",
            "Đánh bại Agent để tiếp tục hành trình.",
            "",
            "Bạn thắng → nhận 'solved', thoát thử thách.",
            "ESC: đóng hộp thoại này.",
        ]

        # Surface riêng để vẽ component — tránh ảnh hưởng nền game
        self._surface = pygame.Surface((TOTAL_W, TOTAL_H))
        self._close_rect = pygame.Rect(0, 0, 0, 0)

        self.reset()

    # ── public interface ─────────────────────────────────────────

    def reset(self):
        self.board        = [[0] * COLS_B for _ in range(ROWS_B)]
        self.game_over    = False
        self.game_started = False
        self.current_turn = 1          # Agent (đỏ) đi trước
        self.is_animating = False
        self.anim_piece   = None
        self.status       = "Chọn thuật toán và ấn Bắt đầu"
        self.log_entries  = []
        self.hover_col    = -1
        self.show_info    = False
        self._agent_won   = False      # cờ để trả về "solved"

    def handle_event(self, event):
        """Trả về 'solved' nếu AGENT thắng (người chơi vượt qua thử thách khi enemy thắng cũng ok — tuỳ bạn đổi)."""
        if self._agent_won:
            return "solved"

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.show_info = False

        if event.type == pygame.MOUSEMOTION:
            mx, my = event.pos
            # Chuyển về tọa độ nội bộ
            lx = mx - self.ox
            ly = my - self.oy
            self.hover_col = lx // SQ if 0 <= lx < BOARD_W and HEADER_H <= ly < HEADER_H + BOARD_H else -1

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mx, my = event.pos

            # Nếu dialog đang mở
            if self.show_info:
                if self._close_rect.collidepoint(mx, my):
                    self.show_info = False
                return

            # Nút ?
            if self.btn_help_rect.collidepoint(mx, my):
                self.show_info = True
                return

            # Nút Chơi lại
            if self.btn_restart_rect.collidepoint(mx, my):
                self.reset()
                return

            if not self.game_started:
                # Chọn thuật toán
                for i, rect in enumerate(self.btn_algo_rects):
                    if rect.collidepoint(mx, my):
                        self.algo_idx = i

                # Bắt đầu
                if self.btn_start_rect.collidepoint(mx, my):
                    self.game_started = True
                    algo = self.algorithms[self.algo_idx]
                    self._add_log(f"=== {algo} vs Enemy Bot ===", C_AI_TIME)
                    self.status = f"Agent ({algo}) đang suy nghĩ..."
                    self._trigger_agent()

        return None

    def draw(self, screen):
        sf = self._surface
        sf.fill(C_BG)

        self._draw_header(sf)
        self._draw_board(sf)
        self._update_anim(sf)
        self._draw_log_panel(sf)
        self._draw_help_btn(sf)

        if self.show_info:
            self._draw_info_dialog(sf)

        # Dán surface lên screen tại offset
        screen.blit(sf, (self.ox, self.oy))

    # ── internal draw ────────────────────────────────────────────

    def _draw_header(self, sf):
        pygame.draw.rect(sf, C_HEADER_BG, (0, 0, BOARD_W, HEADER_H))
        s = self.font_hd.render(self.status, True, C_TEXT)
        sf.blit(s, (12, HEADER_H // 2 - s.get_height() // 2))

        if (self.game_started and not self.game_over
                and not self.is_animating and self.current_turn == 2
                and 0 <= self.hover_col < COLS_B):
            cx = self.hover_col * SQ + SQ // 2
            pygame.draw.circle(sf, C_P2, (cx, HEADER_H // 2), RADIUS, 3)

    def _draw_board(self, sf):
        for r in range(ROWS_B):
            for c in range(COLS_B):
                x, y = c * SQ, HEADER_H + r * SQ
                pygame.draw.rect(sf, C_BOARD, (x, y, SQ, SQ))
                cx, cy = x + SQ // 2, y + SQ // 2
                val = self.board[r][c]
                col = C_EMPTY if val == 0 else (C_P1 if val == 1 else C_P2)
                pygame.draw.circle(sf, col, (cx, cy), RADIUS)
                if val == 0:
                    pygame.draw.circle(sf, C_BOARD, (cx, cy), RADIUS, 2)

    def _draw_log_panel(self, sf):
        lx = BOARD_W
        pygame.draw.rect(sf, C_LOG_BG,    (lx, 0, LOG_W, TOTAL_H))
        pygame.draw.line(sf, C_LOG_BORDER, (lx, 0), (lx, TOTAL_H), 1)
        mouse_abs = pygame.mouse.get_pos()
        # chuyển về tọa độ nội bộ
        mouse = (mouse_abs[0] - self.ox, mouse_abs[1] - self.oy)

        PAD, BTN_H = 10, 28
        total_algo_w = LOG_W - PAD * 2
        algo_btn_w   = (total_algo_w - PAD * 2) // 3

        # 3 nút thuật toán (tọa độ nội bộ)
        for i, name in enumerate(self.algorithms):
            rx   = lx + PAD + i * (algo_btn_w + PAD)
            rect = pygame.Rect(rx, PAD, algo_btn_w, BTN_H)
            hov  = rect.collidepoint(mouse) and not self.game_started
            sel  = (i == self.algo_idx)
            self._btn(sf, rect, name, hov, selected=sel, disabled=self.game_started)

        half_w = (total_algo_w - PAD) // 2
        y2 = PAD + BTN_H + PAD
        r_start   = pygame.Rect(lx + PAD,                  y2, half_w, BTN_H)
        r_restart = pygame.Rect(lx + PAD + half_w + PAD,   y2, half_w, BTN_H)
        self._btn(sf, r_start,   "Bắt đầu",
                  r_start.collidepoint(mouse) and not self.game_started,
                  disabled=self.game_started)
        self._btn(sf, r_restart, "Chơi lại",
                  r_restart.collidepoint(mouse))

        log_top = r_start.bottom + 10
        pygame.draw.line(sf, C_LOG_BORDER, (lx+6, log_top), (lx+LOG_W-6, log_top), 1)
        t = self.font_md.render("Các nước đã đi", True, C_TEXT)
        sf.blit(t, (lx + 8, log_top + 4))

        y0     = log_top + 24
        line_h = 17
        max_ln = (TOTAL_H - y0 - 4) // line_h
        for i, (text, color) in enumerate(self.log_entries[-max_ln:]):
            words, cur, lines = text.split(" "), "", []
            for w in words:
                tt = cur + w + " "
                if self.font_sm.size(tt)[0] > LOG_W - 18:
                    lines.append(cur); cur = w + " "
                else:
                    cur = tt
            lines.append(cur)
            for j, ln in enumerate(lines):
                s = self.font_sm.render(ln, True, color)
                sf.blit(s, (lx + 8, y0 + i * line_h + j * line_h))

    def _draw_help_btn(self, sf):
        # tọa độ nội bộ: góc phải header của board
        r = pygame.Rect(BOARD_W - 36, PAD := 8, 26, 26)
        mouse = (pygame.mouse.get_pos()[0] - self.ox, pygame.mouse.get_pos()[1] - self.oy)
        hov = r.collidepoint(mouse)
        pygame.draw.rect(sf, C_BTN_HOV if hov else C_BTN, r, border_radius=5)
        pygame.draw.rect(sf, C_LOG_BORDER, r, 1, border_radius=5)
        s = self.font_md.render("?", True, C_BTN_TXT)
        sf.blit(s, s.get_rect(center=r.center))

    def _draw_info_dialog(self, sf):
        pad, lh, dw = 18, 20, 360
        dh = pad * 2 + len(self.info_lines) * lh + 40
        dx = (TOTAL_W - dw) // 2
        dy = (TOTAL_H - dh) // 2

        ov = pygame.Surface((TOTAL_W, TOTAL_H), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 140))
        sf.blit(ov, (0, 0))

        pygame.draw.rect(sf, C_HEADER_BG,  (dx, dy, dw, dh), border_radius=10)
        pygame.draw.rect(sf, C_LOG_BORDER, (dx, dy, dw, dh), 1, border_radius=10)

        for i, line in enumerate(self.info_lines):
            s = self.font_sm.render(line, True, C_TEXT if line else C_TEXT_DIM)
            sf.blit(s, (dx + pad, dy + pad + i * lh))

        cr_local = pygame.Rect(dx + dw // 2 - 50, dy + dh - 32, 100, 24)
        mouse = (pygame.mouse.get_pos()[0] - self.ox, pygame.mouse.get_pos()[1] - self.oy)
        hov = cr_local.collidepoint(mouse)
        pygame.draw.rect(sf, C_BTN_HOV if hov else C_BTN, cr_local, border_radius=5)
        s = self.font_sm.render("Đã hiểu [ESC]", True, C_BTN_TXT)
        sf.blit(s, s.get_rect(center=cr_local.center))

        # Lưu close_rect theo tọa độ tuyệt đối để detect click
        self._close_rect = pygame.Rect(
            cr_local.x + self.ox, cr_local.y + self.oy,
            cr_local.w, cr_local.h
        )

    def _btn(self, sf, rect, text, hov, selected=False, disabled=False):
        if disabled:
            bg, fg = (210, 215, 220), (160, 165, 170)
        elif selected:
            bg, fg = C_BTN_SEL, C_BTN_SEL_TXT
        else:
            bg, fg = (C_BTN_HOV if hov else C_BTN), C_BTN_TXT
        pygame.draw.rect(sf, bg,         rect, border_radius=6)
        pygame.draw.rect(sf, C_LOG_BORDER, rect, 1, border_radius=6)
        surf = self.font_md.render(text, True, fg)
        sf.blit(surf, surf.get_rect(center=rect.center))

    # ── animation ────────────────────────────────────────────────

    def _update_anim(self, sf):
        if not self.is_animating or not self.anim_piece: return
        p = self.anim_piece
        p["speed"]     += 3.0
        p["current_y"] += p["speed"]
        if p["current_y"] >= p["target_y"]:
            self.board[p["target_row"]][p["col"]] = p["player"]
            self.is_animating = False
            self.anim_piece   = None
            self._check_end(p["player"])
        else:
            color = C_P1 if p["player"] == 1 else C_P2
            pygame.draw.circle(sf, color,
                               (p["col"] * SQ + SQ // 2, int(p["current_y"])), RADIUS)

    def _start_drop(self, col, player):
        for r in range(ROWS_B - 1, -1, -1):
            if self.board[r][col] == 0:
                self.is_animating = True
                self.anim_piece = {
                    "col": col, "player": player,
                    "current_y":  float(HEADER_H // 2),
                    "target_y":   float(HEADER_H + r * SQ + SQ // 2),
                    "target_row": r, "speed": 16.0,
                }
                return

    # ── game logic ───────────────────────────────────────────────

    def _add_log(self, text, color=C_TEXT):
        self.log_entries.append((text, color))

    def _check_end(self, last_player):
        if is_terminal(self.board, last_player):
            if last_player == 1:
                self.status  = "Agent (Đỏ) THẮNG — vượt thử thách THÀNH CÔNG!"
                self._agent_won = True          # → handle_event sẽ trả "solved"
            else:
                self.status  = "Enemy Bot (Xanh) thắng!"
            self.game_over = True
            winner = "Agent (Đỏ)" if last_player == 1 else "Enemy Bot (Xanh)"
            self._add_log(f"--- KẾT THÚC: {winner} thắng! ---", C_AI_TIME)
            return

        nxt = get_next_turn(self.board)
        if nxt is None:
            self.status    = "Hòa!"
            self.game_over = True
            self._add_log("--- KẾT THÚC: Hòa! ---", C_AI_TIME)
            return

        self.current_turn = nxt
        if nxt == 1:
            self.status = f"Agent ({self.algorithms[self.algo_idx]}) đang suy nghĩ..."
            self._trigger_agent()
        else:
            self.status = "Enemy Bot đang chọn nước..."
            self._trigger_enemy()

    def _trigger_agent(self):
        threading.Thread(target=self._agent_worker, daemon=True).start()

    def _agent_worker(self):
        algo_name = self.algorithms[self.algo_idx]
        fn = ALGO_MAP[algo_name]
        t0 = time.time()
        score, col = fn(self.board)
        elapsed = time.time() - t0
        if col is None:
            valid = get_valid_cols(self.board)
            col = valid[0] if valid else None
        if col is None: return
        move_num = sum(c != 0 for row in self.board for c in row) + 1
        self._add_log(f"#{move_num} Agent → cột {col+1}", C_P1)
        self._add_log(f"  [{algo_name}] score={score:.2f} | {elapsed:.3f}s", C_AI_TIME)
        self._start_drop(col, 1)

    def _trigger_enemy(self):
        threading.Thread(target=self._enemy_worker, daemon=True).start()

    def _enemy_worker(self):
        time.sleep(0.8)
        _, col = random_search(self.board)
        if col is None: return
        move_num = sum(c != 0 for row in self.board for c in row) + 1
        self._add_log(f"#{move_num} Enemy Bot → cột {col+1}", C_P2)
        self._start_drop(col, 2)

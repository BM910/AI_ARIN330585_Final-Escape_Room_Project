import pygame 
import copy
import threading
import time
from algorithms.backtracking_and_ac_3 import backtracking_and_ac_3_search
from algorithms.min_conflict import min_conflict
from algorithms.backtracking_and_forwardcheck import backtracking_forwardcheck_search
from screen.resume import ResumeScreen

WIDTH, HEIGHT = 1000, 600

PANEL_W = 160
LOG_W   = 280
GRID_X  = PANEL_W + 20
GRID_SIZE = min(HEIGHT - 40, WIDTH - PANEL_W - LOG_W - 40)
CELL    = GRID_SIZE // 9
GRID_Y  = (HEIGHT - GRID_SIZE) // 2

PANEL_RECT      = pygame.Rect(8, 8, PANEL_W - 16, HEIGHT - 16)
PANEL_BG        = (255, 255, 255)
PANEL_BORDER    = (200, 200, 192)

COLOR_AC3   = (70,  130, 180)
COLOR_MC    = (100, 160, 80)
COLOR_FC    = (180, 110, 60)
COLOR_SOLVE = (80,  80,  180)

LOG_BG          = (22,  26,  30)
LOG_BORDER      = (50,  55,  60)
LOG_HEADER_COL  = (100, 200, 120)
LOG_LINE_COL    = (50,  60,  55)
LOG_TEXT_OK     = (140, 210, 140)
LOG_TEXT_ERR    = (220, 100, 80)
LOG_LINE_H      = 16

MENU_BTN_BG     = (40,  44,  48)
MENU_BTN_FG     = (180, 180, 180)

FONT_BTN    = ("segoeui", 14)
FONT_TITLE  = ("segoeui", 16)
FONT_NUM    = ("consolas", CELL // 2)
FONT_MONO   = ("consolas", 12)

STATUS_OK_COL   = (50,  160, 80)
STATUS_FAIL_COL = (160, 80,  80)
TIMER_COL       = (200, 160, 60)


class Sudoku:
    def __init__(self, board):
        self.start_board = copy.deepcopy(board)
        self.board = copy.deepcopy(board)

        self.solution_button = pygame.Rect(0, 0, 1, 1)
        self.mc_button       = pygame.Rect(0, 0, 1, 1)
        self.ac_3_button     = pygame.Rect(0, 0, 1, 1)
        self.fc_button       = pygame.Rect(0, 0, 1, 1)
        self.resume_button   = pygame.Rect(0, 0, 1, 1)

        self.resume    = ResumeScreen()
        self.is_resume = False
        self.log       = []

        self.selected_algo = None  
        self.is_solving    = False
        self.confirm_button = pygame.Rect(0, 0, 0, 0)

        self.log_scroll    = 0
        self._solve_start  = 0.0  
        self._last_elapsed = None 

    def is_goal(self):
        board = self.board

        for r in board:
            nums = [x for x in r if x != 0]
            if len(nums) != 9 or len(nums) != len(set(nums)):
                return False

        for c in range(9):
            nums = [board[r][c] for r in range(9) if board[r][c] != 0]
            if len(nums) != 9 or len(nums) != len(set(nums)):
                return False

        for i in range(3):
            for j in range(3):
                nums = [
                    board[r + 3*i][c + 3*j]
                    for r in range(3)
                    for c in range(3)
                    if board[r + 3*i][c + 3*j] != 0
                ]
                if len(nums) != 9 or len(nums) != len(set(nums)):
                    return False

        return True

    def reset(self):
        self.board         = copy.deepcopy(self.start_board)
        self.is_resume     = False
        self.is_solving    = False
        self.selected_algo = None
        self.log           = []
        self.log_scroll    = 0
        self._solve_start  = 0.0
        self._last_elapsed = None

    def return_game(self):
        self.is_resume = False

    def exit(self):
        self.is_resume = False
        return "start"

    def draw(self, screen):
        screen.fill((245, 245, 240))

        font_num   = pygame.font.SysFont(*FONT_NUM)
        font_btn   = pygame.font.SysFont(*FONT_BTN)
        font_title = pygame.font.SysFont(*FONT_TITLE, bold=True)
        font_mono  = pygame.font.SysFont(*FONT_MONO)

        for r in range(9):
            for c in range(9):
                x    = GRID_X + c * CELL
                y    = GRID_Y + r * CELL
                rect = pygame.Rect(x, y, CELL, CELL)

                box_shade = (230, 230, 220) if (r // 3 + c // 3) % 2 == 0 else (245, 245, 240)
                pygame.draw.rect(screen, box_shade, rect)
                pygame.draw.rect(screen, (180, 180, 170), rect, 1)

                val       = self.board[r][c]
                start_val = self.start_board[r][c]
                if val != 0:
                    color = (30, 30, 30) if start_val != 0 else (30, 100, 200)
                    surf  = font_num.render(str(val), True, color)
                    screen.blit(surf, surf.get_rect(center=rect.center))

        for i in range(4):
            lw = 3 if i % 3 == 0 else 1
            pygame.draw.line(screen, (80, 80, 70),
                            (GRID_X, GRID_Y + i * CELL * 3),
                            (GRID_X + GRID_SIZE, GRID_Y + i * CELL * 3), lw)
            pygame.draw.line(screen, (80, 80, 70),
                            (GRID_X + i * CELL * 3, GRID_Y),
                            (GRID_X + i * CELL * 3, GRID_Y + GRID_SIZE), lw)

        pygame.draw.rect(screen, PANEL_BG,     PANEL_RECT, border_radius=10)
        pygame.draw.rect(screen, PANEL_BORDER, PANEL_RECT, 1, border_radius=10)

        title = font_title.render("Thuat toan", True, (50, 50, 50))
        screen.blit(title, (18, 20))

        buttons = [
            ("ac_3_button", "Backtrack+AC3", COLOR_AC3),
            ("mc_button",   "Min-Conflict",   COLOR_MC),
            ("fc_button",   "Forward Check",  COLOR_FC),
        ]
        btn_y = 52
        for attr, label, color in buttons:
            r = pygame.Rect(14, btn_y, PANEL_W - 28, 34)
            setattr(self, attr, r)
            pygame.draw.rect(screen, color, r, border_radius=6)
            algo_map = {"ac_3_button": "ac3", "mc_button": "mc", "fc_button": "fc"}
            if self.selected_algo == algo_map.get(attr):
                pygame.draw.rect(screen, (255, 220, 50), r, 3, border_radius=6)
            t = font_btn.render(label, True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=r.center))
            btn_y += 44

        pygame.draw.rect(screen, (210, 210, 205),
                        pygame.Rect(14, btn_y, PANEL_W - 28, 1))
        btn_y += 12

        sol_r = pygame.Rect(14, btn_y, PANEL_W - 28, 34)
        self.solution_button = sol_r
        pygame.draw.rect(screen, COLOR_SOLVE, sol_r, border_radius=6)
        t = font_btn.render("Giai", True, (255, 255, 255))
        screen.blit(t, t.get_rect(center=sol_r.center))
        btn_y += 44

        if self.is_goal() and not self.is_solving:
            confirm_r = pygame.Rect(14, btn_y, PANEL_W - 28, 34)
            self.confirm_button = confirm_r
            pygame.draw.rect(screen, (50, 160, 80), confirm_r, border_radius=6)
            t = font_btn.render("Xac nhan!", True, (255, 255, 255))
            screen.blit(t, t.get_rect(center=confirm_r.center))
        else:
            self.confirm_button = pygame.Rect(0, 0, 0, 0)

        if self.is_solving:
            # Đang chạy: đếm lên
            elapsed = time.perf_counter() - self._solve_start
            timer_str = f"{elapsed:.2f}s" if elapsed < 60 else f"{int(elapsed//60)}m {elapsed%60:.1f}s"
            t = font_btn.render(timer_str, True, TIMER_COL)
            screen.blit(t, t.get_rect(centerx=PANEL_W // 2, y=HEIGHT - 64))
        else:
            if self._last_elapsed is not None:
                ms = self._last_elapsed
                time_str = f"{ms/1000:.2f}s" if ms >= 1000 else f"{ms:.1f}ms"
                t = font_btn.render(time_str, True, TIMER_COL)
                screen.blit(t, t.get_rect(centerx=PANEL_W // 2, y=HEIGHT - 64))

            if self.is_goal():
                s = font_btn.render("Da giai!", True, STATUS_OK_COL)
            else:
                s = font_btn.render("Chua giai...", True, STATUS_FAIL_COL)
            screen.blit(s, s.get_rect(centerx=PANEL_W // 2, y=HEIGHT - 44))

        log_x    = GRID_X + GRID_SIZE + 20
        log_rect = pygame.Rect(log_x, 8, LOG_W - 12, HEIGHT - 16)
        pygame.draw.rect(screen, LOG_BG,     log_rect, border_radius=10)
        pygame.draw.rect(screen, LOG_BORDER, log_rect, 1, border_radius=10)

        resume_r = pygame.Rect(log_x + LOG_W - 46, 14, 32, 32)
        self.resume_button = resume_r
        pygame.draw.rect(screen, MENU_BTN_BG, resume_r, border_radius=6)
        t = font_btn.render("=", True, MENU_BTN_FG)
        screen.blit(t, t.get_rect(center=resume_r.center))

        hdr = font_mono.render("// log", True, LOG_HEADER_COL)
        screen.blit(hdr, (log_x + 10, 18))
        pygame.draw.line(screen, LOG_LINE_COL,
                        (log_x + 6, 34), (log_x + LOG_W - 18, 34), 1)

        max_lines = (HEIGHT - 55) // LOG_LINE_H
        total     = len(self.log)
        log_text_max_w = LOG_W - 32

        self.log_scroll = max(0, min(self.log_scroll, max(0, total - max_lines)))

        start   = total - max_lines - self.log_scroll
        end     = total - self.log_scroll if self.log_scroll > 0 else total
        visible = self.log[max(0, start):end]

        for i, entry in enumerate(visible):
            col  = LOG_TEXT_OK if not entry.startswith("!") else LOG_TEXT_ERR
            text = entry
            while font_mono.size(text)[0] > log_text_max_w and len(text) > 0:
                text = text[:-1]
            t = font_mono.render(text, True, col)
            screen.blit(t, (log_x + 10, 42 + i * LOG_LINE_H))

        if total > max_lines:
            track_h = HEIGHT - 55
            thumb_h = max(20, track_h * max_lines // total)
            thumb_y = 42 + (track_h - thumb_h) * (total - max_lines - self.log_scroll) // max(1, total - max_lines)
            pygame.draw.rect(screen, (60, 65, 70),
                            pygame.Rect(log_x + LOG_W - 18, 42, 6, track_h), border_radius=3)
            pygame.draw.rect(screen, (120, 130, 120),
                            pygame.Rect(log_x + LOG_W - 18, thumb_y, 6, thumb_h), border_radius=3)

        if self.is_resume:
            self.resume.draw(screen)

    def handle_event(self, event):
        if self.is_resume:
            result = self.resume.handle_event(event)
            if result == "return_game":
                self.return_game()
            elif result == "reset":
                self.reset()
            elif result == "exit":
                return self.exit()
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.is_resume = True

        if event.type == pygame.MOUSEWHEEL:
            log_x = GRID_X + GRID_SIZE + 20
            log_rect = pygame.Rect(log_x, 8, LOG_W - 12, HEIGHT - 16)
            if log_rect.collidepoint(pygame.mouse.get_pos()):
                self.log_scroll = max(0, self.log_scroll + event.y)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.resume_button.collidepoint(event.pos):
                self.is_resume = True

            elif self.mc_button.collidepoint(event.pos):
                self.selected_algo = "mc"
                self.log.append("Da chon: Min-Conflict")

            elif self.ac_3_button.collidepoint(event.pos):
                self.selected_algo = "ac3"
                self.log.append("Da chon: Backtrack+AC3")

            elif self.fc_button.collidepoint(event.pos):
                self.selected_algo = "fc"
                self.log.append("Da chon: Forward Check")

            elif self.solution_button.collidepoint(event.pos):
                if self.selected_algo is None:
                    self.log.append("! Chua chon thuat toan")
                elif not self.is_solving:
                    algo = self.selected_algo
                    self.is_solving    = True
                    self._solve_start  = time.perf_counter()

                    def run():
                        t0 = time.perf_counter()
                        if algo == "mc":
                            self.log.append("--- Min-Conflict ---")
                            result = min_conflict(self.board, self.log)
                        elif algo == "ac3":
                            self.log.append("--- Backtrack+AC3 ---")
                            result = backtracking_and_ac_3_search(self.board, self.log)
                        elif algo == "fc":
                            self.log.append("--- Forward Check ---")
                            result = backtracking_forwardcheck_search(self.board, self.log)

                        elapsed_ms = (time.perf_counter() - t0) * 1000
                        self._last_elapsed = elapsed_ms
                        if result:
                            self.board = result
                            self.log.append(f"Xong! {elapsed_ms:.1f} ms")
                        else:
                            self.log.append(f"! That bai. {elapsed_ms:.1f} ms")
                        self.is_solving = False

                    threading.Thread(target=run, daemon=True).start()

            elif self.confirm_button.collidepoint(event.pos):
                if self.is_goal() and not self.is_solving:
                    return "solved"
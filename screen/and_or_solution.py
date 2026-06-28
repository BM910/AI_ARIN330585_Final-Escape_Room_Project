import pygame
import copy
from algorithms.and_or import and_or_search
from screen.draw_helpers import draw_cell, draw_robot 

CELL_SIZE     = 60
WIDTH, HEIGHT = 1000, 600
PANEL_L       = 180
PANEL_R       = 380
PANEL_MID_W   = WIDTH - PANEL_L - PANEL_R

BG         = (22,  22,  32)
PANEL_BG   = (32,  32,  48)
LOG_BG     = (28,  28,  42)
BTN_IDLE   = (60,  80, 140)
BTN_HOVER  = (80, 110, 190)
BTN_TEXT   = (230, 230, 255)
LOG_TEXT   = (180, 230, 180)
LOG_STEP   = (120, 180, 255)


class _Btn:
    def __init__(self, rect, label):
        self.rect  = pygame.Rect(rect)
        self.label = label

    def draw(self, screen, font):
        color = BTN_HOVER if self.rect.collidepoint(pygame.mouse.get_pos()) else BTN_IDLE
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        txt = font.render(self.label, True, BTN_TEXT)
        screen.blit(txt, txt.get_rect(center=self.rect.center))

    def clicked(self, event):
        return (event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
                and self.rect.collidepoint(event.pos))


class AndOrSolution:
    def __init__(self, node):
        self.start_node = copy.deepcopy(node)
        self.node       = copy.deepcopy(node)

        self.solution   = None
        self.path       = []
        self.step_index = 0
        self.running    = False
        self.done       = False
        self.log        = []
        self.log_scroll = 0

        self.branches        = []
        self.branch_index    = 0
        self.branch_node     = None

        bx, bw = 20, PANEL_L - 40
        self.btn_solve  = _Btn((bx,  80, bw, 42), "Solve")
        self.btn_step   = _Btn((bx, 150, bw, 42), "Step")
        self.btn_run    = _Btn((bx, 220, bw, 42), "Run")
        self.btn_reset  = _Btn((bx, 310, bw, 42), "Reset")
        self.btn_back   = _Btn((bx, 390, bw, 42), "Back")
        self._btns      = [self.btn_solve, self.btn_step,
                           self.btn_run,   self.btn_reset, self.btn_back]

        self.font_btn  = pygame.font.SysFont(None, 26)
        self.font_log  = pygame.font.SysFont("monospace", 15)
        self.font_info = pygame.font.SysFont(None, 24)

    # helper
    def _flat_plan(self, plan):
        if not plan or plan == "failure":
            return []
        if isinstance(plan, dict) and all(isinstance(k, str) for k in plan.keys()):
            return [plan]
        if isinstance(plan, list) and len(plan) == 2:
            action, sub = plan
            if isinstance(sub, dict):
                return [action, sub]
            return [action] + self._flat_plan(sub)
        return []

    def _do_solve(self):
        self.log.append("  Running AND-OR search…")
        self.node         = copy.deepcopy(self.start_node)
        self.step_index   = 0
        self.done         = False
        self.running      = False
        self.branches     = []
        self.branch_index = 0
        self.branch_node  = None

        self.solution = and_or_search(self.start_node.state)

        if not self.solution or self.solution == "failure":
            self.log.append("  No solution found.")
            self.path = []
        else:
            self.path = self._flat_plan(self.solution)
            self.log.append("  Found plan.")

    def _apply_step(self):
        if self.branches:
            branch_path, branch_node, act_label, pos = self.branches[0]
            if branch_path:
                action = branch_path[0]
                self.branches[0] = (branch_path[1:], branch_node, act_label, pos)
                self._move(action)
                self.log.append(f"  [{self.branch_index}] {action:<5}  e={self.node.state.energy}")
            else:
                self.log.append(f"  ✔ Nhánh {act_label} ({pos[0]},{pos[1]}) hoàn thành")
                self.branches.pop(0)
                self.branch_index += 1
                if self.branches:
                    _, next_node, next_act, (nx, ny) = self.branches[0]
                    self.node = copy.deepcopy(next_node)
                    self.log.append(f"  -> Nhánh {next_act}: ({nx},{ny})")
                else:
                    self.branch_node = None
                    if self.step_index < len(self.path):
                        self._apply_step()
                    else:
                        self.done    = True
                        self.running = False
                        self.log.append("  Tất cả nhánh hoàn thành.")
            return

        if not self.path or self.step_index >= len(self.path):
            return

        action = self.path[self.step_index]

        if isinstance(action, dict) and all(isinstance(k, str) for k in action.keys()):
            self.log.append("  Ô '+' — phân nhánh:")
            self.branch_node = copy.deepcopy(self.node)
            self.branches     = []
            self.branch_index = 1

            for act, state_plans in action.items():
                positions = ' | '.join(f"({sk[0]},{sk[1]})" for sk in state_plans.keys())
                self.log.append(f"  {act}: {positions}")
                for state_key, sub_plan in state_plans.items():
                    x, y      = state_key[0], state_key[1]
                    sub_path  = self._flat_plan(sub_plan)
                    branch_start = copy.deepcopy(self.branch_node)
                    branch_start.state.x = x
                    branch_start.state.y = y
                    branch_start.state.energy -= 1
                    bx2, by2 = self.branch_node.state.x, self.branch_node.state.y
                    branch_start.state.map[bx2][by2] = '.'
                    self.branches.append((sub_path, branch_start, act, (x, y)))

            self.branch_index = 1
            self.step_index  += 1
            sub_path, first_node, first_act, (fx, fy) = self.branches[0]
            self.node = copy.deepcopy(first_node)
            self.log.append(f"  → Nhánh {first_act}: ({fx},{fy})")
            return

        if isinstance(action, dict):
            key = self.node.state.get_tuple_no_energy()
            if key not in action:
                self.log.append(" State không khớp nhánh nào.")
                self.done    = True
                self.running = False
                return
            sub_plan   = action[key]
            self.path  = self.path[:self.step_index] + self._flat_plan(sub_plan)
            self._apply_step()
            return

        self._move(action)
        self.step_index += 1
        self.log.append(f"[{self.step_index:02d}] {action:<5}  e={self.node.state.energy}")
        if self.step_index >= len(self.path) and not self.branches:
            self.done    = True
            self.running = False
            self.log.append(" Reached goal.")

    def _move(self, direction):
        dx, dy = {"UP":(-1,0),"DOWN":(1,0),
                  "LEFT":(0,-1),"RIGHT":(0,1)}[direction]
        m  = self.node.state.map
        ks = self.node.state.keys
        x, y   = self.node.state.x, self.node.state.y
        nx, ny = x + dx, y + dy

        if not (0 <= nx < len(m) and 0 <= ny < len(m[0])):
            return
        cell = m[nx][ny]
        if cell == '#':
            return
        if isinstance(cell, str) and cell.isupper() \
                and cell not in ['S','E'] and cell.lower() not in ks:
            return

        if m[x][y] == '+':
            m[x][y] = '.'

        self.node.state.energy -= 1
        self.node.state.x, self.node.state.y = nx, ny

        cell = m[nx][ny]
        if isinstance(cell, int):
            self.node.state.energy += cell
        if isinstance(cell, str) and cell not in ['S','E','@']:
            if cell.islower():   ks.add(cell)
            elif cell.isupper(): ks.discard(cell.lower())
        if cell not in ['S','E','@']:
            m[nx][ny] = '.'
        self.node.state.map  = m
        self.node.state.keys = ks


    def update(self):
        if self.running and not self.done:
            self._apply_step()

    def reset(self):
        self.node         = copy.deepcopy(self.start_node)
        self.solution     = None
        self.path         = []
        self.step_index   = 0
        self.running      = False
        self.done         = False
        self.log          = []
        self.log_scroll   = 0
        self.branches     = []
        self.branch_index = 0
        self.branch_node  = None

    def handle_event(self, event):
        if self.btn_back.clicked(event):
            return "play"
        if self.btn_solve.clicked(event):
            self._do_solve()
        if self.btn_step.clicked(event) and self.solution and not self.done:
            self._apply_step()
        if self.btn_run.clicked(event) and self.solution and not self.done:
            self.running = not self.running
        if self.btn_reset.clicked(event):
            self.reset()

        if event.type == pygame.MOUSEWHEEL:
            if pygame.Rect(WIDTH - PANEL_R, 0, PANEL_R, HEIGHT)\
                    .collidepoint(pygame.mouse.get_pos()):
                line_h     = 18
                visible    = (HEIGHT - 46) // line_h
                max_scroll = max(0, len(self.log) - visible)
                self.log_scroll = max(0, min(max_scroll,
                                             self.log_scroll + event.y))
        return None

    # Phần vẽ giao diện
    def draw(self, screen):
        screen.fill(BG)
        self._draw_left(screen)
        self._draw_matrix(screen)
        self._draw_log(screen)

    def _draw_left(self, screen):
        pygame.draw.rect(screen, PANEL_BG, (0, 0, PANEL_L, HEIGHT))
        title = self.font_btn.render("AND-OR", True, (200, 200, 255))
        screen.blit(title, (20, 30))

        for btn in self._btns:
            btn.draw(screen, self.font_btn)

        if self.solution == "failure" or (self.solution is None and self.log):
            status, sc = "No solution", (255, 100, 100)
        elif self.done:
            status, sc = "Done", (100, 255, 150)
        elif self.solution:
            status, sc = f"{self.step_index}/{len(self.path)}", (200, 200, 255)
        else:
            status, sc = "Not solved", (160, 160, 160)

        screen.blit(self.font_info.render(status, True, sc), (20, 470))
        if self.running:
            screen.blit(
                self.font_info.render("Running", True, (255, 200, 60)),
                (20, 495))


    def _draw_matrix(self, screen):
        gmap = self.node.state.map
        rows, cols = len(gmap), len(gmap[0])

        grid_w = cols * CELL_SIZE
        grid_h = rows * CELL_SIZE
        off_x  = PANEL_L + (PANEL_MID_W - grid_w) // 2
        off_y  = (HEIGHT  - grid_h) // 2

        for r in range(rows):
            for c in range(cols):
                px   = off_x + c * CELL_SIZE
                py   = off_y + r * CELL_SIZE
                rect = (px, py, CELL_SIZE, CELL_SIZE)

                draw_cell(screen, rect, gmap[r][c])

                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        pr = (off_x + self.node.state.y * CELL_SIZE,
              off_y + self.node.state.x * CELL_SIZE,
              CELL_SIZE, CELL_SIZE)
        draw_robot(screen, pr)

        keys_str = ', '.join(sorted(self.node.state.keys)) \
                   if self.node.state.keys else '—'
        info = self.font_info.render(
            f"Energy: {self.node.state.energy}    Keys: {keys_str}",
            True, (220, 220, 220))
        screen.blit(info, (PANEL_L + 10, HEIGHT - 28))


    def _draw_log(self, screen):
        rx = WIDTH - PANEL_R
        pygame.draw.rect(screen, LOG_BG, (rx, 0, PANEL_R, HEIGHT))
        screen.blit(
            self.font_btn.render("Log", True, (200, 200, 255)),
            (rx + 12, 12))
        pygame.draw.line(screen, (60, 60, 90), (rx, 36), (WIDTH, 36), 1)

        line_h     = 18
        visible    = (HEIGHT - 46) // line_h
        total      = len(self.log)
        max_scroll = max(0, total - visible)
        if self.log_scroll > max_scroll:
            self.log_scroll = max_scroll
        start = max(0, total - visible - self.log_scroll)
        end   = start + visible

        for i, line in enumerate(self.log[start:end]):
            if line.startswith("⚡"):
                color = (255, 200,  60)
            elif (line.startswith("  Action") or line.startswith("  UP")
                  or line.startswith("  DOWN") or line.startswith("  LEFT")
                  or line.startswith("  RIGHT")):
                color = (180, 140, 255)
            elif line.startswith("  ✔"):
                color = (100, 255, 150)
            elif line.startswith("  →"):
                color = (255, 160,  80)
            elif line.startswith("  ["):
                color = (120, 180, 255)
            elif line.startswith("["):
                color = (120, 180, 255)
            elif line.startswith("🏁"):
                color = (100, 255, 150)
            elif line.startswith("❌") or line.startswith("⚠️"):
                color = (255, 100, 100)
            elif line.startswith("✅"):
                color = (100, 255, 150)
            else:
                color = LOG_TEXT

            screen.blit(
                self.font_log.render(line, True, color),
                (rx + 8, 44 + i * line_h))

        if total > visible:
            bar_x      = WIDTH - 8
            bar_area_h = HEIGHT - 46
            bar_h      = max(20, bar_area_h * visible // total)
            bar_y      = (44 + (bar_area_h - bar_h)
                          * (max_scroll - self.log_scroll) // max_scroll
                          if max_scroll else 44)
            pygame.draw.rect(screen, (80, 80, 120),
                             (bar_x, 44, 6, bar_area_h), border_radius=3)
            pygame.draw.rect(screen, (160, 160, 220),
                             (bar_x, bar_y, 6, bar_h), border_radius=3)
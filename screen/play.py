import pygame 
import copy
from screen.resume import ResumeScreen
from screen.success import SuccessScreen
from screen.failure import FailureScreen
from screen.sudoku import Sudoku
from screen.connect_4 import ConnectFour          # ← thêm import

from screen.level_1_agent_mode import AIReplayScreen

ROWS, COLS = 6, 6
CELL_SIZE = 80
WIDTH, HEIGHT = 1000, 600

GRID_WIDTH  = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
OFFSET_X = (WIDTH  - GRID_WIDTH)  // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2


class PlayScreen:
    def __init__(self, level, node, board_sudoku=None, board_connect4=None):
        self.level = level
        self.node  = node
        self.start_node = copy.deepcopy(node)

        self.resume_screen = ResumeScreen()
        self.resume_button = pygame.Rect(WIDTH - 60, 10, 45, 45)
        self.is_resume = False

        self.agent_button = pygame.Rect(WIDTH - 220, 10, 145, 45)

        self.success = SuccessScreen(level)
        self.is_success = False

        self.failure = FailureScreen(level)
        self.is_failure = False

        # --- Sudoku ---
        self.sudoku    = None
        self.is_sudoku = False
        if board_sudoku is not None:
            self.sudoku = Sudoku(board_sudoku)

        # --- Connect 4 ---
        self.connect4    = None
        self.is_connect4 = False
        if board_connect4 is not None:
            # Truyền kích thước màn hình để ConnectFour tự căn giữa
            self.connect4 = ConnectFour(screen_w=WIDTH, screen_h=HEIGHT)

        self.list_events = {
            "return_game": self.return_game,
            "reset":       self.reset,
            "exit":        self.exit,
        }

    # ── di chuyển ────────────────────────────────────────────────

    def move(self, direction):
        match direction:
            case 'up':    dx, dy = -1,  0
            case 'down':  dx, dy =  1,  0
            case 'left':  dx, dy =  0, -1
            case 'right': dx, dy =  0,  1

        map_  = self.node.state.map
        keys  = self.node.state.keys
        x, y  = self.node.state.x, self.node.state.y

        if x + dx < 0 or x + dx >= len(map_) or y + dy < 0 or y + dy >= len(map_[0]):
            return

        next_move = map_[x + dx][y + dy]

        if next_move == '#':
            return
        if (isinstance(next_move, str) and next_move.isupper()
                and next_move != 'E' and next_move.lower() not in keys):
            return

        self.node.state.energy -= 1
        self.node.state.x, self.node.state.y = x + dx, y + dy
        self.new_update()

    def new_update(self):
        map_   = self.node.state.map
        keys   = self.node.state.keys
        energy = self.node.state.energy
        x, y   = self.node.state.x, self.node.state.y

        # Kích hoạt Sudoku
        if map_[x][y] == '@':
            if self.sudoku is not None:
                self.is_sudoku = True
            return

        # Kích hoạt Connect 4  ← ký hiệu '$' trên map
        if map_[x][y] == '$':
            if self.connect4 is not None:
                self.connect4.reset()
                self.is_connect4 = True
            return

        if isinstance(map_[x][y], int):
            energy += map_[x][y]

        if isinstance(map_[x][y], str):
            if map_[x][y] not in ['S', 'E']:
                if map_[x][y].islower():
                    keys.add(map_[x][y])
                if map_[x][y].isupper():
                    keys.discard(map_[x][y].lower())

        if map_[x][y] == 'E':
            self.is_success = True

        if energy <= 0:
            self.is_failure = True

        if map_[x][y] not in ['S', 'E', '@', '$']:
            map_[x][y] = '.'

        self.node.state.map    = map_
        self.node.state.keys   = keys
        self.node.state.energy = energy

    # ── handle_event ─────────────────────────────────────────────

    def handle_event(self, event):
        if self.is_resume:
            result = self.resume_screen.handle_event(event)
            if result in self.list_events:
                return self.list_events[result]()
            return

        if self.is_success:
            result = self.success.handle_event(event)
            if result == "reset": self.reset()
            elif result: return result
            return

        if self.is_failure:
            result = self.failure.handle_event(event)
            if result == "reset": self.reset()
            elif result: return result
            return

        # --- Sudoku overlay ---
        if self.is_sudoku:
            result = self.sudoku.handle_event(event)
            if result == "solved":
                x, y = self.node.state.x, self.node.state.y
                self.node.state.map[x][y] = '.'
                self.is_sudoku = False
                self.sudoku.reset()
            elif result == "start":
                return result
            return

        # --- Connect 4 overlay ---
        if self.is_connect4:
            result = self.connect4.handle_event(event)
            if result == "solved":
                # Agent thắng → xoá ô '$', thoát thử thách
                x, y = self.node.state.x, self.node.state.y
                self.node.state.map[x][y] = '.'
                self.is_connect4 = False
                self.connect4.reset()
            return

        # --- Game chính ---
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.collidepoint(event.pos):
                self.is_resume = True
            
            if self.resume_button.collidepoint(event.pos):
                self.is_resume = True
                return

            if self.agent_button.collidepoint(event.pos):
                # Map + energy của level hiện tại (level 1)
                start_map = copy.deepcopy(self.start_node.state.map)
                start_energy = self.start_node.state.energy

                # Mở Agent Mode
                AIReplayScreen(start_map, energy=start_energy).run()
                return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_resume = True
            elif event.key in (pygame.K_UP,    pygame.K_w): self.move('up')
            elif event.key in (pygame.K_DOWN,  pygame.K_s): self.move('down')
            elif event.key in (pygame.K_LEFT,  pygame.K_a): self.move('left')
            elif event.key in (pygame.K_RIGHT, pygame.K_d): self.move('right')

        return None

    # ── reset / navigation ───────────────────────────────────────

    def reset(self):
        self.node        = copy.deepcopy(self.start_node)
        self.is_resume   = False
        self.is_success  = False
        self.is_failure  = False
        self.is_sudoku   = False
        self.is_connect4 = False
        if self.sudoku   is not None: self.sudoku.reset()
        if self.connect4 is not None: self.connect4.reset()

    def return_game(self):
        self.is_resume = False

    def exit(self):
        self.is_resume = False
        return "start"

    def menu(self):
        return "menu level"

    # ── draw ─────────────────────────────────────────────────────

    def draw(self, screen):
        screen.fill((30, 30, 40))

        game_map  = self.node.state.map
        font_cell = pygame.font.SysFont(None, 36)

        for r in range(ROWS):
            for c in range(COLS):
                x = OFFSET_X + c * CELL_SIZE
                y = OFFSET_Y + r * CELL_SIZE
                value = game_map[r][c]

                if value == '.':             color = (220, 220, 220)
                elif value == '#':           color = (40,  40,  40)
                elif isinstance(value, int): color = (80,  200, 120)
                elif value == '$':           color = (200, 80,  180)  # ô Connect 4 — tím
                elif isinstance(value, str) and value.islower(): color = (255, 220, 60)
                elif isinstance(value, str) and value.isupper(): color = (220, 80,  80)
                else:                        color = (160, 160, 160)

                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)

                if value not in ['.']:
                    text = font_cell.render(str(value), True, (0, 0, 0))
                    screen.blit(text, text.get_rect(
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)))

        # Player
        pygame.draw.circle(
            screen, (60, 120, 255),
            (OFFSET_X + self.node.state.y * CELL_SIZE + CELL_SIZE // 2,
             OFFSET_Y + self.node.state.x * CELL_SIZE + CELL_SIZE // 2),
            CELL_SIZE // 3
        )

        # Nút Resume
        pygame.draw.rect(screen, (60, 60, 80), self.resume_button, border_radius=8)
        bx, by = self.resume_button.x, self.resume_button.y
        bw, bh = self.resume_button.width, self.resume_button.height
        bar_w, bar_h = 6, bh - 16
        bar_y = by + 8
        pygame.draw.rect(screen, (230, 230, 230), (bx + bw//2 - 9, bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (230, 230, 230), (bx + bw//2 + 3, bar_y, bar_w, bar_h), border_radius=3)

        # Nút Agent Mode
        pygame.draw.rect(screen, (70, 110, 220), self.agent_button, border_radius=8)
        pygame.draw.rect(screen, (230, 230, 255), self.agent_button, 2, border_radius=8)

        font_agent = pygame.font.SysFont(None, 30)
        agent_text = font_agent.render("Agent Mode", True, (255, 255, 255))
        screen.blit(agent_text, agent_text.get_rect(center=self.agent_button.center))

        # Info bar
        font_info = pygame.font.SysFont(None, 28)
        info = font_info.render(
            f"Energy: {self.node.state.energy}    Keys: {self.node.state.keys}",
            True, (230, 230, 230)
        )
        screen.blit(info, (20, 20))

        # --- Overlay theo thứ tự ưu tiên ---
        if self.is_connect4:
            self.connect4.draw(screen)    # vẽ Connect 4 lên trên game map
            return

        if self.is_sudoku:
            self.sudoku.draw(screen)
            return

        if self.is_resume:
            self.resume_screen.draw(screen)

        if self.is_success:
            self.success.draw(screen)
        elif self.is_failure:
            self.failure.draw(screen)
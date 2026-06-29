import pygame
import copy
import random
from screen.resume import ResumeScreen
from screen.success import SuccessScreen
from screen.failure import FailureScreen
from screen.sudoku import Sudoku
from screen.connect_4 import ConnectFour
from screen.levels_agent_mode import AIReplayScreen
from screen.sensorless_screen import SensorlessReplayScreen
from screen.draw_helpers import draw_cell, draw_robot, draw_key_bar

CELL_SIZE     = 80
WIDTH, HEIGHT = 1000, 600

class PlayScreen:
    def __init__(self, level, node, board_sudoku=None, board_connect4=None):
        self.level      = level
        self.node       = node
        self.start_node = copy.deepcopy(node)

        self.rows     = len(node.state.map)
        self.cols     = len(node.state.map[0])
        self.offset_x = (WIDTH  - self.cols * CELL_SIZE) // 2
        self.offset_y = (HEIGHT - self.rows * CELL_SIZE) // 2

        self.resume_screen = ResumeScreen()
        self.resume_button = pygame.Rect(WIDTH - 60, 10, 45, 45)
        self.is_resume     = False

        self.agent_button  = pygame.Rect(WIDTH - 220, 10, 145, 45)
        self.is_agent_mode = False

        self.success    = SuccessScreen(level)
        self.is_success = False

        self.failure    = FailureScreen(level)
        self.is_failure = False

        # Sudoku
        self.board_sudoku = board_sudoku
        self.sudoku       = None
        self.is_sudoku    = False
        if board_sudoku is not None:
            self.sudoku = Sudoku(board_sudoku)

        # Connect 4
        self.connect4    = None
        self.is_connect4 = False
        if board_connect4 is not None:
            self.connect4 = ConnectFour(screen_w=WIDTH, screen_h=HEIGHT)

        self.list_events = {
            "return_game": self.return_game,
            "reset":       self.reset,
            "exit":        self.exit,
        }


    def move(self, direction):
        match direction:
            case 'up':    dx, dy = -1,  0
            case 'down':  dx, dy =  1,  0
            case 'left':  dx, dy =  0, -1
            case 'right': dx, dy =  0,  1

        map_  = self.node.state.map
        keys  = self.node.state.keys
        x, y  = self.node.state.x, self.node.state.y

        # Ô '+': random hướng
        if map_[x][y] == '+':
            map_[x][y] = '.'
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)
            for rdx, rdy in directions:
                nx, ny = x + rdx, y + rdy
                if not (0 <= nx < len(map_) and 0 <= ny < len(map_[0])):
                    continue
                cell = map_[nx][ny]
                if cell == '#':
                    continue
                if isinstance(cell, str) and cell.isupper() and cell not in ['S', 'E'] and cell.lower() not in keys:
                    continue
                dx, dy = rdx, rdy
                break
            else:
                return

        if x+dx < 0 or x+dx >= len(map_) or y+dy < 0 or y+dy >= len(map_[0]):
            return

        next_move = map_[x+dx][y+dy]
        if next_move == '#':
            return
        if (isinstance(next_move, str) and next_move.isupper()
                and next_move not in ('S', 'E') and next_move.lower() not in keys):
            return

        self.node.state.energy -= 1
        self.node.state.x, self.node.state.y = x+dx, y+dy
        self.new_update()

    def new_update(self):
        map_   = self.node.state.map
        keys   = self.node.state.keys
        energy = self.node.state.energy
        x, y   = self.node.state.x, self.node.state.y

        if map_[x][y] == '@':
            if self.sudoku is not None:
                self.is_sudoku = True
            return

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

        if map_[x][y] not in ['S', 'E', '@', '$', '+']:
            map_[x][y] = '.'

        self.node.state.map    = map_
        self.node.state.keys   = keys
        self.node.state.energy = energy


    def handle_event(self, event):
        if self.is_agent_mode:
            return None

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

        if self.is_sudoku:
            result = self.sudoku.handle_event(event)
            if result == "solved":
                x, y = self.node.state.x, self.node.state.y
                self.node.state.map[x][y] = '.'
                self.is_sudoku = False
                if self.board_sudoku is not None:
                    self.sudoku = Sudoku(self.board_sudoku)
                else:
                    self.sudoku = None
            elif result == "start":
                return result
            return

        if self.is_connect4:
            result = self.connect4.handle_event(event)
            if result == "solved":
                x, y = self.node.state.x, self.node.state.y
                self.node.state.map[x][y] = '.'
                self.is_connect4 = False
                self.connect4.reset()
            return

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.collidepoint(event.pos):
                self.is_resume = True
                return

            if self.level in (1, 2, 3, 4, 5, 6) and self.agent_button.collidepoint(event.pos):
                if self.level in (1, 2, 3, 4, 5):
                    self._open_agent_mode()
                else:
                    return ("and_or", self.start_node)
                return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_resume = True
            elif self.level != 5:
                if event.key in (pygame.K_UP,    pygame.K_w): self.move('up')
                elif event.key in (pygame.K_DOWN,  pygame.K_s): self.move('down')
                elif event.key in (pygame.K_LEFT,  pygame.K_a): self.move('left')
                elif event.key in (pygame.K_RIGHT, pygame.K_d): self.move('right')

        return None

    def _open_agent_mode(self):
        self.is_agent_mode = True
        start_map    = copy.deepcopy(self.start_node.state.map)
        start_energy = self.start_node.state.energy
        if self.level == 5:
            SensorlessReplayScreen(start_map, energy=start_energy).run()
        else:
            algo_map = {
                1: ["BFS", "DFS", "UCS"],
                2: ["Greedy", "A*", "IDA*"],
                3: ["Hill Climbing", "Local Beam", "Simulated Annealing"],
                4: ["Partial Observation"],
            }
            algo_names = algo_map.get(self.level, ["BFS", "DFS", "UCS"])
            AIReplayScreen(start_map, energy=start_energy, algo_names=algo_names).run()

        pygame.display.set_mode((WIDTH, HEIGHT))
        self.is_agent_mode = False

    def reset(self):
        self.node          = copy.deepcopy(self.start_node)
        self.is_resume     = False
        self.is_success    = False
        self.is_failure    = False
        self.is_sudoku     = False
        self.is_connect4   = False
        self.is_agent_mode = False
        if self.board_sudoku is not None:
            self.sudoku = Sudoku(self.board_sudoku)
        else:
            self.sudoku = None
        if self.connect4 is not None:
            self.connect4.reset()

    def return_game(self):
        self.is_resume = False

    def exit(self):
        self.is_resume = False
        return "start"

    def menu(self):
        return "menu level"


    def draw(self, screen):
        if self.is_agent_mode:
            return

        screen.fill((30, 30, 40))

        game_map = self.node.state.map
        for r in range(self.rows):
            for c in range(self.cols):
                px   = self.offset_x + c * CELL_SIZE
                py   = self.offset_y + r * CELL_SIZE
                rect = (px, py, CELL_SIZE, CELL_SIZE)
                draw_cell(screen, rect, game_map[r][c])
                pygame.draw.rect(screen, (0, 0, 0), rect, 1)

        # Robot
        if self.level != 5:
            pr = (self.offset_x + self.node.state.y * CELL_SIZE,
                  self.offset_y + self.node.state.x * CELL_SIZE,
                  CELL_SIZE, CELL_SIZE)
            draw_robot(screen, pr)

        # Nút Resume
        pygame.draw.rect(screen, (60, 60, 80), self.resume_button, border_radius=8)
        bx, by = self.resume_button.x, self.resume_button.y
        bw, bh = self.resume_button.width, self.resume_button.height
        bar_w, bar_h = 6, bh - 16
        bar_y = by + 8
        pygame.draw.rect(screen, (230, 230, 230),
                         (bx + bw//2 - 9, bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(screen, (230, 230, 230),
                         (bx + bw//2 + 3, bar_y, bar_w, bar_h), border_radius=3)

        # Nút Agent Mode
        if self.level in (1, 2, 3, 4, 5, 6):
            pygame.draw.rect(screen, (70, 110, 220), self.agent_button, border_radius=8)
            pygame.draw.rect(screen, (230, 230, 255), self.agent_button, 2, border_radius=8)
            font_agent = pygame.font.SysFont(None, 30)
            agent_text = font_agent.render("Agent Mode", True, (255, 255, 255))
            screen.blit(agent_text, agent_text.get_rect(center=self.agent_button.center))

        # Info bar
        font_info   = pygame.font.SysFont(None, 28)
        energy_surf = font_info.render(
            f"Energy: {self.node.state.energy}    Keys: ",
            True, (230, 230, 230))
        screen.blit(energy_surf, (20, 20))
        if self.node.state.keys:
            draw_key_bar(screen, self.node.state.keys,
                         x=20 + energy_surf.get_width(), y=10, size=28)
        else:
            none_surf = font_info.render("—", True, (230, 230, 230))
            screen.blit(none_surf, (20 + energy_surf.get_width(), 20))

        # Overlays
        if self.is_connect4:
            self.connect4.draw(screen)
            return

        if self.is_sudoku:
            self.sudoku.draw(screen)
            return

        if self.is_resume:
            self.resume_screen.draw(screen)
            return

        if self.is_success:
            self.success.draw(screen)
        elif self.is_failure:
            self.failure.draw(screen)
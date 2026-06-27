import pygame 
import copy
from screen.resume import ResumeScreen
from screen.success import SuccessScreen
from screen.failure import FailureScreen
from screen.sudoku import Sudoku

ROWS, COLS = 6, 6
CELL_SIZE = 80
WIDTH, HEIGHT = 1000, 600

# Tính offset để ma trận nằm giữa màn hình
GRID_WIDTH = COLS * CELL_SIZE
GRID_HEIGHT = ROWS * CELL_SIZE
OFFSET_X = (WIDTH - GRID_WIDTH) // 2
OFFSET_Y = (HEIGHT - GRID_HEIGHT) // 2

class PlayScreen:
    def __init__(self, level, node, board_sudoku=None):
        self.level = level
        self.node = node
        self.start_node = copy.deepcopy(node)

        self.resume_screen = ResumeScreen()
        self.resume_button = pygame.Rect(WIDTH - 60, 10, 45, 45)
        self.is_resume = False

        self.success = SuccessScreen(level)
        self.is_success = False

        self.failure = FailureScreen(level)
        self.is_failure = False

        self.board_sudoku = board_sudoku
        self.sudoku = None
        self.is_sudoku = False
        if board_sudoku is not None:
            self.sudoku = Sudoku(board_sudoku)

        self.list_events = {
            "return_game": self.return_game,
            "reset": self.reset,
            "exit": self.exit
        }

    def move(self, direction):
        match direction:
            case 'up':
                dx, dy = -1, 0 
            case 'down':
                dx, dy = 1, 0
            case 'left':
                dx, dy = 0, -1
            case 'right':
                dx, dy = 0, 1

        map = self.node.state.map 
        keys = self.node.state.keys
        x, y = self.node.state.x, self.node.state.y

        if x + dx < 0 or x + dx >= len(map) or y + dy < 0 or y + dy >= len(map[0]):
            return
        
        next_move = map[x + dx][y + dy]

        if next_move == '#':
            return 
        
        if isinstance(next_move, str) and next_move.isupper() and next_move != 'E' and next_move.lower() not in keys:
            return
        
        self.node.state.energy -= 1
        self.node.state.x, self.node.state.y = x + dx, y + dy

        self.new_update()

    def new_update(self):
        map = self.node.state.map 
        keys = self.node.state.keys
        energy = self.node.state.energy
        x, y = self.node.state.x, self.node.state.y

        if map[x][y] == '@':
            self.is_sudoku = True
            return

        if isinstance(map[x][y], int):
            energy += map[x][y]

        if isinstance(map[x][y], str):
            if map[x][y] not in ['S', 'E']:  # ← thêm điều kiện này
                if map[x][y].islower():
                    keys.add(map[x][y])
                if map[x][y].isupper():
                    keys.discard(map[x][y].lower())

        if map[x][y] == 'E':
            self.is_success = True

        if energy <= 0:
            self.is_failure = True

        if map[x][y] not in ['S', 'E', '@']:     
            map[x][y] = '.'

        self.node.state.map = map 
        self.node.state.keys = keys 
        self.node.state.energy = energy

    def handle_event(self, event):
        if self.is_resume:
            result = self.resume_screen.handle_event(event)
            if result in self.list_events:
                return self.list_events[result]()
            return

        if self.is_success:
            result = self.success.handle_event(event)
            if result == "reset":
                self.reset()
            elif result:
                return result
            return

        if self.is_failure:
            result = self.failure.handle_event(event)
            if result == "reset":
                self.reset()
            elif result:
                return result
            return
        
        if self.is_sudoku:
            result = self.sudoku.handle_event(event)

            if result == "solved":
                x, y = self.node.state.x, self.node.state.y
                self.node.state.map[x][y] = '.'
                self.is_sudoku = False
                self.sudoku = None
                return

            if result == "start":
                return result
            return
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.resume_button.collidepoint(event.pos):
                self.is_resume = True
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.is_resume = True
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                self.move('up')
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                self.move('down')
            elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                self.move('left')
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                self.move('right')

        return None

    def reset(self):
        self.node = copy.deepcopy(self.start_node)
        self.is_resume  = False
        self.is_success = False
        self.is_failure = False
        self.is_sudoku  = False
        if self.board_sudoku is not None:
            self.sudoku = Sudoku(self.board_sudoku)
        else:
            self.sudoku = None

    def return_game(self):
        self.is_resume = False

    def exit(self):
        self.is_resume = False
        return "start"
    
    def menu(self):
        return "menu level"

    def draw(self, screen):
        screen.fill((30, 30, 40))  # Nền tối nhẹ cho dễ nhìn

        game_map = self.node.state.map
        font_cell = pygame.font.SysFont(None, 36)

        for r in range(ROWS):
            for c in range(COLS):
                # Vị trí ô có offset để căn giữa
                x = OFFSET_X + c * CELL_SIZE
                y = OFFSET_Y + r * CELL_SIZE

                value = game_map[r][c]

                if value == '.':
                    color = (220, 220, 220)
                elif value == '#':
                    color = (40, 40, 40)
                elif isinstance(value, int):
                    color = (80, 200, 120)
                elif isinstance(value, str) and value.islower():
                    color = (255, 220, 60)
                elif isinstance(value, str) and value.isupper():
                    color = (220, 80, 80)
                else:
                    color = (160, 160, 160)

                # Ô nền
                pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                # Viền
                pygame.draw.rect(screen, (0, 0, 0), (x, y, CELL_SIZE, CELL_SIZE), 1)

                # Hiển thị nội dung ô
                if value != '.':
                    text = font_cell.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
                    screen.blit(text, text_rect)

        # Vẽ player
        player_x = self.node.state.x
        player_y = self.node.state.y
        pygame.draw.circle(
            screen,
            (60, 120, 255),
            (
                OFFSET_X + player_y * CELL_SIZE + CELL_SIZE // 2,
                OFFSET_Y + player_x * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 3
        )

        # Nút Resume — góc phải trên, hình dấu = xoay 90° (║)
        pygame.draw.rect(screen, (60, 60, 80), self.resume_button, border_radius=8)
        bx, by = self.resume_button.x, self.resume_button.y
        bw, bh = self.resume_button.width, self.resume_button.height
        bar_w, bar_h = 6, bh - 16
        bar_y = by + 8
        # Thanh trái
        pygame.draw.rect(screen, (230, 230, 230), (bx + bw // 2 - 9, bar_y, bar_w, bar_h), border_radius=3)
        # Thanh phải
        pygame.draw.rect(screen, (230, 230, 230), (bx + bw // 2 + 3, bar_y, bar_w, bar_h), border_radius=3)

        # Thanh thông tin — góc trái trên
        font_info = pygame.font.SysFont(None, 28)
        info = font_info.render(
            f"Energy: {self.node.state.energy}    Keys: {self.node.state.keys}",
            True,
            (230, 230, 230)
        )
        screen.blit(info, (20, 20))

        if self.is_sudoku:
            self.sudoku.draw(screen)
            return  

        if self.is_resume:
            self.resume_screen.draw(screen)

        if self.is_success:
            self.success.draw(screen)
        elif self.is_failure:
            self.failure.draw(screen)


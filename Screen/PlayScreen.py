import pygame 
import copy
from Screen.ResumeScreen import ResumeScreen

ROWS, COLS = 6, 6
CELL_SIZE = 50
WIDTH, HEIGHT = 1000, 600

class PlayScreen:
    def __init__(self, level, node):
        self.level = level
        self.node = node
        self.start_node = copy.deepcopy(node)

        self.resume_screen = ResumeScreen()
        self.resume_button = pygame.Rect(WIDTH - 120, HEIGHT - 70, 100, 50)
        self.check_resume = False

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
        energy = self.node.state.energy
        x, y = self.node.state.x, self.node.state.y
        
        if x + dx < 0 or x + dx >= len(map) or y + dy < 0 or y + dy >= len(map[0]):
            return
        
        next_move = map[x + dx][y + dy]

        if next_move == '#':
            return 
        
        if isinstance(next_move, str) and next_move.isupper() and next_move.lower() not in keys:
            return
        
        self.node.state.energy -= 1
        self.node.state.x, self.node.state.y = x + dx, y + dy

        self.new_update()

    def new_update(self):
        map = self.node.state.map 
        keys = self.node.state.keys
        energy = self.node.state.energy
        x, y = self.node.state.x, self.node.state.y

        if isinstance(map[x][y], int):
            energy += map[x][y]

        if isinstance(map[x][y], str):
            if map[x][y] not in ['S', 'E']:
                if map[x][y].islower():
                    keys.append(map[x][y])
                if map[x][y].isupper():
                    keys.remove(map[x][y].lower())
        
        map[x][y] = '.'

        self.node.state.map = map 
        self.node.state.keys = keys 
        self.node.state.energy = energy


    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_resume:
                result = self.resume_screen.handle_event(event)
                if result in self.list_events:
                    return self.list_events[result]()
                return
            
            if self.resume_button.collidepoint(event.pos):
                self.check_resume = True
                
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
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
        self.check_resume = False

    def return_game(self):
        self.check_resume = False

    def exit(self):
        self.check_resume = False
        return "start"

    def draw(self, screen):
        screen.fill((255, 255, 255))

        game_map = self.node.state.map

        font = pygame.font.SysFont(None, 32)

        for r in range(ROWS):
            for c in range(COLS):
                x = c * CELL_SIZE
                y = r * CELL_SIZE

                value = game_map[r][c]

                if value == '.':
                    color = (220, 220, 220)

                elif value == '#':
                    color = (0, 0, 0)

                elif isinstance(value, int):
                    color = (0, 255, 0)

                elif isinstance(value, str) and value.islower():
                    color = (255, 255, 0)

                elif isinstance(value, str) and value.isupper():
                    color = (255, 0, 0)

                else:
                    color = (150, 150, 150)

                # Ô nền
                pygame.draw.rect(
                    screen,
                    color,
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

                # Viền
                pygame.draw.rect(
                    screen,
                    (0, 0, 0),
                    (x, y, CELL_SIZE, CELL_SIZE),
                    1
                )

                # Hiển thị nội dung ô
                if value != '.':
                    text = font.render(str(value), True, (0, 0, 0))
                    text_rect = text.get_rect(
                        center=(x + CELL_SIZE // 2,
                                y + CELL_SIZE // 2)
                    )
                    screen.blit(text, text_rect)

        # Vẽ player
        player_x = self.node.state.x
        player_y = self.node.state.y

        pygame.draw.circle(
            screen,
            (0, 0, 255),
            (
                player_y * CELL_SIZE + CELL_SIZE // 2,
                player_x * CELL_SIZE + CELL_SIZE // 2
            ),
            CELL_SIZE // 3
        )

        pygame.draw.rect(screen, (0, 255, 0), self.resume_button)

        font = pygame.font.SysFont(None, 30)

        info = font.render(
            f"Energy: {self.node.state.energy} | Keys: {self.node.state.keys}",
            True,
            (0, 0, 0)
        )

        screen.blit(info, (350, 20))

        if self.check_resume:
            self.resume_screen.draw(screen)




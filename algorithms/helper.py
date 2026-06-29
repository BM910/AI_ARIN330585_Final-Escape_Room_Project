import copy

# Phần helper cho robot di chuyển thoát khỏi căn phòng
class State:
    def __init__(self, map, x, y, energy, keys):
        self.map = map
        self.x = x
        self.y = y
        self.energy = energy 
        self.keys = keys   

    def get_moves(self):
        moves = []
    
        if self.energy == 0:
            return moves

        move_directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

        # Đang đứng trên '+' -> loạn điều khiển, chỉ check tường
        if self.map[self.x][self.y] == '+':
            for move in move_directions:
                dx, dy = move_directions[move]
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(self.map) and 0 <= ny < len(self.map[0]) and self.map[nx][ny] != '#':
                    moves.append(move)
            return moves  

        # Check nước đi hợp lệ và không gặp tường
        for move in move_directions:
            dx, dy = move_directions[move]
            next_x, next_y = self.x + dx, self.y + dy
            if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != '#':
                moves.append(move)

        # Kiểm tra lại điều kiện trò chơi
        for move in moves[::-1]:
            dx, dy = move_directions[move]
            next_x, next_y = self.x + dx, self.y + dy

            # Gặp boost/ bẫy -> Check lại năng lượng sau đó
            if isinstance(self.map[next_x][next_y], int):
                if self.energy - 1 + self.map[next_x][next_y] < 0:
                    moves.remove(move)

            # Nếu là nước đi bình thường, khóa hoặc cổng 
            elif isinstance(self.map[next_x][next_y], str):
                    # Vị trí bắt đầu hoặc xuất phát phải được loại bỏ
                    if self.map[next_x][next_y] in ['S', 'E']:
                        pass
                    
                    # Gặp cổng phải kiểm tra có khóa không
                    elif self.map[next_x][next_y].isupper() and self.map[next_x][next_y].lower() not in self.keys:
                        moves.remove(move)

        return moves

    def is_at_goal(self):
        return self.map[self.x][self.y] == 'E'
    
    def get_tuple_representation(self):
        # Trả về một đại diện dạng tuple
        flat_map = tuple(tuple(row) for row in self.map)
        return (self.x, self.y, self.energy, tuple(sorted(list(self.keys))), flat_map)
        

class Node:
    def __init__(self, state, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        

def generate_new_state(state, move):
    if move not in state.get_moves():
        return None

    map, x, y, energy, keys = copy.deepcopy(state.map), state.x, state.y, state.energy, copy.deepcopy(state.keys)

    move_directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    next_x = x + move_directions[move][0]
    next_y = y + move_directions[move][1]

    # Đang đứng trên ô '+' -> loạn điều khiển, trả về list
    if map[x][y] == '+':
        result_states = []
        map[x][y] = '.'  # xóa '+' khi rời đi

        for dx, dy in move_directions.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] != '#':
                result_states.append(State(copy.deepcopy(map), nx, ny, energy - 1, copy.deepcopy(keys)))
            else:
                # Gặp tường → đứng yên tại '+'
                result_states.append(State(copy.deepcopy(map), x, y, energy - 1, copy.deepcopy(keys)))

        return result_states  # list

    # Bước vào ô '+' -> đứng yên tại đó, giữ '+' để bước sau loạn
    if map[next_x][next_y] == '+':
        x, y = next_x, next_y
        energy -= 1
        return State(map, x, y, energy, keys)  # 1 state bình thường

    # Logic cũ giữ nguyên
    x, y = next_x, next_y
    energy -= 1

    if isinstance(map[x][y], int):
        energy += map[x][y]
        map[x][y] = '.'
    elif isinstance(map[x][y], str) and map[x][y].islower():
        keys.add(map[x][y])
        map[x][y] = '.'

    return State(map, x, y, energy, keys)

def find_start_position(map):
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == "S":
                return (row, col)
    return

def get_result_path(node: Node):
    node_list = []

    curr = node
    while curr.parent:
        node_list.append(curr)
        curr = curr.parent
    node_list.append(curr)

    node_list.reverse()
    return node_list


# Phần helper cho connect-4
def get_next_turn(board):
    count_1 = 0
    count_2 = 0
    empty  = 0

    for row in board:
        for cell in row:
            if cell == 1:
                count_1 += 1
            elif cell == 2:
                count_2 += 1
            else:
                empty += 1

    if empty == 0:
        return None

    delta = count_1 - count_2
    if abs(delta) > 1:
        return None
    if delta <= 0:
        return 1
    return 2


def evaluate_if_max_depth(board):
    turn = 1
    enemy = 2

    def evaluate_4_cells(window):
        w = list(window)
        if w.count(turn) == 3 and w.count(0) == 1:
            return 5
        if w.count(turn) == 2 and w.count(0) == 2:
            return 2
        if w.count(enemy) == 3 and w.count(0) == 1:
            return -4
        return 0

    rows, cols = len(board), len(board[0])
    score = 0

    for r in range(rows):
        for c in range(cols - 3):
            score += evaluate_4_cells(board[r][c:c+4])

    for c in range(cols):
        col_array = [board[r][c] for r in range(rows)]
        for r in range(rows - 3):
            score += evaluate_4_cells(col_array[r:r+4])

    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r+i][c+i] for i in range(4)]
            score += evaluate_4_cells(window)

    for r in range(rows - 3):
        for c in range(cols - 3):
            window = [board[r+3-i][c+i] for i in range(4)]
            score += evaluate_4_cells(window)

    return score


def is_terminal(board, turn):
    def check_4(a, b, c, d):
        return a == b == c == d == turn

    rows, cols = len(board), len(board[0])

    for r in range(rows):
        for c in range(cols - 3):
            if check_4(board[r][c], board[r][c+1], board[r][c+2], board[r][c+3]):
                return True

    for r in range(rows - 3):
        for c in range(cols):
            if check_4(board[r][c], board[r+1][c], board[r+2][c], board[r+3][c]):
                return True

    for r in range(rows - 3):
        for c in range(cols - 3):
            if check_4(board[r][c], board[r+1][c+1], board[r+2][c+2], board[r+3][c+3]):
                return True

    for r in range(3, rows):
        for c in range(cols - 3):
            if check_4(board[r][c], board[r-1][c+1], board[r-2][c+2], board[r-3][c+3]):
                return True

    return False


def generate_next_states(board, turn):
    result = []
    rows = len(board)

    for y in range(len(board[0])):
        for x in range(rows - 1, -1, -1):  
            if board[x][y] == 0:            
                new_state = copy.deepcopy(board)
                new_state[x][y] = turn
                result.append((new_state, y))
                break                     

    return result
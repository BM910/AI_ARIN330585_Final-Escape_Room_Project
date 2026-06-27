import copy

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

def minimax_search(board):
    turn = get_next_turn(board)
    max_depth = 7

    if turn is None:
        return None

    if turn == 1:
        return max_value(board, 0, max_depth)
    return min_value(board, 0, max_depth)


def max_value(board, depth, max_depth):
    if is_terminal(board, 2):
        return -10000, None
    if is_terminal(board, 1):
        return 10000, None

    if depth == max_depth:
        return evaluate_if_max_depth(board), None 

    best_val, best_pos = float('-inf'), None

    for next_state, pos in generate_next_states(board, 1):
        val, _ = min_value(next_state, depth + 1, max_depth)

        if val > best_val:
            best_val, best_pos = val, pos

    return best_val, best_pos


def min_value(board, depth, max_depth):
    if is_terminal(board, 1):
        return 10000, None
    if is_terminal(board, 2):
        return -10000, None

    if depth == max_depth:
        return evaluate_if_max_depth(board), None

    best_val, best_pos = float('inf'), None

    for next_state, pos in generate_next_states(board, 2):
        val, _ = max_value(next_state, depth + 1, max_depth)

        if val < best_val:
            best_val, best_pos = val, pos

    return best_val, best_pos
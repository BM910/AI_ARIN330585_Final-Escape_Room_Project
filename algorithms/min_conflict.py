import random

def cell_conflict(r, c, board):
    conflict = 0
    val = board[r][c]

    for i in range(9):
        if i != c and board[r][i] == val:
            conflict += 1

    for i in range(9):
        if i != r and board[i][c] == val:
            conflict += 1

    r_board = (r // 3) * 3
    c_board = (c // 3) * 3

    for i in range(3):
        for j in range(3):
            if (r_board + i != r or c_board + j != c) and board[r_board + i][c_board + j] == val:
                conflict += 1

    return conflict

def list_cell_conflict(board, avaiable):
    cells = []
    for r in range(9):
        for c in range(9):
            if (r, c) not in avaiable and cell_conflict(r, c, board) > 0:
                cells.append((r, c))
    return cells

def total_conflict(board):
    total = 0
    for r in range(9):
        for c in range(9):
            total += cell_conflict(r, c, board)
    return total

def cell_with_max_conflict(list_conflict, board):
    max_conf = max(cell_conflict(r, c, board) for r, c in list_conflict)
    
    # Lấy tất cả ô cùng conflict cao nhất
    best_cells = [(r, c) for r, c in list_conflict if cell_conflict(r, c, board) == max_conf]
    
    # Chọn ngẫu nhiên trong số đó để tránh bị kẹt
    return random.choice(best_cells)


def min_conflict(board, avaiable):
    # Gán giá trị ngẫu nhiên cho các ô không cố định
    for r in range(9):
        for c in range(9):
            if (r, c) not in avaiable:
                board[r][c] = random.choice(range(1, 10))

    MAXSTEP = 1000000

    for step in range(MAXSTEP):
        if total_conflict(board) == 0:
            print("Giải xong!")
            return board

        list_conflict = list_cell_conflict(board, avaiable)

        if not list_conflict:
            break

        r, c = cell_with_max_conflict(list_conflict, board)

        best_conflict = float('inf')
        best_vals = []

        for i in range(1, 10):
            board[r][c] = i
            curr = cell_conflict(r, c, board)
            if curr < best_conflict:
                best_conflict = curr
                best_vals = [i]
            elif curr == best_conflict:
                best_vals.append(i)

        board[r][c] = random.choice(best_vals)

    print("Không tìm được lời giải!")
    return None
import random

def get_avaiable(board):
    result = set()
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                result.add((r,c))
    return result

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
    scored = [(cell_conflict(r, c, board), r, c) for r, c in list_conflict]  # chỉ 1 lần
    max_conf = max(scored, key=lambda x: x[0])[0]
    best_cells = [(r, c) for conf, r, c in scored if conf == max_conf]
    return random.choice(best_cells)


def min_conflict(board, log=None):
    avaiable = get_avaiable(board)

    for r in range(9):
        for c in range(9):
            if (r, c) not in avaiable:
                board[r][c] = random.choice(range(1, 10))

    MAXSTEP = 100000

    if log is not None:
        log.append("Min-Conflict bắt đầu...")

    for step in range(MAXSTEP):
        total = total_conflict(board)
        if total == 0:
            if log is not None:
                log.append(f"✔ Giải xong! ({step} buoc)")
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

        if log is not None and step % 500 == 0:
            log.append(f"Step {step}: cf={total}")

    if log is not None:
        log.append("! Khong tim duoc loi giai")
    return None
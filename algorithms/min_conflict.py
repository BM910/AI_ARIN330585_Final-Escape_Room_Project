import random
import time

def get_fixed_cells(board):
    result = set()
    for r in range(9):
        for c in range(9):
            if board[r][c] != 0:
                result.add((r, c))
    return result


def cell_conflict(r, c, board):
    val = board[r][c]
    conflicts = set()

    for i in range(9):
        if i != c and board[r][i] == val:   # kiểm tra cột
            conflicts.add((r, i))
        if i != r and board[i][c] == val:   #  kiểm tra hàng
            conflicts.add((i, c))

    # kiểm tra block 3x3
    r_board = (r // 3) * 3
    c_board = (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if (r_board + i != r or c_board + j != c) and board[r_board + i][c_board + j] == val:
                conflicts.add((r_board + i, c_board + j))

    return len(conflicts)


def get_list_conflict(board, fixed_cells):
    cells = []
    for r in range(9):
        for c in range(9):
            if (r, c) not in fixed_cells and cell_conflict(r, c, board) > 0:
                cells.append((r, c))
    return cells


def min_conflict(board, log=None):
    fixed_cells = get_fixed_cells(board)
    MAXSTEP = 100000
    RESTART_AFTER = 500

    if log is not None:
        log.append("Min-Conflict bắt đầu...")

    restart_count = 0

    while True:
        # phép gán ban đầu
        for r in range(9):
            for c in range(9):
                if (r, c) not in fixed_cells:
                    board[r][c] = random.randint(1, 9)

        best_conflict_count = len(get_list_conflict(board, fixed_cells))
        no_improve = 0

        for step in range(MAXSTEP):
            list_conflict = get_list_conflict(board, fixed_cells)
            
            # phép gán đã là solution
            if not list_conflict:
                if log is not None:
                    log.append(f"✔ Giải xong! (restart={restart_count}, step={step})")
                return board

            # phát hiện kẹt
            current_conflict_count = len(list_conflict)
            if current_conflict_count < best_conflict_count:
                best_conflict_count = current_conflict_count
                no_improve = 0
            else:
                no_improve += 1

            if no_improve >= RESTART_AFTER:
                restart_count += 1
                if log is not None:
                    log.append(f"! Restart #{restart_count} | conflicts={current_conflict_count}")
                break

            # chọn ngẫu nhiên 1 ô đang bị mâu thuẫn
            r, c = random.choice(list_conflict)

            # tìm giá trị tốt nhất cho ô đó
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

            chosen = random.choice(best_vals)
            board[r][c] = chosen

            if log is not None and step % 100 == 0:
                log.append(f"Step {step:5d} | set ({r},{c}) = {chosen} | remaining conflicts={current_conflict_count}")
                time.sleep(0.01)
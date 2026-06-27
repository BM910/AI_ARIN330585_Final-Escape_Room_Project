def get_csp(matrix):
    """Trích xuất biến và miền giá trị ban đầu từ ma trận Sudoku."""
    vars = []
    val_in_rows   = [set() for _ in range(9)]
    val_in_cols   = [set() for _ in range(9)]
    val_in_blocks = [set() for _ in range(9)]

    for i in range(9):
        for j in range(9):
            if not isinstance(matrix[i][j], int) or matrix[i][j] == 0:
                vars.append((i, j))
            else:
                val_in_rows[i].add(matrix[i][j])
                val_in_cols[j].add(matrix[i][j])
                val_in_blocks[(i // 3) * 3 + j // 3].add(matrix[i][j])

    domain = {}
    full_values = set(range(1, 10))
    for i, j in vars:
        block_idx = (i // 3) * 3 + (j // 3)
        domain[(i, j)] = list(full_values - val_in_rows[i] - val_in_cols[j] - val_in_blocks[block_idx])

    return vars, domain


def is_neighbor(var1, var2):
    x1, y1 = var1
    x2, y2 = var2
    if x1 == x2 and y1 == y2:
        return False
    if x1 == x2 or y1 == y2:
        return True
    if (x1 // 3) * 3 + (y1 // 3) == (x2 // 3) * 3 + (y2 // 3):
        return True
    return False


def forward_check(var, value, vars, domain, assignment):
    """
    Sau khi gán value cho var, loại value khỏi miền của mọi biến
    chưa gán mà là hàng xóm của var.
    Trả về dict {biến: [giá trị đã xóa]} để có thể hoàn tác,
    hoặc None nếu có biến nào bị miền rỗng.
    """
    pruned = {}
    for neighbor in vars:
        if neighbor in assignment or not is_neighbor(var, neighbor):
            continue
        if value in domain[neighbor]:
            domain[neighbor].remove(value)
            pruned.setdefault(neighbor, []).append(value)
            if not domain[neighbor]:
                return None   # miền rỗng → nhánh này thất bại
    return pruned


def restore(pruned, domain):
    """Hoàn tác các giá trị đã bị xóa bởi forward checking."""
    for var, values in pruned.items():
        domain[var].extend(values)


def backtrack(vars, domain, assignment):
    if len(assignment) == len(vars):
        return assignment

    # MRV: chọn biến chưa gán có miền nhỏ nhất
    unassigned = [v for v in vars if v not in assignment]
    var = min(unassigned, key=lambda v: len(domain[v]))

    for value in list(domain[var]):
        assignment[var] = value

        # Forward checking: loại value khỏi hàng xóm
        pruned = forward_check(var, value, vars, domain, assignment)

        if pruned is not None:
            result = backtrack(vars, domain, assignment)
            if result is not None:
                return result

        # Backtrack: hoàn tác gán và pruning
        restore(pruned or {}, domain)
        del assignment[var]

    return None


def backtracking_forwardcheck_search(matrix):
    vars, domain = get_csp(matrix)

    result = backtrack(vars, domain, {})
    if result is None:
        return None

    for (x, y), val in result.items():
        matrix[x][y] = val

    return matrix


# --- Test ---
if __name__ == "__main__":
    import copy

    sudoku = [
        [5, 3, 0,  0, 7, 0,  0, 0, 0],
        [6, 0, 0,  1, 9, 5,  0, 0, 0],
        [0, 9, 8,  0, 0, 0,  0, 6, 0],

        [8, 0, 0,  0, 6, 0,  0, 0, 3],
        [4, 0, 0,  8, 0, 3,  0, 0, 1],
        [7, 0, 0,  0, 2, 0,  0, 0, 6],

        [0, 6, 0,  0, 0, 0,  2, 8, 0],
        [0, 0, 0,  4, 1, 9,  0, 0, 5],
        [0, 0, 0,  0, 8, 0,  0, 7, 9],
    ]

    solution = backtracking_forwardcheck_search(copy.deepcopy(sudoku))

    if solution:
        print("Giải thành công!")
        for row in solution:
            print(row)
    else:
        print("Không tìm được lời giải.")
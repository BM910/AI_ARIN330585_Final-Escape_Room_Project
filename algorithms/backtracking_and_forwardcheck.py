import time


def get_csp(matrix):
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


def forward_check(var, value, vars, domain, assignment, log=None):
    pruned = {}
    for neighbor in vars:
        if neighbor in assignment or not is_neighbor(var, neighbor):
            continue
        if value in domain[neighbor]:
            domain[neighbor].remove(value)
            pruned.setdefault(neighbor, []).append(value)
            if log is not None:
                nr, nc = neighbor
                log.append(f"  ({nr},{nc}) loại {value}: còn {sorted(domain[neighbor])}")
            if not domain[neighbor]:
                if log is not None:
                    log.append(f"  ({nr},{nc}) domain rỗng")
                return None
    return pruned


def restore(pruned, domain):
    for var, values in pruned.items():
        domain[var].extend(values)


def backtrack(vars, domain, assignment, step_count, matrix, log=None):
    if len(assignment) == len(vars):
        return assignment

    unassigned = [v for v in vars if v not in assignment]
    var = min(unassigned, key=lambda v: len(domain[v]))
    r, c = var

    if log is not None:
        log.append(f" ({r},{c}) domain={sorted(domain[var])}")

    for value in list(domain[var]):
        assignment[var] = value
        step_count[0] += 1
        matrix[r][c] = value

        if log is not None:
            log.append(f"  Đặt ({r},{c})={value} [b{step_count[0]}]")

        time.sleep(0.01)

        pruned = forward_check(var, value, vars, domain, assignment, log)

        if pruned is not None:
            result = backtrack(vars, domain, assignment, step_count, matrix, log)
            if result is not None:
                return result

        if log is not None:
            log.append(f"  lùi ({r},{c})={value}")

        restore(pruned or {}, domain)
        matrix[r][c] = 0
        del assignment[var]

    return None


def backtracking_forwardcheck_search(matrix, log=None):
    if log is not None:
        log.append("ForwardCheck bắt đầu...")

    vars, domain = get_csp(matrix)

    if log is not None:
        log.append(f" Có {len(vars)} ô trống")
        for var in vars:
            if len(domain[var]) > 1:
                r, c = var
                log.append(f"  ({r},{c}): {sorted(domain[var])}")

    step_count = [0]
    result = backtrack(vars, domain, {}, step_count, matrix, log)

    if result is None:
        if log is not None:
            log.append("Không tìm được lời giải")
        return None

    if log is not None:
        log.append(f"Giải xong! ({step_count[0]} bước)")

    for (x, y), val in result.items():
        matrix[x][y] = val

    return matrix
from collections import deque

def get_csp(matrix):
    vars = []
    val_in_rows = [set() for _ in range(9)]
    val_in_cols = [set() for _ in range(9)]
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
        allowed_values = full_values - val_in_rows[i] - val_in_cols[j] - val_in_blocks[block_idx]
        domain[(i, j)] = list(allowed_values)
    
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


def rm_inconsistent_values(var1, var2, domain):
    removed = False
    
    if len(domain[var2]) == 1:
        val_to_remove = domain[var2][0]
        if val_to_remove in domain[var1]:
            domain[var1].remove(val_to_remove)
            removed = True
            
            if not domain[var1]:
                return None
                
    return removed


def ac_3(matrix, log=None):
    vars, domain = get_csp(matrix)
    arcs_queue = deque()

    for var1 in vars:
        for var2 in vars:
            if is_neighbor(var1, var2):
                arcs_queue.append((var1, var2))

    pruned = 0
    while arcs_queue:
        var1, var2 = arcs_queue.popleft()
        if log is not None:
            r1, c1 = var1
            r2, c2 = var2
            log.append(f"Xét cung ({r1},{c1}) - ({r2},{c2})")
        is_rm = rm_inconsistent_values(var1, var2, domain)
        
        if is_rm == True:
            pruned += 1
            if log is not None:
                r, c = var1
                log.append(f"Cập nhật ({r},{c}): {sorted(domain[var1])}")
            for var_k in vars:
                if is_neighbor(var1, var_k):
                    arcs_queue.append((var_k, var1))
        elif is_rm is None:
            if log is not None:
                log.append(f"Các giá trị {var1} đều thỏa")
            return None

    if log is not None:
        log.append(f"AC3 xong, cắt {pruned} giá trị")
        for var in vars:
            if len(domain[var]) > 1:
                r, c = var
                log.append(f"  ({r},{c}): {sorted(domain[var])}")

    return vars, domain


def backtrack(vars, domain, assignment, matrix, log=None):
    if len(assignment) == len(vars):
        return assignment
    
    unassigned_vars = [v for v in vars if v not in assignment]
    var = min(unassigned_vars, key=lambda v: len(domain[v]))
    r, c = var

    if log is not None:
        log.append(f"({r},{c}) thử {sorted(domain[var])}")

    for value in domain[var]:
        is_valid = True
        for assigned in assignment.keys():
            if is_neighbor(var, assigned) and assignment[assigned] == value:
                is_valid = False
                break
                
        if is_valid:
            assignment[var] = value
            matrix[r][c] = value

            if log is not None:
                log.append(f"  Đặt ({r},{c})={value}")

            import time
            time.sleep(0.01)

            result = backtrack(vars, domain, assignment, matrix, log)
            if result is not None:
                return result

            if log is not None:
                log.append(f"  Lùi ({r},{c})={value}")

            matrix[r][c] = 0
            del assignment[var]
            
    return None


def backtracking_and_ac_3_search(matrix, log=None):
    if log is not None:
        log.append("AC3 bat dau...")

    ac3_result = ac_3(matrix, log)
    if ac3_result is None:
        if log is not None:
            log.append("! AC3 thất bại")
        return None
        
    vars, domain = ac3_result

    if log is not None:
        log.append(f"Backtrack: {len(vars)} ô trống")

    result = backtrack(vars, domain, {}, matrix, log)

    if result is None:
        if log is not None:
            log.append("Không tìm được lời giải")
        return None

    if log is not None:
        log.append(f"Giải xong")

    for x, y in result:
        matrix[x][y] = result[(x, y)]
    
    return matrix
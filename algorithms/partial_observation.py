from helper import Node, State, generate_new_state, find_start_position


# - Quan sát cục bộ 3x3
# - Không có ô năng lượng
# - Có chìa khóa và cửa
# - Những ô chưa từng thấy hiển thị là '?'
# - Belief map khởi đầu toàn '?' trừ vị trí S và E


UNKNOWN = '?'


def get_observation_3x3(actual_map, x, y):
    """Trả về tất cả ô trong vùng 3x3 xung quanh agent (bán kính 1 theo mọi hướng)."""
    visible = {}
    for dx in range(-1, 2):
        for dy in range(-1, 2):
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(actual_map) and 0 <= ny < len(actual_map[0]):
                visible[(nx, ny)] = actual_map[nx][ny]
    return visible


def manhattan(x, y, goal_x, goal_y):
    """Khoảng cách Manhattan từ (x, y) tới đích."""
    return abs(x - goal_x) + abs(y - goal_y)


def lrta_star(actual_map):
    # --- Tìm vị trí S và E ---
    start_x, start_y = find_start_position(actual_map)
    goal_x = goal_y = None
    for r, row in enumerate(actual_map):
        for c, cell in enumerate(row):
            if cell == 'E':
                goal_x, goal_y = r, c

    rows, cols = len(actual_map), len(actual_map[0])

    # --- Belief map: mọi ô đều là '?' trừ S và E ---
    belief_map = [[UNKNOWN for _ in range(cols)] for _ in range(rows)]
    belief_map[start_x][start_y] = 'S'
    belief_map[goal_x][goal_y] = 'E'

    # --- Bảng heuristic heuristics (khởi tạo = Manhattan) ---
    heuristics = {(r, c): manhattan(r, c, goal_x, goal_y)
         for r in range(rows) for c in range(cols)}

    # --- Khởi tạo node đầu ---
    # energy=inf vì không dùng, keys=set() ban đầu
    start_state = State(belief_map, start_x, start_y, float('inf'), set())
    current_node = Node(start_state, parent=None, action=None, cost=0)
    path = [current_node]

    # --- Vòng lặp hành động ---
    while not current_node.state.is_at_goal():
        x, y = current_node.state.x, current_node.state.y

        # Cập nhật belief map: ghi đè các ô trong vùng 3x3 quan sát được
        for (nx, ny), val in get_observation_3x3(actual_map, x, y).items():
            current_node.state.map[nx][ny] = val

        moves = current_node.state.get_moves()
        if not moves:
            print("Agent bị kẹt, không còn nước đi!")
            return None

        # Tính cost dự kiến cho từng nước đi: 1 + heuristics(ô kế tiếp)
        candidates = []
        for action in moves:
            next_state = generate_new_state(current_node.state, action)
            if next_state is None:
                continue
            if isinstance(next_state, list):
                next_state = next_state[0]
            candidates.append((1 + heuristics[(next_state.x, next_state.y)], action, next_state))

        if not candidates:
            print("Không có nước đi hợp lệ!")
            return None

        # Cập nhật heuristic ô hiện tại (bước "học" của LRTA*)
        heuristics[(x, y)] = min(c[0] for c in candidates)

        # Chọn nước đi tốt nhất
        candidates.sort(key=lambda c: c[0])
        _, best_action, best_next = candidates[0]

        # Đồng bộ: chìa khóa đã nhặt → xóa khỏi actual_map
        nx, ny = best_next.x, best_next.y
        if isinstance(actual_map[nx][ny], str) and actual_map[nx][ny].islower():
            actual_map[nx][ny] = '.'

        current_node = Node(best_next, current_node, best_action, current_node.cost + 1)
        path.append(current_node)

    return path


# --- In bản đồ belief (hiển thị '?' cho vùng chưa khám phá) ---
def print_state(state: State):
    for i, row in enumerate(state.map):
        for j, tile in enumerate(row):
            if i == state.x and j == state.y:
                print("*", end=" ")
            elif tile in ('.', 'S'):
                print(" ", end=" ")
            else:
                print(tile, end=" ")
        print()
    print()


if __name__ == "__main__":
    actual_map = [
        ['#', '#', '#', '#', '#', '#', '#'],
        ['#', 'S', '.', '#', '.', 'E', '#'],
        ['#', '.', '#', '#', 'A', '#', '#'],
        ['#', '.', '.', '.', '.', '.', '#'],
        ['#', '#', '#', '.', '.', '.', '#'],
        ['#', 'a', '.', '.', '.', '.', '#'],
        ['#', '#', '#', '#', '#', '#', '#'],
    ]

    print("=== LRTA* - Quan sát cục bộ 3x3 ===\n")
    path = lrta_star(actual_map)

    if path:
        for node in path:
            print_state(node.state)
            print(f"Hành động : {node.action}")
            print(f"Chìa khóa : {node.state.keys}")
            print("-" * 30)
        print(f"\nThành công! Tổng số bước: {len(path) - 1}")
    else:
        print("Thất bại! Không tìm được đường đi.")
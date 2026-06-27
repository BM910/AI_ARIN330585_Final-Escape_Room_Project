from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position

def calculate_manhattan(state: State):
    curr_map = state.map
    for row in range(len(curr_map)):
        for col in range(len(curr_map[0])):
            if curr_map[row][col] == "E":
                return abs(row - state.x) + abs(col - state.y)
    return float("inf")


def simple_hill_climbing(start_map, energy=float("inf")):
    if not start_map:
        return None
    
    # Khởi tạo trạng thái ban đầu
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    current_node = Node(state, parent=None, action=None, cost=0)

    while True:
        if current_node.state.is_at_goal():
            return get_result_path(current_node)
            
        # Tính toán độ tốt (heuristic) của trạng thái hiện tại
        current_h = calculate_manhattan(current_node.state)
        
        moves = current_node.state.get_moves()
        neighbor_moved = False
        
        # DUYỆT TỪNG NƯỚC ĐI (Đặc trưng của Simple Hill Climbing)
        for action in moves:
            next_state = generate_new_state(current_node.state, action)
            if next_state is None:
                continue
                
            # Tính heuristic của trạng thái láng giềng
            neighbor_h = calculate_manhattan(next_state)
            
            # CHỈ CẦN TỐT HƠN TRẠNG THÁI HIỆN TẠI -> CHỌN NGAY VÀ NGẮT VÒNG LẶP
            if neighbor_h < current_h:
                child_node = Node(next_state, current_node, action, current_node.cost + 1)
                current_node = child_node  # Di chuyển sang node mới
                neighbor_moved = True
                break # không tìm kiếm thêm nữa

        # Nếu đã duyệt hết tất cả láng giềng mà không có ô nào tốt hơn -> bị kẹt
        if not neighbor_moved:
            return get_result_path(current_node)
        

# test
if __name__ == "__main__":
    def print_state(state : State):
        for i, row in enumerate(state.map):
            for j, tile in enumerate(row):
                if i == state.x and j == state.y:
                    print("*", end=" ")
                elif tile == "." or tile == "S":
                    print(" ", end=" ")
                else:
                    print(tile, end=" ")
            print()
        print()

    test_map = [
            ['S', '.', '.', '.', '.', '.', '.'],
            ['.', '#', '#', '#', '#', '#', '#'],
            ['.', '.', '#', '.', '.', '.', '.'],
            ['a', '.', 'A', '.', '#', '.', 'E'],
            ['.', '#', '#', '#', '#', '#', '#'],
            ['.', '.', '.', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '.', '.', '.'],
    ]

    node_list = simple_hill_climbing(test_map, energy=30)
    action_list = []
    if node_list:
        for node in node_list:
            action_list.append(node.action)
            print_state(node.state)
            print(f"action: {node.action}  cost: {node.cost}  energy: {node.state.energy}")
            print("-"*20)
        for action in action_list:
            print(action, end=" ")
    else:
        print(node_list)
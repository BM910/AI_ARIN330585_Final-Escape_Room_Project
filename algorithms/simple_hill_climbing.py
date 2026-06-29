from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position

def calculate_manhattan(state: State):
    curr_map = state.map
    for row in range(len(curr_map)):
        for col in range(len(curr_map[0])):
            if curr_map[row][col] == "E":
                return abs(row - state.x) + abs(col - state.y)
    return float("inf")


def simple_hill_climbing(start_map, energy=float("inf")):
    """Thuật toán Simple hill climbing, h(n) = Khoảng cách Manhattan từ Agent đến đích"""
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    current_node = Node(state, parent=None, action=None, cost=0)

    while True:
        if current_node.state.is_at_goal():
            return get_result_path(current_node)
            
        current_h = calculate_manhattan(current_node.state)
        
        moves = current_node.state.get_moves()
        neighbor_moved = False
        
        for action in moves:
            next_state = generate_new_state(current_node.state, action)
            if next_state is None:
                continue
                
            neighbor_h = calculate_manhattan(next_state)
            
            if neighbor_h < current_h:
                child_node = Node(next_state, current_node, action, current_node.cost + 1)
                current_node = child_node 
                neighbor_moved = True
                break 

        if not neighbor_moved:
            return get_result_path(current_node)
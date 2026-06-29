import random, math
from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position

    
def calculate_heuristic(state: State):
    distance_goal, remain_keys = 0, 0
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if not isinstance(state.map[row][col], str):
                continue
            if state.map[row][col] == 'E':
                distance_goal = abs(row - state.x) + abs(col - state.y)
            if state.map[row][col].islower() and state.map[row][col] not in ('.', 's'):
                remain_keys += 1
    return distance_goal + remain_keys * 2
        

def simulated_annealing(start_map, energy=float("inf")):
    """Thuật toán mô phỏng luyện kim, g(n) = Khoảng cách Manhattan tới đích + 2 x Số chìa khóa còn lại, T=90, T_min=1, alpha=0.97"""
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    current_node = Node(state, parent=None, action=None, cost=calculate_heuristic(state))

    # Gán cố định
    T = 90       
    T_min = 1
    alpha = 0.97

    while T > T_min: 
        if current_node.state.is_at_goal():
            return get_result_path(current_node)
        
        moves = current_node.state.get_moves()
        if not moves:
            return get_result_path(current_node)
        
        move = random.choice(moves)
        next_state = generate_new_state(current_node.state, move)
        h_cost_next_state = calculate_heuristic(next_state)

        delta = h_cost_next_state - current_node.cost
        if delta < 0:
            current_node = Node(next_state, current_node, move, h_cost_next_state)
        else:
            p = math.exp(-delta/T)
            if random.uniform(0, 1) < p:
                current_node = Node(next_state, current_node, move, h_cost_next_state)
        
        T *= alpha

    return get_result_path(current_node)
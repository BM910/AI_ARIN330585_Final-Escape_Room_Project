import random, math
from helper import Node, State, generate_new_state, get_result_path

    
def calculate_heuristic(state: State):
    distance_goal, remain_keys = 0, 0
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if state.map[row][col] == 'E':
                distance_goal = abs(row - state.x) + abs(col - state.y)
            if state.map[row][col].lower():
                remain_keys += 1
    return distance_goal + remain_keys * 2
        

def simulated_annealing(initial_state):
    current_node = Node(initial_state, None, None, calculate_heuristic(initial_state))

    T = 90          # Gán cố định
    T_min = 0.01
    alpha = 0.99

    while T > T_min: 
        if current_node.state.is_at_goal():
            return get_result_path(current_node)
        
        moves = current_node.state.get_moves()
        if not moves:
            return None
        
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

    return None

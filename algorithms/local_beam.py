from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position
import random
    
def calculate_heuristic(state: State):
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if state.map[row][col] == 'E':
                return abs(row - state.x) + abs(col - state.y)
            
    return None

def local_beam_search(start_map, energy=float("inf")):
    """Thuật toán Local Beam Search với k = 2"""
    k = 2 
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    node = Node(state, parent=None, action=None, cost=0)

    child_nodes = []
    for action in state.get_moves():
        child_nodes.append(Node(generate_new_state(state, action), node, action, cost=1))

    list_node = list(random.choices(child_nodes, k=k))
    best_node = node

    while list_node:
        for node in list_node:
            if node.state.is_at_goal():
                return get_result_path(node)  
        
        next_list = []
        for node in list_node:
            for action in node.state.get_moves():
                next_state = generate_new_state(node.state, action)
                next_node = Node(next_state, node, action, calculate_heuristic(next_state))
                next_list.append(next_node)

        if not next_list:
            return get_result_path(best_node)

        next_list.sort(key=lambda x : x.cost)
        list_node = next_list[:k]
        best_node = list_node[0]

    return get_result_path(best_node)
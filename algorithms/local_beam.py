from helper import Node, State, generate_new_state, get_result_path

    
def calculate_heuristic(state: State):
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if state.map[row][col] == 'E':
                return abs(row - state.x) + abs(col - state.y)
        
    return None

def local_beam_search(start_state):
    k = 2 
    node = Node(start_state, parent=None, action=None, cost=0)

    list_node = [node]

    while list_node:
        if any(node.state.is_at_goal for node in list_node):
            return  
        
        next_list = []
        for node in list_node:
            for action in node.state.get_moves():
                next_state = generate_new_state(node.state, action)
                next_node = Node(next_state, node, action, calculate_heuristic(next_state))
                next_list.append(next_node)

        if not next_list:
            return None

        next_list.sort(key=lambda x : x.cost)
        list_node = next_list[:k]

    return None

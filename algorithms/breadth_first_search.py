from helper import Node, State, generate_new_state, get_result_path, find_start_position
from collections import deque

def bfs(start_map, energy=float("inf")):
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy)
    node = Node(state, parent=None, action=None, cost=0)

    if state.is_at_goal():
        return get_result_path(node)

    frontier = deque([node])
    reached = set()
    
    reached.add(state.get_tuple_representation())

    while frontier:
        node = frontier.popleft()
    
        moves = node.state.get_moves()
        
        for action in moves:
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
                
            child_node = Node(next_state, node, action, node.cost + 1)

            if child_node.state.is_at_goal():
                return get_result_path(child_node)

            state_tuple = child_node.state.get_tuple_representation()

            if state_tuple not in reached:
                reached.add(state_tuple)
                frontier.append(child_node)

    return None
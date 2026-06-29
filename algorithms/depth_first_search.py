from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position


def get_tuple_representation_no_energy(state):
    flat_map = tuple(tuple(row) for row in state.map)
    return (state.x, state.y, tuple(sorted(list(state.keys))), flat_map)

def is_state_in_frontier(state: State, frontier_set):
    return get_tuple_representation_no_energy(state) in frontier_set

def is_state_in_reached(state: State, reached):
    return get_tuple_representation_no_energy(state) in reached


def dfs_version_2(start_map, energy=float("inf")):
    """Thuật toán dfs cách tiếp cận 2"""
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    node = Node(state, parent=None, action=None, cost=0)

    if node.state.is_at_goal():
        return get_result_path(node)

    frontier = [node]
    frontier_set = {get_tuple_representation_no_energy(node.state)}

    reached = set()

    while frontier:
        node = frontier.pop()
        frontier_set.remove(get_tuple_representation_no_energy(node.state))

        reached.add(get_tuple_representation_no_energy(node.state))
        
        for action in node.state.get_moves():
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
                
            child_node = Node(next_state, node, action, node.cost + 1)

            if not is_state_in_frontier(next_state, frontier_set) and not is_state_in_reached(next_state, reached):
                if child_node.state.is_at_goal():
                    return get_result_path(child_node)

                frontier.append(child_node)
                frontier_set.add(get_tuple_representation_no_energy(child_node.state))

    return None
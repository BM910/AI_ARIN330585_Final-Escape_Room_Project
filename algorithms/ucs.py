from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position

def ucs(start_map, energy=float("inf")):
    """Thuật toán UCS, g(n) = g(parent) + năng lượng hao phí của bước di chuyển"""
    if not start_map:
        return None 
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    node = Node(state, parent=None, action=None, cost=0)
    
    frontier = [node]
    frontier_cost = {node.state.get_tuple_representation() : node.cost}

    reached = {}

    while frontier:
        frontier.sort(key = lambda x : x.cost)

        node = frontier.pop(0)
        state_tuple = node.state.get_tuple_representation()

        if node.state.is_at_goal():
            return get_result_path(node)

        frontier_cost.pop(state_tuple, None)

        reached[state_tuple] = node.cost

        for action in node.state.get_moves():
            next_state = generate_new_state(node.state, action)

            if next_state is None:
                continue

            new_cost = node.cost + (node.state.energy - next_state.energy if node.state.energy > next_state.energy else 0)

            child_node = Node(next_state, parent=node, action=action, cost=new_cost)
            child_state = next_state.get_tuple_representation()

            # Kiểm tra reached
            if child_state in reached and reached[child_state] <= new_cost:
                continue

            # Kiểm tra frontier
            if child_state in frontier_cost and frontier_cost[child_state] <= new_cost:
                continue

            # Nếu có cost tốt hơn thì xóa node cũ
            if child_state in frontier_cost:
                frontier = [
                    n for n in frontier
                    if n.state.get_tuple_representation() != child_state
                ]

            frontier.append(child_node)
            frontier_cost[child_state] = new_cost

    return None
from algorithms.helper import State, Node, generate_new_state, get_result_path, find_start_position

def calculate_heuristic(state: State):
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if state.map[row][col] == 'E':
                return abs(row - state.x) + abs(col - state.y)
    return None

def ida_star(start_map, energy=float("inf")):
    if not start_map:
        return None

    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())

    heuristic_cost = calculate_heuristic(state)
    root = Node(state, parent=None, action=None, cost={
        'g_n': 0, 'h_n': heuristic_cost, 'f_n': heuristic_cost
    })

    threshold = heuristic_cost

    while threshold < 100000:
        min_threshold = float('inf')
        visited = {root.state.get_tuple_no_energy()}
        stack = [root]

        while stack:
            node = stack[-1]

            if node.state.is_at_goal():
                return get_result_path(node)

            next_action = None
            next_state_to_expand = None
            for action in node.state.get_moves():
                next_state = generate_new_state(node.state, action)
                if next_state is None:
                    continue
                if next_state.get_tuple_no_energy() not in visited:
                    next_action = action
                    next_state_to_expand = next_state
                    break

            # Hết action -> backtrack
            if next_action is None:
                stack.pop()
                visited.discard(node.state.get_tuple_no_energy())
                continue

            g_new = node.cost['g_n'] + (
                (node.state.energy - next_state_to_expand.energy)
                if node.state.energy > next_state_to_expand.energy else 0
            )
            h_new = calculate_heuristic(next_state_to_expand)
            f_new = g_new + h_new

            if f_new > threshold:
                if f_new < min_threshold:
                    min_threshold = f_new
                continue

            child_node = Node(next_state_to_expand, node, next_action, {
                'g_n': g_new, 'h_n': h_new, 'f_n': f_new
            })

            visited.add(next_state_to_expand.get_tuple_no_energy())
            stack.append(child_node)

        if min_threshold == float('inf'):
            return None

        threshold = min_threshold

    return None
from helper import Node, State, generate_new_state, get_result_path

def calculate_heuristic(state: State):
    for row in range(len(state.map)):
        for col in range(len(state.map[0])):
            if state.map[row][col] == 'E':
                return abs(row - state.x) + abs(col - state.y)
        
    return None

# Lấy ra node có f(n) nhỏ nhất từ frontier
def pop_min_cost_state(frontier):
    lowest_cost_node = min(frontier.values(), key=lambda node: node.cost['f_n'])

    del frontier[lowest_cost_node.state.get_tuple_representation()]

    return lowest_cost_node

def ida_star(initial_state):
    if not initial_state:
        return None
    
    heuristic_cost = calculate_heuristic(initial_state)
    root = Node(initial_state, parent=None, action=None, cost={'g_n': 0, 'h_n': heuristic_cost, 'f_n': heuristic_cost})
    threshold = heuristic_cost

    while threshold < 100000:
        min_threshold = float('inf')
        frontier = {root.state.get_tuple_representation(): root}
        reached = dict()

        while frontier:
            node = pop_min_cost_state(frontier)

            if node.state.is_at_goal():
                return get_result_path(node)

            reached[node.state.get_tuple_representation()] = node.cost['g_n']
            
            for action in node.state.get_moves():
                next_state = generate_new_state(node.state, action)
                if next_state is None:
                    continue
                
                tuple_state = next_state.get_tuple_representation()
                g_new = node.cost['g_n'] + ((node.state.energy - next_state.energy) if node.state.energy > next_state.energy else 0)
                h_new = calculate_heuristic(next_state)
                f_new = g_new + h_new

                if f_new > threshold:
                    if f_new < min_threshold:
                        min_threshold = f_new
                    continue

                if tuple_state in reached:
                    if g_new >= reached[tuple_state]:
                        continue
                    else:
                        del reached[tuple_state]

                if tuple_state in frontier:
                    node_in_frontier = frontier[tuple_state]
                    if node_in_frontier.cost['g_n'] > g_new:
                        node_in_frontier.cost['g_n'] = g_new
                        node_in_frontier.cost['f_n'] = g_new + node_in_frontier.cost['h_n']
                        node_in_frontier.parent = node
                    continue

                child_node = Node(next_state, node, action, None)
                child_node.cost = {'g_n': g_new, 'h_n': h_new, 'f_n': f_new}
                frontier[tuple_state] = child_node

        threshold = min_threshold

    return None
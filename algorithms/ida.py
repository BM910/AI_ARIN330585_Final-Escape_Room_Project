from helper import Node, State, generate_new_state, get_result_path, find_start_position

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

def ida_star(start_map, energy=float("inf")):
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())

    heuristic_cost = calculate_heuristic(state)
    root = Node(state, parent=None, action=None, cost={'g_n': 0, 'h_n': heuristic_cost, 'f_n': heuristic_cost})
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

# test
if __name__ == "__main__":
    def print_state(state : State):
        for i, row in enumerate(state.map):
            for j, tile in enumerate(row):
                if i == state.x and j == state.y:
                    print("*", end=" ")
                elif tile == "." or tile == "S":
                    print(" ", end=" ")
                else:
                    print(tile, end=" ")
            print()
        print()

    test_map = [
            ['S', '.', '.', '.', '.', '.', '.', ],
            ['.', '#', '#', '#', '#', '#', '.', ],
            ['.', '.', '#', '.', -5 , '.', '.', ],
            ['.', -9 , 'A', 'E', '#', '#', '.', ],
            ['.', '.', '#', '.', '#', '.', '.', ],
            ['.', 'a', '#', '.', '.', '.', '#', ],
            ['#', '#', '#', '#', '#', '#', '#', ],
    ]

    node_list = ida_star(test_map, energy=30)
    action_list = []
    if node_list:
        for node in node_list:
            action_list.append(node.action)
            print_state(node.state)
            print(f"action: {node.action}  cost: {node.cost}  energy: {node.state.energy}")
            print("-"*20)
        for action in action_list:
            print(action, end=" ")
    else:
        print(node_list)
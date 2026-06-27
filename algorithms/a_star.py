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


def a_star(start_map, energy=float("inf")):
    if not start_map:
        return
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    heuristic_cost = calculate_heuristic(state)
    node = Node(state, parent=None, action=None, cost={'g_n': 0, 'h_n': heuristic_cost, 'f_n': heuristic_cost})
    

    frontier = {node.state.get_tuple_representation(): node}

    reached = dict()    # Lưu state dạng tuple và g(n)
    while frontier:
        node = pop_min_cost_state(frontier)

        if node.state.is_at_goal():
            return get_result_path(node)

        reached[node.state.get_tuple_representation()] = node.cost['g_n']      # Lưu biểu diễn dạng tuple kèm g(node)
        
        for action in node.state.get_moves():
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
            
            tuple_state = next_state.get_tuple_representation()
            g_new = node.cost['g_n'] + ((node.state.energy - next_state.energy) if  node.state.energy > next_state.energy else 0)

            if tuple_state in reached:     # Nếu state đã xét và có cost tối ưu hơn --> Xóa trong reached để xét lại
                if g_new >= reached[next_state.get_tuple_representation()]:
                    continue
                else:
                    del reached[next_state.get_tuple_representation()]
            
            if tuple_state in frontier:     # Nếu state trong frontier và có cost tối ưu hơn --> Thay thế node trong frontier
                node_in_frontier = frontier[tuple_state]
                if node_in_frontier.cost['g_n'] > g_new:
                    node_in_frontier.cost['g_n'] = g_new
                    node_in_frontier.cost['f_n'] = g_new + node_in_frontier.cost['h_n']
                    node_in_frontier.parent = node

                continue

            if not tuple_state in frontier and not tuple_state in reached:

                child_node = Node(next_state, node, action, None)
                heuristic_cost = calculate_heuristic(next_state)
                child_node.cost = {'g_n': g_new, 'h_n': heuristic_cost, 'f_n': g_new + heuristic_cost}

                frontier[tuple_state] = child_node

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
            ['S', '.', '.', '.', '.', '.', '.'],
            [-5 , '#', '#', '#', '#', '#', '.'],
            ['a', '#', '.', '.', '.', '.', '.'],
            ['#', '.', '.', '#', '#', '#', 'A'],
            ['a', '.', '#', '.', 'B', '.',  8 ],
            ['b', '.', '.', '.', '#', '.', 'E'],
            ['#', '#', '#', '#', '#', '#', '#']
    ]

    node_list = a_star(test_map, energy=25)
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
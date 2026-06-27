from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position

def ucs(start_map, energy=float("inf")):
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

            # Kiểm tra reached
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
            [-20, '#', '#', '#', '#', '#', '.'],
            ['a', '#', '.', '.', '.', '.', '.'],
            ['#', '.', '.', '#', '#', '#', 'A'],
            ['.', '.', '#', '.', '.', '.', '.'],
            ['.', '.', '.', '.', '#', '.', 'E'],
            ['#', '#', '#', '#', '#', '#', '#']
    ]

    node_list = ucs(test_map, energy=30)
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
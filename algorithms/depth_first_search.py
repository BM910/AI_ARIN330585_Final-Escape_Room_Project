from algorithms.helper import Node, State, generate_new_state, get_result_path, find_start_position


def get_tuple_representation_no_energy(state):
        # Trả về một đại diện dạng tuple
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

        reached.add(get_tuple_representation_no_energy(node.state))      # Lưu biểu diễn dạng tuple
        
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

    node_list = dfs_version_2(test_map, energy=30)
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
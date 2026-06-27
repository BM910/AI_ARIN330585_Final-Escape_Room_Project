from helper import Node, State, generate_new_state, get_result_path, find_start_position
from collections import deque

def bfs(start_map, energy=float("inf")):
    if not start_map:
        return None
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
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

    node_list = bfs(test_map, energy=30)
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
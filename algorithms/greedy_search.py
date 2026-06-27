from helper import Node, State, generate_new_state, get_result_path, find_start_position
import heapq


def calculate_manhattan(state : State):
    map = state.map
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == "E":
                return abs(row - state.x) + abs(col - state.y)
    return float("inf")


def greedy(start_map, energy=float("inf")):
    if not start_map:
        return
    
    x, y = find_start_position(start_map)
    state = State(start_map, x, y, energy, set())
    node = Node(state, parent=None, action=None, cost=0)
    
    counter = 0
    frontier = [(calculate_manhattan(state), counter, node)]
    
    reached = set()
    frontier_set = set()
    frontier_set.add(state.get_tuple_representation())

    reached.add(state.get_tuple_representation())

    while frontier:
        _, _, node = heapq.heappop(frontier)

        if node.state.is_at_goal():
            return get_result_path(node)
    
        node_state_tuple = node.state.get_tuple_representation()
        reached.add(node_state_tuple)
        frontier_set.discard(node_state_tuple)

        moves = node.state.get_moves()
        for action in moves:
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue

            next_state_tuple = next_state.get_tuple_representation()

            if next_state_tuple not in reached and next_state_tuple not in frontier_set:
                child_node = Node(next_state, node, action, node.cost+1)
                counter += 1
                heapq.heappush(frontier, (calculate_manhattan(next_state), counter, child_node))
                frontier_set.add(next_state_tuple)

    return None

# test
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

if __name__ == "__main__":
    test_map = [
            ['#', '#', 'a', '#', '#'],
            ['.',  3 , 'S', 'A', '#'],
            ['#', '#', '.', '#', '#'],
            ['E', '#', '.', '#', '#'],
            ['.', '.', '.', '#', '#'],
    ]

    node_list = greedy(test_map, energy=6)
    for node in node_list:
        print_state(node.state)
        print(f"action: {node.action}")
        print("-"*20)
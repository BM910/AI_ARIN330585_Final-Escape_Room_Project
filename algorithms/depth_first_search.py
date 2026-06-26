from helper import Node, State, generate_new_state, get_result_path


def is_state_in_frontier(state: State, frontier_set):
    return state.get_tuple_representation() in frontier_set

def is_state_in_reached(state: State, reached):
    return state.get_tuple_representation() in reached


def dfs_version_2(initial_state):
    if not initial_state: #Nếu initial_state là None thì không làm gì hết
        return None
    
    # Khởi tạo Node
    node = Node(initial_state, parent=None, action=None, cost=0)
    if node.state.is_at_goal():
        return get_result_path(node)

    frontier = [node]
    frontier_set = {node.state.get_tuple_representation()}

    reached = set()

    while frontier:
        node = frontier.pop()
        frontier_set.remove(node.state.get_tuple_representation())

        reached.add(node.state.get_tuple_representation())      # Lưu biểu diễn dạng tuple
        
        for action in node.state.get_moves():
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
                
            child_node = Node(next_state, node, action, node.cost + 1)

            if not is_state_in_frontier(next_state, frontier_set) and not is_state_in_reached(next_state, reached):
                if child_node.state.is_at_goal():
                    return get_result_path(child_node)

                frontier.append(child_node)
                frontier_set.add(child_node.state.get_tuple_representation())

    return None
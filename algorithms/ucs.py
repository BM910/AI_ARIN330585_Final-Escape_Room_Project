from helper import Node, generate_new_state, get_result_path

def ucs(initial_state):
    if not initial_state:
        return None 
    
    node = Node(initial_state, parent=None, action=None, cost=0)
    
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



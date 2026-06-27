from helper import Node, generate_new_state

def and_or_search(start_state):
    node = Node(start_state, parent=None, action=None, cost=0)
    return or_search(node, [])

def or_search(node, path):
    if node.state.is_at_goal():
        return []
    
    if node.state.get_tuple_representation() in path:
        return 'failure'
    
    for action in node.state.get_moves():
        result = generate_new_state(node.state, action)

        plan = and_search(result, node, path + [node.state.get_tuple_representation])

        if plan != 'failure':
            return [action, plan]
        
    return 'failure'
    
def and_search(result, parent_node, path):
    states = result if isinstance(result, list) else [result]

    plans = {}
    for s in states:
        child_node = Node(s, parent=parent_node, action=None, cost=0)
        plan_s = or_search(child_node, path)

        if plan_s == 'failure':
            return 'failure'

        plans[s.get_tuple_representation()] = plan_s

    # Deterministic → trả về plan trực tiếp thay vì dict 1 phần tử
    if not isinstance(result, list):
        return plans[result.get_tuple_representation()]

    return plans


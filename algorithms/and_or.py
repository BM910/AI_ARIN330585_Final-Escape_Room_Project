from data.Node import Node
from data.State import generate_new_state


def and_or_search(start_state):
    node = Node(start_state, parent=None, action=None, cost=0)
    return or_search(node.state, [])

def or_search(state, path):
    if state.is_at_goal():
        return []
    
    if state.get_tuple_no_energy() in path:
        return 'failure'
    
    # Đang đứng trên '+' -> thu thập plan cho tất cả action
    if state.map[state.x][state.y] == '+':
        all_plans = {}
        for action in state.get_moves():
            result_states = generate_new_state(state, action)
            if result_states is None:
                continue
            plan = and_search(result_states, path + [state.get_tuple_no_energy()])
            if plan != 'failure':
                all_plans[action] = plan
        return all_plans if all_plans else 'failure'

    # Bình thường -> dừng sớm khi tìm được plan
    for action in state.get_moves():
        result_states = generate_new_state(state, action)
        if result_states is None:
            continue
        plan = and_search(result_states, path + [state.get_tuple_no_energy()])
        if plan != 'failure':
            return [action, plan]
        
    return 'failure'
    
def and_search(states, path):
    if not isinstance(states, list):
        states = [states]

    plans = {}
    for s in states:
        plan_s = or_search(s, path)

        if plan_s == 'failure':
            return 'failure'

        plans[s.get_tuple_no_energy()] = plan_s

    if len(states) == 1:
        return plans[states[0].get_tuple_no_energy()]

    return plans
import copy
from helper import Node, State, generate_new_state, get_result_path

    
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


def a_star(initial_state):
    if not initial_state: #Nếu initial_state là None thì không làm gì hết
        return None
    
    # Khởi tạo Node
    heuristic_cost = initial_state.calculate_heuristic()
    node = Node(initial_state, parent=None, action=None, cost={'g_n': 0, 'h_n': heuristic_cost, 'f_n': heuristic_cost})

    frontier = {node.state.get_tuple_representation(): node}    # Cài đặt frontier dạng dict, key = state dạng tuple --> Tìm kiếm dễ dàng

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
                heuristic_cost = next_state.calculate_heuristic()
                child_node.cost = {'g_n': g_new, 'h_n': heuristic_cost, 'f_n': g_new + heuristic_cost}

                frontier[tuple_state] = child_node

    return None
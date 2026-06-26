import copy

class State:
    def __init__(self, map, x, y, energy, keys):
        self.map = map
        self.x = x
        self.y = y
        self.energy = energy 
        self.keys = keys   

    def get_moves(self):
        moves = []
    
        if self.energy == 0:
            return moves

        move_directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

        # Check nước đi hợp lệ và không gặp tường
        for move in move_directions:
            dx, dy = move_directions[move]
            next_x, next_y = self.x + dx, self.y + dy
            if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]) and self.map[next_x][next_y] != '#':
                moves.append(move)

        # Kiểm tra lại điều kiện trò chơi
        for move in moves[::-1]:
            dx, dy = move_directions[move]
            next_x, next_y = self.x + dx, self.y + dy

            # Gặp boost/ bẫy --> Check lại năng lượng sau đó
            if isinstance(self.map[next_x][next_y], int):
                if self.energy - 1 + self.map[next_x][next_y] < 0:
                    moves.remove(move)

            # Nếu là nước đi bình thường, khóa hoặc cổng 
            elif isinstance(self.map[next_x][next_y], str):
                    # Vị trí bắt đầu hoặc xuất phát phải được loại bỏ
                    if self.map[next_x][next_y] in ['S', 'E']:
                        pass
                    
                    # Gặp cổng phải kiểm tra có khóa không
                    elif self.map[next_x][next_y].isupper() and self.map[next_x][next_y].lower() not in self.keys:
                        moves.remove(move)

        return moves

    def is_at_goal(self):
        return self.map[self.x][self.y] == 'E'
    
    def get_tuple_representation(self):
        # Trả về một đại diện dạng tuple
        flat_map = tuple(tuple(row) for row in self.map)
        return (self.x, self.y, self.energy, tuple(sorted(list(self.keys))), flat_map)
    
    
    def calculate_heuristic(self):
        for row in range(len(self.map)):
            for col in range(len(self.map[0])):
                if self.map[row][col] == 'E':
                    return abs(row - self.x) + abs(col - self.y)
        
        return None
        

class Node:
    def __init__(self, state: State, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost
        

def generate_new_state(state, move):
    if move not in state.get_moves():
        return None

    map, x, y, energy, keys = copy.deepcopy(state.map), state.x, state.y, state.energy, copy.deepcopy(state.keys)

    move_directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}
    x, y = x + move_directions[move][0], y + move_directions[move][1]
    energy -= 1     # Mặc định phải trừ, dù đi vào ô năng lượng

    # Gặp năng lượng --> Nhặt
    if isinstance(map[x][y], int):
        energy += map[x][y]
        map[x][y] = '.'

    # Nhặt khóa thì năng lượng vẫn -1
    elif isinstance(map[x][y], str) and map[x][y].islower():
        keys.add(map[x][y])
        map[x][y] = '.'

    return State(map, x, y, energy, keys)


def get_result_path(node: Node):
    path = []

    curr = node
    while curr.parent:
        path.append(curr.action)
        curr = curr.parent

    path.reverse()
    return path

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

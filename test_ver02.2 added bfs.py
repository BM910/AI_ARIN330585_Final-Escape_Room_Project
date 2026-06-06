import copy
from collections import deque

class State:
    def __init__(self, map, x, y, energy, keys):
        self.map = map
        self.x = x # hàng
        self.y = y # cột
        self.energy = energy 
        self.keys = keys   

    def get_moves(self):
        moves = []
        # Không còn năng lượng sẽ cút
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


def print_state(state, move_name="INITIAL STATE"):
    print(f"\n--- {move_name} ---")
    print(f"Vị trí: ({state.x}, {state.y}) | Năng lượng: {state.energy} | Chìa khóa: {state.keys}")
    print("Bản đồ:")
    for row in state.map:
        print("  " + " ".join([str(cell) if isinstance(cell, int) else cell for cell in row]))


def bfs1(initial_state):
    if not initial_state: #Nếu initial_state là None thì không làm gì hết
        return None
    
    # Khởi tạo Node
    node = Node(initial_state, parent=None, action=None, cost=0)

    frontier = deque([node])
    reached = set()
    
    # Lưu biểu diễn dạng tuple
    reached.add(initial_state.get_tuple_representation())

    while frontier:
        node = frontier.popleft()

        if node.state.is_at_goal():
            return node
        
        # moves là một danh sách chuỗi hành động như ['UP', 'DOWN']
        moves = node.state.get_moves()
        
        for action in moves:
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
                
            child_node = Node(next_state, node, action, node.cost + 1)
            state_tuple = child_node.state.get_tuple_representation()

            if state_tuple not in reached:
                reached.add(state_tuple)
                frontier.append(child_node)

    return None


def bfs2(initial_state):
    if not initial_state: #Nếu initial_state là None thì không làm gì hết
        return None
    
    # Khởi tạo Node
    node = Node(initial_state, parent=None, action=None, cost=0)

    frontier = deque([node])
    reached = set()
    
    # Lưu biểu diễn dạng tuple
    reached.add(initial_state.get_tuple_representation())

    while frontier:
        node = frontier.popleft()
        
        # moves là một danh sách chuỗi hành động như ['UP', 'DOWN']
        moves = node.state.get_moves()
        
        for action in moves:
            next_state = generate_new_state(node.state, action)
            if next_state is None:
                continue
                
            child_node = Node(next_state, node, action, node.cost + 1)
            if child_node.state.is_at_goal():
                return child_node
            state_tuple = child_node.state.get_tuple_representation()

            if state_tuple not in reached:
                reached.add(state_tuple)
                frontier.append(child_node)

    return None


# ------- Khu vực test---------


if __name__ == "__main__":
    # Khởi tạo bản đồ test
    # Tại (1, 2) là 'S'. 
    # UP: gặp chìa khóa 'a'
    # DOWN: gặp đường đi '.'
    # LEFT: gặp bình năng lượng +5
    # RIGHT: gặp cửa khóa 'A' (Dự kiến: Sẽ bị loại vì chưa có chìa)
    test_map = [
        ['#', '#', 'a', '#', '#'],
        ['.',  3 , 'S', 'A', '#'],
        ['#', '#', '.', '#', '#'],
        ['E', '#', '.', '#', '#'],
        ['.', '.', '.', '#', '#'],
    ]
    
    # Khởi tạo trạng thái ban đầu: Năng lượng = 5, túi đồ rỗng (dùng set)
    initial_state = State(test_map, 1, 2, 5, keys=set())

    print("\n--- Chạy thử thuật toán BFS tìm đường tới E ---")
    result_node = bfs1(initial_state)
    if result_node:
        path = []
        curr = result_node
        while curr.parent:
            path.append(curr.action)
            curr = curr.parent
        print(f"Tìm thấy đường đi thành công! Các bước đi: {path[::-1]}\n")
    else:
        print("Không tìm thấy đường đi tới đích!")
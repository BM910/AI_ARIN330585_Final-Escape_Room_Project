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
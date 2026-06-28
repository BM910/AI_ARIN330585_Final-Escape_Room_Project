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

        # Đang đứng trên '+' → loạn điều khiển, chỉ check tường
        if self.map[self.x][self.y] == '+':
            for move in move_directions:
                dx, dy = move_directions[move]
                nx, ny = self.x + dx, self.y + dy
                if 0 <= nx < len(self.map) and 0 <= ny < len(self.map[0]) and self.map[nx][ny] != '#':
                    moves.append(move)
            return moves  

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
    
    def get_tuple_no_energy(self):
        flat_map = tuple(tuple(row) for row in self.map)
        return (self.x, self.y, tuple(sorted(list(self.keys))), flat_map)
        

def generate_new_state(state, move):
    if move not in state.get_moves():
        return None

    map, x, y, energy, keys = copy.deepcopy(state.map), state.x, state.y, state.energy, copy.deepcopy(state.keys)
    move_directions = {'UP': (-1, 0), 'DOWN': (1, 0), 'LEFT': (0, -1), 'RIGHT': (0, 1)}

    # Đang đứng trên '+' → trả về list tất cả state có thể xảy ra
    if map[x][y] == '+':
        map[x][y] = '.'  # ô '+' mất sau khi dùng
        results = []
        for dx, dy in move_directions.values():
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(map) and 0 <= ny < len(map[0]) and map[nx][ny] != '#':
                m2 = copy.deepcopy(map)
                k2 = copy.deepcopy(keys)
                e2 = energy - 1
                if isinstance(m2[nx][ny], int):
                    e2 += m2[nx][ny]
                    m2[nx][ny] = '.'
                elif isinstance(m2[nx][ny], str) and m2[nx][ny].islower():
                    k2.add(m2[nx][ny])
                    m2[nx][ny] = '.'
                if e2 > 0:
                    results.append(State(m2, nx, ny, e2, k2))
        return results  # AND node

    # Bình thường → di chuyển theo đúng move
    dx, dy = move_directions[move]
    x, y = x + dx, y + dy
    energy -= 1

    if isinstance(map[x][y], int):
        energy += map[x][y]
        map[x][y] = '.'
    elif isinstance(map[x][y], str) and map[x][y].islower():
        keys.add(map[x][y])
        map[x][y] = '.'

    return State(map, x, y, energy, keys)

def find_start_position(map):
    for row in range(len(map)):
        for col in range(len(map[0])):
            if map[row][col] == "S":
                return (row, col)
    return

def get_result_path(node):
    node_list = []

    curr = node
    while curr.parent:
        node_list.append(curr)
        curr = curr.parent
    node_list.append(curr)

    node_list.reverse()
    return node_list

from data.State import State, generate_new_state


def print_state(state, move_name="INITIAL STATE"):
    print(f"\n--- {move_name} ---")
    print(f"Vị trí: ({state.x}, {state.y}) | Năng lượng: {state.energy} | Chìa khóa: {state.keys}")
    print("Bản đồ:")
    for row in state.map:
        # Format in ra đẹp mắt hơn, đổi int thành str
        print("  " + " ".join([str(cell) if isinstance(cell, int) else cell for cell in row]))



if __name__ == "__main__":
    # Khởi tạo bản đồ test
    # Tại (1, 2) là 'S'. 
    # UP: gặp chìa khóa 'a'
    # DOWN: gặp đường '.'
    # LEFT: gặp bình năng lượng +5
    # RIGHT: gặp cửa khóa 'A' (Dự kiến: Sẽ bị loại vì chưa có chìa)
    test_map = [
        ['#', '#', 'a', '#', '#'],
        ['#',  2 , 'S', 'A', '#'],
        ['#', '#', '.', '#', '#'],
    ]
    
    # Khởi tạo trạng thái ban đầu: Năng lượng = 5, túi đồ rỗng (dùng set)
    initial_state = State(test_map, 1, 2, 5, keys=set())
    
    print_state(initial_state)

    # Lấy danh sách các nước đi hợp lệ
    valid_moves = initial_state.get_moves()
    print(f"\nCác nước đi hợp lệ từ S: {valid_moves}")
    # Dự kiến: ['UP', 'DOWN', 'LEFT']. RIGHT bị loại vì cửa 'A' khóa.

    # Sinh và in ra các trạng thái kế tiếp
    for move in valid_moves:
        next_state = generate_new_state(initial_state, move)
        if next_state:
            print_state(next_state, f"SAU KHI ĐI {move}")
from algorithms.helper import get_next_turn, evaluate_if_max_depth, is_terminal, generate_next_states


def expectimax(board):
    turn = get_next_turn(board)
    max_depth = 5

    if turn is None:
        return None
    
    if turn == 1:
        return max_value_ex(board, 0, max_depth)
    return chance_node(board, 0, max_depth)


def max_value_ex(board, depth, max_depth):
    if is_terminal(board, 2):
        return -10000, None
    if is_terminal(board, 1):
        return 10000, None
    
    if depth == max_depth:
        return evaluate_if_max_depth(board), None 
    
    best_val, best_pos = float('-inf'), None

    for next_state, pos in generate_next_states(board, 1):
        val, _ = chance_node(next_state, depth + 1, max_depth)

        if val > best_val:
            best_val, best_pos = val, pos

    return best_val, best_pos 


def chance_node(board, depth, max_depth):
    if is_terminal(board, 2):
        return -10000, None
    if is_terminal(board, 1):
        return 10000, None
    
    if depth == max_depth:
        return evaluate_if_max_depth(board), None
    
    children = generate_next_states(board, 2)
    if not children:
        return evaluate_if_max_depth(board), None 
    
    total = 0 

    for next_state, _ in children:
        val, _ = max_value_ex(next_state, depth + 1, max_depth)
        total += val 
    
    return total / len(children), None
from algorithms.helper import Node, State, generate_new_state, get_result_path
from collections import deque
import copy

def get_tuple_representation_no_energy(state):
        flat_map = tuple(tuple(row) for row in state.map)
        return (state.x, state.y, tuple(sorted(list(state.keys))), flat_map)

def generate_belief_states(map):
    belief_state_set = []

    rows, cols = len(map), len(map[0])
    initial_energy = rows * cols

    for x in range(rows):
        for y in range(cols):
            if map[x][y] == '.':
                belief_state_set.append(State(map=copy.deepcopy(map), x=x, y=y, energy=float('inf'), keys=set()))

    return belief_state_set


def is_goal_state_set(bs_set):
    if not bs_set:
        return False
    return all(state.is_at_goal() for state in bs_set)


def get_set_representation(state_set):
    return frozenset(get_tuple_representation_no_energy(state) for state in state_set)

def is_state_in_frontier(state_set, frontier_set):
    return get_set_representation(state_set) in frontier_set

def is_state_in_reached(state_set, reached):
    return get_set_representation(state_set) in reached


def sensorless_bfs_version(start_map, energy=float("inf")):
    """Thuật toán BFS dùng trong môi trường không nhìn thấy, biết G không biết S"""
    if not start_map:
        return None
    
    # Sinh ra Belief state và khởi tạo Node
    node = Node(generate_belief_states(start_map), parent=None, action=None, cost=0)
    if is_goal_state_set(node.state):
        return get_result_path(node)

    frontier = deque()
    frontier.append(node)
    frontier_set = {get_set_representation(node.state)}

    reached = set()

    while frontier:
        node = frontier.popleft()
        frontier_set.remove(get_set_representation(node.state))

        reached.add(get_set_representation(node.state))    # Lưu biểu diễn dạng tuple
        
        valid_actions = []
        for state in node.state:
            valid_actions.append(state.get_moves())

        for action in ('UP', 'DOWN', 'LEFT', 'RIGHT'):
            after_states = []
            after_states_set = set()

            for idx in range(len(node.state)):
                
                if node.state[idx].is_at_goal() or action not in valid_actions[idx]:
                    if get_tuple_representation_no_energy(node.state[idx]) not in after_states_set:
                        after_states.append(node.state[idx])
                        after_states_set.add(get_tuple_representation_no_energy(node.state[idx]))
                    else:
                        continue
                if action in valid_actions[idx]:
                    next_state = generate_new_state(node.state[idx], action)
                    if next_state is None:
                        continue
                    if get_tuple_representation_no_energy(next_state) not in after_states_set:
                        after_states.append(next_state)
                        after_states_set.add(get_tuple_representation_no_energy(next_state))
                        
            child_node = Node(after_states, node, action, node.cost + 1)

            if not is_state_in_frontier(after_states, frontier_set) and not is_state_in_reached(after_states, reached):
                if is_goal_state_set(child_node.state):
                    return get_result_path(child_node)

                frontier.append(child_node)
                frontier_set.add(get_set_representation(child_node.state))

    return None
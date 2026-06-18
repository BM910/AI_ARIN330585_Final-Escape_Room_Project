from data.State import State

class Node:
    def __init__(self, state: State, parent, action, cost):
        self.state = state
        self.parent = parent
        self.action = action
        self.cost = cost


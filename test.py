from data.State import State
from screen.simulator import AIReplayScreen




if __name__ == "__main__":
    demo_map = [
        ['S', '.', 'a', '#', 'b', '.'],
        ['#', '.', -5,  'A', '.', '.'],
        ['.', '.', '#', '#', '.', 'B'],
        ['.', 10,  '.', '.', '.', 'E']
    ]

    init_state = demo_map
    app = AIReplayScreen(init_state)
    app.run()
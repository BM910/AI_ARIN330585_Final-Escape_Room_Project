from data.State import State
from screen.sensorless_screen import SensorlessReplayScreen



if __name__ == "__main__":
    demo_map = [
        ['.', '.', '.', '#'],
        ['#', 'a', '.', '.'],
        ['.', '.', 'b', '#'],
        ['.', 'A', 'B', 'E']
    ]

    init_state = demo_map
    app = SensorlessReplayScreen(init_state)
    app.run()
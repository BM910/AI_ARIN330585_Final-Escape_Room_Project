import json
from data.State import State
from data.Node import Node

def load_level(path: str) -> tuple[int, Node]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    level = data["level"]
    s = data["state"]

    state = State(
        map=s["map"],
        x=s["x"],
        y=s["y"],
        energy=s["energy"],
        keys=set(s["keys"]),   # JSON lưu list, State dùng set
    )

    node = Node(state=state, parent=None, action=None, cost=0)
    return level, node
index = {
    "current_action": 0
}


def get_action_index():
    a = index["current_action"]
    index["current_action"] += 1
    return a

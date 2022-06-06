DETECTION = "DETECTION"
ROTATE = "ROTATE"
SHOOT = "SHOOT"
MOVE_FORWARD = "MOVE_FORWARD"
MOVE_BACKWARD = "MOVE_BACKWARD"
MOVE_LEFT = "MOVE_LEFT"
MOVE_RIGHT = "MOVE_RIGHT"

possible_actions = [DETECTION, ROTATE, SHOOT, MOVE_FORWARD, MOVE_BACKWARD, MOVE_LEFT, MOVE_RIGHT]


def decode_message(message: str) -> (str, int):
    action_type = None
    action_value = None
    for action in possible_actions:
        if message.startswith(action):
            action_type = action
            action_value = message[len(action)+1:]
            break

    return action_type, action_value

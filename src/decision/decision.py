from src.TankController import ACTION_SHOOT_TARGET
from src.shared.indexing import get_action_index

# PRIORITY CONFIGURATION
HIGH = 4
MEDIUM = 3
LOW = 2
LOWEST = 1

priority_dict = {
    "type 1": HIGH,
    "type 2": LOWEST,
    "type 3": LOWEST,
    "type 4": LOWEST
}
# END PRIORITY CONFIGURATION

CONFIRMED_TARGET_THRESHOLD = 20
POSITION_ERROR_THRESHOLD = 0.01

decision_dict = {}


def request_action():
    global decision_dict

    if len(decision_dict) == 0:
        return None

    max_value = max(decision_dict.values())
    max_keys = [k for k, v in decision_dict.items() if v == max_value]
    if max_value > CONFIRMED_TARGET_THRESHOLD:
        target = max_keys[0]
        decision_dict.pop(target)
        return get_action_index(), [ACTION_SHOOT_TARGET, target]
    else:
        return None


def add_detection(props: str):
    global decision_dict

    name, priority, screen_position = extract_opts(props)

    if "enemy" not in name:
        return

    upper_bound = round(screen_position + POSITION_ERROR_THRESHOLD, 2)
    lower_bound = round(screen_position - POSITION_ERROR_THRESHOLD, 2)
    print(lower_bound in decision_dict, upper_bound in decision_dict)

    if screen_position in decision_dict:
        decision_dict.update({screen_position: decision_dict[screen_position] + 1 * priority})
    elif upper_bound in decision_dict:
        decision_dict.update(
            {upper_bound: decision_dict[upper_bound] + 1 * priority})
    elif lower_bound in decision_dict:
        decision_dict.update(
            {lower_bound: decision_dict[lower_bound] + 1 * priority})
    else:
        decision_dict.update({screen_position: 1 * priority})


def extract_opts(props: str):
    name, screen_position = props.split(',')
    name = name.lower()
    priority = LOWEST

    for key, value in priority_dict.items():
        if key in name:
            priority = value
            break
    return name, priority, float(screen_position)

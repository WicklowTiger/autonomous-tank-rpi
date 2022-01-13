

def decode_message(message: str) -> (str, int):
    if message.__contains__("ROTATE"):
        degree = message.upper().replace("ROTATE", "")
        if degree.isnumeric():
            return "rotate", int(degree)
    return "not implemented", None

import logging
from src.ActionManager import ActionManager


if __name__ == "__main__":
    logFormat = "%(asctime)s: %(message)s"
    logging.basicConfig(format=logFormat, level=logging.INFO,
                        datefmt="%H:%M:%S")

    # Instantiate and start ActionManager
    action_manager = ActionManager()
    action_manager.run()

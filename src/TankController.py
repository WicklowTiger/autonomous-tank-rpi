import threading

import RPi.GPIO as GPIO

from time import sleep

ACTION_ROTATE = "ROTATE"
ACTION_SHOOT = "SHOOT"
ACTION_SHOOT_TARGET = "SHOOT_TARGET"

# example actions { 1: [ACTION_ROTATE, 0.5], 2: [ACTION_SHOOT, None], 3: [ACTION_SHOOT_TARGET, 0.5] }
controller_action_queue = {}


def compute_angle(screen_position, camera_fov=49, camera_offset=66) -> int:
    return int(camera_offset + ((1-screen_position) * camera_fov))


class TankController:
    """
    Simple controller for turret servo + motors
    """
    servo_signal_pin = 12
    turret_pin = 11
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_signal_pin, GPIO.OUT)
        GPIO.setup(self.turret_pin, GPIO.OUT)
        GPIO.output(self.turret_pin, True)

        self.busy = False
        self.pwm = GPIO.PWM(self.servo_signal_pin, 50)
        self.pwm.start(0)
        self.runThread = threading.Thread(target=self.run)
        self.runThread.start()

    def set_angle(self, angle: int) -> None:
        """
        Converts angle to pwm signal and sends it to servo
        """
        print("setting angle to " + str(angle))
        duty = angle / 18 + 2
        GPIO.output(self.servo_signal_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.servo_signal_pin, False)
        self.pwm.ChangeDutyCycle(0)
        sleep(0.1)  # just to make sure the turret is in the right position

    def shoot(self, time=0.5) -> None:
        GPIO.output(self.turret_pin, False)
        sleep(time)
        GPIO.output(self.turret_pin, True)

    def run(self):
        while True:
            if len(controller_action_queue.keys()) != 0:
                self.busy = True
                action = list(controller_action_queue.items())[0]
                if action[1][0] == ACTION_ROTATE:
                    self.set_angle(compute_angle(action[1][1]))
                elif action[1][0] == ACTION_SHOOT:
                    print("shoot")
                elif action[1][0] == ACTION_SHOOT_TARGET:
                    self.set_angle(compute_angle(action[1][1]))
                    print("shoot target")
                controller_action_queue.pop(action[0])
                self.busy = False
            sleep(0.1)

import RPi.GPIO as GPIO

from time import sleep


class TankController:
    servo_signal_pin = 3
    
    def __init__(self):
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.servo_signal_pin, GPIO.OUT)

        self.pwm = GPIO.PWM(self.servo_signal_pin, 50)
        self.pwm.start(0)

    def set_angle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.servo_signal_pin, True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.servo_signal_pin, False)
        self.pwm.ChangeDutyCycle(0)


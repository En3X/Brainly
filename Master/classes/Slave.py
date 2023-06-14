from pyfirmata import Arduino, util
import pyfirmata
from pyfiglet import Figlet
from PySide2.QtCore import QThread
from pynput import keyboard


class Slave():
    def __init__(self, baudrate, comm):
        super().__init__()
        self.SELF_DRIVING_MODE = True

        try:
            self.formatter = Figlet(font='slant')
            print(self.formatter.renderText("BRAINLY"))

            self.car = Arduino(comm, baudrate=baudrate)
            print(f"Connection to {comm} Successful")
            print("Setting up pin")

            self.pin11 = self.car.get_pin('d:11:p')
            self.pin3 = self.car.get_pin('d:3:p')
            self.pin5 = self.car.get_pin('d:5:p')
            self.pin6 = self.car.get_pin('d:6:p')

            self.pin6.mode = pyfirmata.PWM
            self.pin11.mode = pyfirmata.PWM
            self.pin5.mode = pyfirmata.PWM
            self.pin3.mode = pyfirmata.PWM

            self.MOTOR_DIRECTION = 0x01

            print("Setting up pin successful")
            print("Adding Keyboard Controller")

        except Exception as e:
            raise Exception(e)

    def set_driving_mode(self, self_driving):
        self.SELF_DRIVING_MODE = self_driving

    def set_motor_direction(self, direction):
        self.car.send_sysex(self.MOTOR_DIRECTION, [direction])

    def activate_pins(self):
        self.pin11.write(0.8)
        self.pin3.write(0.8)
        self.pin5.write(0.8)
        self.pin6.write(0.8)

    def forward(self):
        self.set_motor_direction(1)
        self.activate_pins()
        print("Going forward")

    def left(self):
        #  Function name is wrong, should go right
        self.set_motor_direction(5)
        self.activate_pins()
        print("Going top left")

    def right(self):
        #  Function name is wrong, should go left

        self.set_motor_direction(6)
        self.activate_pins()
        print("Going top right")

    def topLeft(self):
        self.set_motor_direction(6)
        self.activate_pins()
        print("Going top left")

    def backward(self):
        self.set_motor_direction(2)
        self.activate_pins()
        print("Going backward")

    def topRight(self):
        self.set_motor_direction(5)
        self.activate_pins()
        print("Going top right")

    def stop(self):
        self.set_motor_direction(7)
        self.pin11.write(0)
        self.pin3.write(0)
        self.pin5.write(0)
        self.pin6.write(0)

from pyfirmata import Arduino, util
from pyfiglet import Figlet
from PySide2.QtCore import QThread
from pynput import keyboard


class Slave():
    def __init__(self, baudrate, comm):
        super().__init__()
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
            self.MOTOR_DIRECTION = 0x01

            print("Setting up pin successful")
            print("Adding Keyboard Controller")

        except Exception as e:
            raise Exception(e)

    def set_motor_direction(self, direction):
        self.car.send_sysex(self.MOTOR_DIRECTION, [direction])

    def activate_pins(self):
        self.pin11.write(1)
        self.pin3.write(1)
        self.pin5.write(1)
        self.pin6.write(1)

    def forward(self):
        self.set_motor_direction(1)
        self.activate_pins()
        print("Going forward")

    def left(self):
        self.set_motor_direction(5)
        self.activate_pins()
        print("Going top right")

    def right(self):
        self.set_motor_direction(5)
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

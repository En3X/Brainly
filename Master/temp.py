from pyfirmata import Arduino, util
from pynput import keyboard

if __name__ == '__main__':
    car = Arduino("COM3", baudrate=9600)
    print("Connected to arduino")

    pin11 = car.get_pin('d:11:p')
    pin3 = car.get_pin('d:3:p')
    pin5 = car.get_pin('d:5:p')
    pin6 = car.get_pin('d:6:p')
    print("Pins set")
    MOTOR_DIRECTION = 0x01


    def set_motor_direction(direction):
        car.send_sysex(MOTOR_DIRECTION, [direction])


    def forward():
        # print("Going Forward")
        set_motor_direction(1)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)
        # car.pass_time(1)
        # pin11.write(0)
        # pin3.write(0)
        # pin5.write(0)
        # pin6.write(0)


    def backward():
        # print("Going Backward")

        set_motor_direction(2)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)
        # car.pass_time(1)
        # pin11.write(0)
        # pin3.write(0)
        # pin5.write(0)
        # pin6.write(0)
        # car.pass_time(1)


    def left():
        # print("Going Left")
        set_motor_direction(3)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)
        # car.pass_time(1)
        # pin11.write(0)
        # pin3.write(0)
        # pin5.write(0)
        # pin6.write(0)
        # car.pass_time(1)


    def right():
        # print("Going Right")
        set_motor_direction(4)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)
        # car.pass_time(1)
        # pin11.write(0)
        # pin3.write(0)
        # pin5.write(0)
        # pin6.write(0)
        # car.pass_time(1)


    def topLeft():
        # print("Going Left")
        set_motor_direction(6)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)


    def topRight():
        # print("Going Left")
        set_motor_direction(5)
        pin11.write(1)
        pin3.write(1)
        pin5.write(1)
        pin6.write(1)


    def stop(key):
        set_motor_direction(7)
        pin11.write(0)
        pin3.write(0)
        pin5.write(0)
        pin6.write(0)


    #
    # forward()
    # backward()
    # left()
    # right()

    def keyboard_listener(key):
        if key == keyboard.Key.up or key == "w":
            print("Going forward")
            forward()
        elif key == keyboard.Key.down or key == 's':
            print("Going Back")
            backward()

        elif key == keyboard.Key.right:
            print("Going top right")
            topLeft()

        elif key == keyboard.Key.left:
            print("Going top left")
            topRight()

        # elif key == keyboard.Key.left or key == 'a':
        #     print("Going Left")
        #     left()
        #
        # elif  key == keyboard.Key.right or key == 'd':
        #     print("Going Right")
        #     right()
        else:
            pass


    with keyboard.Listener(on_press=keyboard_listener, on_release=stop) as listener:
        listener.join()

    # while True:
    #     try:
    #         if kb.is_pressed('w'):
    #             keyboard_listener('w')
    #         elif keyboard.is_pressed('s'):
    #             keyboard_listener('s')
    #         elif keyboard.is_pressed('d'):
    #             keyboard_listener('d')
    #         elif keyboard.is_pressed('a'):
    #             keyboard_listener('aaa')
    #         else:
    #             pass
    #     except Exception as e:
    #         print(e)

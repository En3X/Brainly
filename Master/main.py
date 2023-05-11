from pynput import keyboard
from classes import Slave,TKGUI
from threading import Thread

if __name__ == '__main__':
    gui = TKGUI.TKGUI()




    def start_mainloop():
        gui.mainloop()

    def log(log_type,log_text):
        new_log = gui.logs.cget("text")
        new_log = f"{new_log}\n<{log_type}> {log_text}"
        logs_controller = new_log.split("\n")
        if len(logs_controller)>10:
            logs_controller.pop()
        new_log = "\n".join(logs_controller)
        gui.logs.config(text=new_log)

    car = None
    def initialize_car():
        try:
            global car
            car = Slave.Slave(baudrate=9600, comm="COM3")
            log("SUCCESS","Connection to car successful")
        except Exception as e:
            print(e)
            log("ERROR",e)

    def on_key_press(key):
        print("Key pressed", key)
        try:
            if key == keyboard.Key.up:
                gui.up_btn.configure(background="pink")
                log("COMMAND","Going forward")
                # ui.up.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")
                car.forward()
            elif key == keyboard.Key.down:
                gui.down_btn.configure(background="pink")

                log("COMMAND","Going Back")
                # ui.down.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")

                car.backward()

            elif key == keyboard.Key.right:
                gui.right_btn.configure(background="pink")

                log("COMMAND","Going top right")
                # ui.right.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")

                car.topRight()

            elif key == keyboard.Key.left:
                gui.left_btn.configure(background="pink")

                log("COMMAND","Going top left")
                # ui.left.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")
                car.topLeft()
            else:
                pass

        except Exception as e:
            print(e)

    def stop(key):
        try:
            gui.up_btn.configure(background="#f0f0f0")
            gui.down_btn.configure(background="#f0f0f0")
            gui.right_btn.configure(background="#f0f0f0")
            gui.left_btn.configure(background="#f0f0f0")
            log("COMMAND", "Stopping car")
            car.stop()
        except Exception as e:
            print(e)

    def setup_listener():
        listener = keyboard.Listener(on_press=on_key_press, on_release=stop)
        listener.start()


    # setup_listener()
    listener_thread = Thread(target=setup_listener)
    car_thread = Thread(target=initialize_car)

    car_thread.start()
    listener_thread.start()
    start_mainloop()
    car_thread.join()
    listener_thread.join()




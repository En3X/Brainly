import time

from pynput import keyboard
from classes import Slave, TKGUI, VideoControl
from classes import StartPage
from threading import Thread
from PIL import Image, ImageTk

if __name__ == '__main__':
    gui = StartPage.MainWindow()
    gui.title = "Brainly - A Vehicle With a Brain"
    IS_CAR_RUNNING = False


    def start_mainloop():
        gui.mainloop()


    def log(log_type, log_text):
        log_text = str(log_text)
        new_log = gui.logs.cget("text")
        logs_controller = new_log.split("\n")
        if len(logs_controller) > 15:
            removed_data = logs_controller.remove(logs_controller[0])
        if not f"<{log_type}> {log_text}".__eq__(logs_controller[-1]):
            print(logs_controller[-1])
            logs_controller.insert(len(logs_controller), f"<{log_type}> {log_text}")

        # print(logs_controller[-1])
        new_log = "\n".join(logs_controller)
        gui.logs.config(text=new_log)


    car = None
    video = None

    def initialize_car():
        global IS_CAR_RUNNING
        global car

        try:
            car = Slave.Slave(baudrate=9600, comm="COM3")
            log("SUCCESS", "Connection to car successful")
            IS_CAR_RUNNING = True

        except Exception as e:
            IS_CAR_RUNNING = False
            print(e)
            log("ERROR", e)

    def enableSelfDrivingMode():
        gui.DRIVING_MODE = "SELF"
        pass


    def enableMannualMode():
        gui.DRIVING_MODE = "MANNUAL"
        pass


    def on_key_press(key):
        # print("Key pressed", key)
        if not IS_CAR_RUNNING:
            log("WARNING","The bluetooth module is still loading and the car is not connected yet")
            return

        # if(key == keyboard.Key.alt):
        #     enableSelfDrivingMode()
        # else:
        enableMannualMode()

        try:

            if key == keyboard.Key.up:
                gui.up_btn.configure(background="white",foreground="#292C3C")
                car.forward()
                log("COMMAND", "Going forward")
                # ui.up.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")
            elif key == keyboard.Key.down:
                gui.down_btn.configure(background="white",foreground="#292C3C")
                car.backward()

                log("COMMAND", "Going Back")
                # ui.down.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")


            elif key == keyboard.Key.right:
                gui.right_btn.configure(background="white",foreground="#292C3C")
                car.topRight()
                log("COMMAND", "Going top right")
                # ui.right.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")


            elif key == keyboard.Key.left:
                gui.left_btn.configure(background="white",foreground="#292C3C")
                car.topLeft()

                log("COMMAND", "Going top left")
                # ui.left.setStyleSheet("background-color: #DCF7D0;border: 1px solid #DCF7D0;")
            else:
                pass

        except Exception as e:
            print(e)

    def stop(key):
        if not IS_CAR_RUNNING:
            return
        try:
            gui.up_btn.configure(background="#292C3C",foreground="white")
            gui.down_btn.configure(background="#292C3C",foreground="white")
            gui.right_btn.configure(background="#292C3C",foreground="white")
            gui.left_btn.configure(background="#292C3C",foreground="white")
            log("COMMAND", "Stopping car")
            car.stop()
        except Exception as e:
            print(e)


    def setup_listener():
        listener = keyboard.Listener(on_press=on_key_press, on_release=stop)
        listener.start()
        log("INFO", "Keyboard controller activated")



    def show_video_footage():
        try:
            video = VideoControl.VideoController()
            ret, img, canny, direction = video.getVideo()
            camera_holder_label = gui.camera_holder_label
            if (img is not None):
                photo = ImageTk.PhotoImage(image=Image.fromarray(canny))
                camera_holder_label.imgtk = photo
                camera_holder_label.configure(image=photo)

                if gui.SELF_DRIVING_MODE and car!= None:
                    stop('q')
                    # print("Direction:",direction)
                    if direction == "left":
                        car.topLeft()
                    elif direction == "right":
                        car.topRight()
                    elif direction == "straight":
                        car.forward()
                    else:
                        stop('q')

            else:
                print("No frame detected")
            camera_holder_label.after(20, show_video_footage)

        except Exception as e:
            print(e)



    # setup_listener()
    video_thread = Thread(target=show_video_footage)

    listener_thread = Thread(target=setup_listener)
    car_thread = Thread(target=initialize_car)

    video_thread.start()
    car_thread.start()
    listener_thread.start()
    start_mainloop()
    car_thread.join()
    listener_thread.join()

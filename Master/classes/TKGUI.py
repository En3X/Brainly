from tkinter import *
import tkinter as tk
from PIL import Image, ImageTk
from classes import VideoControl


class TKGUI(Tk):
    def __init__(self):
        global camera_width, camera_height
        super().__init__()
        self.title("Brainly - Vehicle With A Brain")
        self.width = int(self.winfo_screenwidth() / 1.5)
        self.height = int(self.winfo_screenheight() / 1.5)
        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")

        try:
            # setting up camera
            camera_height = int(self.height / 2)
            camera_width = int(self.width - 200)
            self.camera_ = tk.Frame(self, bg="black", height=camera_height, width=camera_width)

            self.camera_holder_label = tk.Label(self.camera_, text="Hello world", background="black",fg="white")
            self.camera_holder_label.place(x=0, y=0)

            self.camera_.place(x=(self.width - camera_width) / 2, y=20)

            try:
                self.video = VideoControl.VideoController()
                self.show_video_footage()
            except Exception as e:
                print(e)

            # self.camera_text = Label(self.camera_, text="Camera not initialized",bg="black",fg="white")
            # self.camera_text.place(relx=0.5,rely=0.5)
        except Exception as e:
            print(e)

        # Controller Buttons
        btn_frame_height = int(camera_height / 1.3)
        btn_frame_width = int(camera_width / 2)
        self.btn_frames = tk.Frame(self, height=btn_frame_height, width=btn_frame_width)
        btn_width = 10
        btn_height = 2
        self.up_btn = tk.Button(self.btn_frames, text="Up", width=btn_width, height=btn_height)
        self.down_btn = tk.Button(self.btn_frames, text="Down", width=btn_width, height=btn_height)
        self.left_btn = tk.Button(self.btn_frames, text="Left", width=btn_width, height=btn_height)
        self.right_btn = tk.Button(self.btn_frames, text="Right", width=btn_width, height=btn_height)

        self.up_btn.place(relx=0.3, rely=0.1)
        self.down_btn.place(relx=0.3, rely=0.8)
        self.left_btn.place(relx=0, rely=0.5)
        self.right_btn.place(relx=0.6, rely=0.5)

        self.controller_title = tk.Label(self, text="Mannual controller")

        self.controller_title.place(x=(self.width - camera_width) / 2, y=camera_height + 25)
        self.btn_frames.place(x=(self.width - camera_width) / 2, y=camera_height + 50)

        # setting up logs box
        log_box_x = ((self.width - camera_width) / 2) + (camera_width / 2)
        self.log_box = tk.Frame(self, bg="white", height=camera_height / 1.3, width=camera_width / 2)
        self.logs_title = tk.Label(self, text="Logs")
        self.logs_title.place(x=log_box_x, y=camera_height + 25)

        self.logs = tk.Label(self.log_box, text="<INFO> Connecting to car via Bluetooth and setting up pins",
                             foreground="black", background="white", wraplength=(camera_width / 2) - 40, justify="left")
        self.logs.place(x=0, y=0)
        self.log_box.place(x=log_box_x, y=(camera_height + 50))

    def show_video_footage(self):
        ret, frame = self.video.getVideo()
        if ret and (frame is not None):
            photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.camera_holder_label.imgtk = photo
            self.camera_holder_label.configure(image=photo)
        else:
            print("No frame detected")
        self.camera_holder_label.after(20, self.show_video_footage)


if __name__ == '__main__':
    gui = TKGUI()
    gui.mainloop()

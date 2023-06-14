from tkinter import *
from tkinter.font import Font
import tkinter as tk
from PIL import Image, ImageTk
from classes import VideoControl
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
class ManualControlPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.font_awesome = Font(family="Font Awesome 5 Free Solid", size=12)
        try:
            self.width = int(self.winfo_screenwidth() / 1.5)
            self.height = int(self.winfo_screenheight() / 1.5)

            # setting up camera
            camera_height = int(self.height / 2)
            camera_width = int(self.width - 200)
            self.camera_ = tk.Frame(self, bg="black", height=camera_height, width=camera_width)

            self.camera_holder_label = tk.Label(self.camera_, text="Camera module not initialized", background="black",
                                                fg="white")
            self.camera_holder_label.place(x=0, y=0)

            self.camera_.place(x=(self.width - camera_width) / 2, y=20)

            try:
                self.video = VideoControl.VideoController()
                #
                # video_thread = Thread(target=self.show_video_footage)
                # video_thread.start()
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
        btn_width = 6
        btn_height = 2
        try:
            self.up_btn = tk.Button(self.btn_frames, border=0, background="#292C3C", foreground="white", text="\uf062",
                                    width=btn_width, height=btn_height, font=self.font_awesome)
            self.down_btn = tk.Button(self.btn_frames, border=0, text="\uf063", width=btn_width, height=btn_height,
                                      font=self.font_awesome, background="#292C3C", foreground="white")
            self.left_btn = tk.Button(self.btn_frames, border=0, text="\uf060", width=btn_width, height=btn_height,
                                      font=self.font_awesome, background="#292C3C", foreground="white")
            self.right_btn = tk.Button(self.btn_frames, border=0, text="\uf061", width=btn_width, height=btn_height,
                                       font=self.font_awesome, background="#292C3C", foreground="white")

            self.up_btn.place(relx=0.15, rely=0.2)
            self.down_btn.place(relx=0.15, rely=0.6)
            self.left_btn.place(relx=0, rely=0.4)
            self.right_btn.place(relx=0.3, rely=0.4)

            self.on_btn = tk.PhotoImage("./on.png")
            self.off_btn = tk.PhotoImage("./off.png")

            self.switch = tk.Button(self.frame, image=self.off_btn, bd=0, command=self.changeSwitch)

        except Exception as e:
            print(e)
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

        # Setup car



    def setSelfDrivingMode(self, mode):
        self.SELF_DRIVING_MODE = mode

    def getSelfDivingMode(self):
        return self.SELF_DRIVING_MODE

    def getPhotoImage(self, path):
        try:
            data = svg2rlg(path)
            temp_bytes = BytesIO()

            png_data = renderPM.drawToFile(data, temp_bytes, fmt="PNG")

            return ImageTk.PhotoImage(Image.open(png_data).resize((40, 40), Image.ANTIALIAS))

        except Exception as e:
            return None

    def show_video_footage(self):
        ret, frame = self.video.getVideo()
        if (frame is not None):
            photo = ImageTk.PhotoImage(image=Image.fromarray(ret))
            self.camera_holder_label.imgtk = photo
            self.camera_holder_label.configure(image=photo)
        else:
            print("No frame detected")
        self.camera_holder_label.after(20, self.show_video_footage)


def go_to_page(self, page_name):
        self.controller.show_frame(page_name)

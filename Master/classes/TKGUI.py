from tkinter import *
from tkinter.font import Font
import tkinter as tk
from PIL import Image, ImageTk
from classes import VideoControl
from threading import Thread
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
from io import BytesIO
class TKGUI(Tk):
    def __init__(self):
        global camera_width, camera_height
        super().__init__()

        self.SELF_DRIVING_MODE = True

        self.DRIVING_MODE = "MANNUAL"


        self.title("Brainly - Vehicle With A Brain")
        self.width = int(self.winfo_screenwidth() / 1.5)
        self.height = int(self.winfo_screenheight() / 1.2)
        self.resizable(False, False)
        self.geometry(f"{self.width}x{self.height}")
        self.font_awesome = Font(family="Font Awesome 5 Free Solid",size=12)
        try:
            # setting up camera
            camera_height = int(self.height / 2)
            camera_width = int(self.width - 200)
            self.camera_ = tk.Frame(self, bg="black", height=camera_height, width=camera_width)

            self.camera_holder_label = tk.Label(self.camera_, text="Camera module not initialized", background="black", fg="white")
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
        btn_frame_height = int(camera_height / 1.5)
        btn_frame_width = int(camera_width / 2)
        self.btn_frames = tk.Frame(self, height=btn_frame_height, width=btn_frame_width)
        btn_width = 6
        btn_height = 2
        try:
            self.up_btn = tk.Button(self.btn_frames,border=0,background="#292C3C",foreground="white",text="\uf062", width=btn_width, height=btn_height,font=self.font_awesome)
            self.down_btn = tk.Button(self.btn_frames,border=0, text="\uf063", width=btn_width, height=btn_height,font=self.font_awesome,background="#292C3C",foreground="white")
            self.left_btn = tk.Button(self.btn_frames,border=0, text="\uf060", width=btn_width, height=btn_height,font=self.font_awesome,background="#292C3C",foreground="white")
            self.right_btn = tk.Button(self.btn_frames,border=0, text="\uf061", width=btn_width, height=btn_height,font=self.font_awesome,background="#292C3C",foreground="white")

            self.up_btn.place(relx=0.15, rely=0.2)
            self.down_btn.place(relx=0.15, rely=0.6)
            self.left_btn.place(relx=0, rely=0.4)
            self.right_btn.place(relx=0.3, rely=0.4)


        #
        except Exception as e:
            print(e)
        self.controller_title = tk.Label(self, text="Control Mode: Mannual controller")

        BTN_FRAME_X = (self.width - camera_width) / 2
        BTN_FRAME_Y = camera_height + 50
        self.controller_title.place(x=(self.width - camera_width) / 2, y=camera_height + 25)
        self.btn_frames.place(x=BTN_FRAME_X, y=BTN_FRAME_Y)

        # setting up logs box
        log_box_x = ((self.width - camera_width) / 2) + (camera_width / 2)
        self.log_box = tk.Frame(self, bg="white", height=camera_height / 1.5, width=camera_width / 2)
        self.logs_title = tk.Label(self, text="Logs")
        self.logs_title.place(x=log_box_x, y=camera_height + 25)

        self.logs = tk.Label(self.log_box, text="<INFO> Connecting to car via Bluetooth and setting up pins",
                             foreground="black", background="white", wraplength=(camera_width / 2) - 40, justify="left")
        self.logs.place(x=0, y=0)
        self.log_box.place(x=log_box_x, y=(camera_height + 50))

        self.on_btn = tk.PhotoImage("./on.png")
        self.off_btn = tk.PhotoImage("./off.png")

        # self.SelfDrivingLabel = tk.Label(self,text="Self Driving Mode: ")
        # self.voiceControlModeLabel = tk.Label(self,text="Voice Control Mode: ")
        self.sd_var = tk.IntVar()
        self.vc_var = tk.IntVar()

        self.selfDrivingControl = tk.Checkbutton(self, text='Enable Self Driving Mode',variable=self.sd_var, onvalue=1, offvalue=0,command=self.setSelfDrivingMode)
        self.selfDrivingControl.place(x=BTN_FRAME_X, y=(BTN_FRAME_Y+btn_frame_height))

        self.voiceControlMode = tk.Checkbutton(self, text='Enable Voice Control Mode',variable=self.vc_var, onvalue=1, offvalue=0,command=self.setVoiceControlMode)
        self.voiceControlMode.place(x=BTN_FRAME_X, y=(BTN_FRAME_Y+btn_frame_height+30))


    def setMannualMode(self):
        self.DRIVING_MODE = "MANNUAL"
        self.controller_title.config(text="Control Mode: Mannual controller")
        self.vc_var.set(0)
        self.sd_var.set(0)

    def setSelfDrivingMode(self):
        if self.DRIVING_MODE == "SELF":
            self.setMannualMode()
        else:
            self.DRIVING_MODE = "SELF"
            self.controller_title.config(text="Control Mode: Self Driving")
            self.vc_var.set(0)
            self.sd_var.set(1)


    def setVoiceControlMode(self):
        if self.DRIVING_MODE == "VOICE":
            self.setMannualMode()
        else:
            self.DRIVING_MODE = "VOICE"
            self.controller_title.config(text="Control Mode: Voice Controlled")
            self.sd_var.set(0)
            self.vc_var.set(1)

    def getPhotoImage(self, path):
        try:
            data = svg2rlg(path)
            temp_bytes = BytesIO()

            png_data = renderPM.drawToFile(data,temp_bytes,fmt="PNG")

            return ImageTk.PhotoImage(Image.open(png_data).resize((40,40), Image.ANTIALIAS))

        except Exception as e:
            return None



    # def show_video_footage(self):
    #     ret, frame = self.video.getVideo()
    #     if (frame is not None):
    #         photo = ImageTk.PhotoImage(image=Image.fromarray(ret))
    #         self.camera_holder_label.imgtk = photo
    #         self.camera_holder_label.configure(image=photo)
    #     else:
    #         print("No frame detected")
    #     self.camera_holder_label.after(20, self.show_video_footage)





if __name__ == '__main__':
    gui = TKGUI()
    gui.mainloop()

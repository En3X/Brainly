import cv2
from PIL import  Image, ImageTk

class VideoController:
    def __init__(self):
        self.capture = cv2.VideoCapture(0,cv2.CAP_DSHOW)
        if not self.capture.isOpened():
            raise ValueError("No video source found")

    def getVideo(self):
        if self.capture.isOpened():
            ret, frame = self.capture.read()
            if ret:
                return ret,frame


        return ret, None



import sys
from PySide2 import QtCore, QtWidgets
import qtawesome as qta


class GUI(QtWidgets.QWidget):

    # def create_car_instance(self):
    #     try:
    #         self.car = Slave.Slave(baudrate=9600, comm="COM3")
    #     except Exception as e:
    #         print(e)
    #
    # def keyPressEvent(self, signal):
    #     print(signal.text())


    def setupUi(self):
        self.setObjectName("Brainly")
        self.setFixedSize(800, 513)
        # self.centralwidget = QtWidgets.QWidget(self)
        # self.centralwidget.setObjectName("centralwidget")

        # flags = QtCore.Qt.WindowFlags(QtCore.Qt.FramelessWindowHint)
        # Brainly.setWindowFlags(flags)

        self.logs_box = QtWidgets.QTextEdit(self)
        self.logs_box.setGeometry(QtCore.QRect(450, 310, 331, 171))
        self.logs_box.setObjectName("logs_box")
        self.logs_box.setPlainText("Hello worldl")
        self.logs_box.setReadOnly(True)

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(450, 280, 61, 21))
        self.label.setObjectName("label")
        self.label.setText("Logs")

        self.camera_ = QtWidgets.QTextEdit(self)
        self.camera_.setGeometry(QtCore.QRect(10, 30, 781, 231))
        self.camera_.setObjectName("camera_")
        self.camera_.setReadOnly(True)
        self.camera_.setText("Camera not initialized")
        self.camera_.setDisabled(True)

        # self.controller_frame = QtWidgets.QFrame(self.centralwidget)
        # self.controller_frame.setGeometry(QtCore.QRect(19, 309, 271, 171))
        # self.controller_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        # self.controller_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        # self.controller_frame.setObjectName("controller_frame")

        up_icon = qta.icon("ei.chevron-up")
        self.up = QtWidgets.QPushButton(self)
        self.up.setIcon(up_icon)
        self.up.setGeometry(QtCore.QRect(100, 310, 75, 23))
        self.up.setObjectName("control_btn")

        down_icon = qta.icon("ei.chevron-down")
        self.down = QtWidgets.QPushButton(self)
        self.down.setIcon(down_icon)
        self.down.setGeometry(QtCore.QRect(100, 430, 75, 23))
        self.down.setObjectName("control_btn")

        left_icon = qta.icon("ei.chevron-left")
        self.left = QtWidgets.QPushButton(self)
        self.left.setIcon(left_icon)
        self.left.setGeometry(QtCore.QRect(20, 370, 75, 23))
        self.left.setObjectName("control_btn")

        right_icon = qta.icon("ei.chevron-right")
        self.right = QtWidgets.QPushButton(self)
        self.right.setIcon(right_icon)
        self.right.setGeometry(QtCore.QRect(180, 370, 75, 23))

        self.right.setObjectName("control_btn")

        self.setWindowTitle("Brainly - A Vehicle with a brain")

    def setLog(self, log):
        self.logs_box.setPlainText(log)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    ui = GUI()
    ui.setupUi()
    ui.show()
    sys.exit(app.exec_())

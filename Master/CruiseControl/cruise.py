from classes import Slave
import cv2
from ultralytics import YOLO
from PIL import Image
import supervision as sv
import math
import numpy as np
from time import sleep
from threading import Thread

STOP_MODEL = YOLO("F:\Programming\Project\Master\CruiseControl\\best.pt")
TRAFFIC_MODEL = YOLO(
    "F:\Programming\Project\Master\CruiseControl\\traffic_light_best.pt"
)
BOUNDING_BOX = sv.BoxAnnotator(
    thickness=2,
    text_thickness=2,
    text_scale=1,
)


def initialize_car():
    try:
        car = Slave.Slave(baudrate=9600, comm="COM3")
        print("SUCCESS", "Connection to car successful")

        return car
    except Exception as e:
        print(e)
        return None


def test_car(car):
    car.forward()
    car.car.pass_time(1)
    car.backward()
    car.car.pass_time(1)
    car.topLeft()
    car.car.pass_time(1)
    car.topRight()
    car.car.pass_time(1)
    car.stop()


def get_blur_and_gray_video(img):
    img = cv2.GaussianBlur(img, (5, 5), 0)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    return img


def check_for_stop_sign(img):
    global STOP_MODEL
    stop_sign_detection = STOP_MODEL.predict(img, conf=0.5)[0]
    detections = sv.Detections.from_yolov8(stop_sign_detection)
    if len(detections.xyxy) < 1:
        return None
    else:
        return detections


def check_for_traffic_light(img):
    global TRAFFIC_MODEL
    traffic_light_detection = TRAFFIC_MODEL.predict(img, conf=0.6)[0]
    detections = sv.Detections.from_yolov8(traffic_light_detection)
    if len(detections.xyxy) < 1:
        return False, None, None
    else:
        detection_name = TRAFFIC_MODEL.model.names[detections.class_id[0]]
        if detection_name == "red_light":
            return True, detection_name, detections
        else:
            return False, detection_name, detections


def getDataFromDetections(detection):
    if detection is None:
        return None

    if len(detection.xyxy) == 0:
        return None

    return detection.xyxy[0]


def initialize_self_driving_mode(car, blur_and_gray):
    _, binary_img = cv2.threshold(blur_and_gray, 180, 255, cv2.THRESH_BINARY)
    canny = cv2.Canny(binary_img, 100, 200)
    divider_lines = cv2.HoughLinesP(
        canny, 100, math.pi / 180, 50, minLineLength=20, maxLineGap=50
    )
    if divider_lines is None:
        # no lane line detected
        print("Stop")
        return
    line_img = np.zeros_like(blur_and_gray)
    left_lines = []
    right_lines = []
    direction = ""
    left_slope = right_slope = ""

    for line in divider_lines:
        x1, y1, x2, y2 = line.reshape(4)
        slope = (x2 - x1) / (y2 - y1)

        if slope < 0:
            left_lines.append(line)
        elif slope > 0:
            right_lines.append(line)
        left_slope, left_intercept = np.mean(
            [(y2 - y1) / (x2 - x1) for line in left_lines for x1, y1, x2, y2 in line]
        ), np.mean(
            [
                y1 - (y2 - y1) / (x2 - x1) * x1
                for line in left_lines
                for x1, y1, x2, y2 in line
            ]
        )

        right_slope, right_intercept = np.mean(
            [(y2 - y1) / (x2 - x1) for line in right_lines for x1, y1, x2, y2 in line]
        ), np.mean(
            [
                y1 - (y2 - y1) / (x2 - x1) * x1
                for line in right_lines
                for x1, y1, x2, y2 in line
            ]
        )

        threshold = 0
        if (
            math.isnan(left_slope)
            or not math.isnan(right_slope)
            and int(right_slope) in range(1, 5)
        ):
            direction = "left"
        elif math.isnan(right_slope) and left_slope < -threshold:
            direction = "right"
        elif left_slope in np.arange(0.5, -0.5) or right_slope in np.arange(0.5, -0.5):
            direction = "stop"
        else:
            direction = "straight"

    line_img = cv2.addWeighted(line_img, 1, blur_and_gray, 1, 0)
    line_img = cv2.putText(
        line_img,
        f"D: {direction}",
        (0, 50),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        1,
        (255, 192, 203),
        1,
        cv2.LINE_AA,
    )

    line_img = cv2.putText(
        line_img,
        f"L {left_slope}",
        (0, (line_img.shape[0] - 50)),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        1,
        (255, 192, 203),
        1,
        cv2.LINE_AA,
    )
    line_img = cv2.putText(
        line_img,
        f"R {right_slope}",
        (0, (line_img.shape[0] - 100)),
        cv2.FONT_HERSHEY_COMPLEX_SMALL,
        1,
        (255, 192, 203),
        1,
        cv2.LINE_AA,
    )

    if direction == "straight":
        car.forward()
    elif direction == "left":
        car.topLeft()
    elif direction == "right":
        car.topRight()

    sleep(0.3)
    car.stop()

    # show all windows
    cv2.imshow("Canny", canny)
    cv2.imshow("Detected lines", line_img)
    cv2.imshow("Binary", binary_img)


def main():
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Cannot open video source")
        return
    # video source available
    print("Video source opened")

    car = initialize_car()
    if car is None:
        print()
        return
    # test_car(car)

    print("Connected to car vioa hc-06 module")

    # video processing starts here

    while True:
        ret, img = capture.read()
        if not ret:
            print("Cannot find image")
            return
        blur_and_gray = get_blur_and_gray_video(img)

        # writing code to detect stop signs
        stop_signs_detections = check_for_stop_sign(img)

        if stop_signs_detections is None:
            isRedLight, detection_name, detection = check_for_traffic_light(img)
            if detection is not None:
                x1, y1, x2, y2 = getDataFromDetections(detection=detection)
                if isRedLight is False:
                    # here we will implement all the self driving car logic
                    initialize_self_driving_mode(car, blur_and_gray)

                    if (
                        detection_name == "green_light"
                        or detection_name == "yellow_light"
                    ):
                        img = cv2.rectangle(
                            img, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2
                        )

                else:
                    img = cv2.rectangle(
                        img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2
                    )
                    car.stop()
            else:
                initialize_self_driving_mode(car, blur_and_gray)

        else:
            x1, y1, x2, y2 = getDataFromDetections(stop_signs_detections)
            img = cv2.rectangle(
                img, (int(x1), int(y1)), (int(x2), int(y2)), (255, 0, 0), 2
            )
            car.stop()

        cv2.imshow("Brainly - Original Video", img)
        cv2.imshow("Blurred and Grayscale", blur_and_gray)
        # cv2.imshow("Detected frame", detected_frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()
    car.stop()


if __name__ == "__main__":
    main()

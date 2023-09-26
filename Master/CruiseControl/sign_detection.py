from classes import Slave
import cv2
from ultralytics import YOLO
from PIL import Image
import supervision as sv
import torch


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


def initialize_self_driving_mode(car, img):
    car.forward()


def main():
    capture = cv2.VideoCapture(1)
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
                    initialize_self_driving_mode(car, img)

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
                initialize_self_driving_mode(car, img)

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

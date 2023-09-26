import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


def capture_region_of_interest(img):
    height, width = img.shape[0], img.shape[1]  # height of image
    TOP_CENTER = (381, 123)
    TOP_LEFT = (58, 180)
    TOP_RIGHT = (420, 388)
    BOTTOM_LEFT = (0, height)
    BOTTOM_RIGHT = (width, height)
    REGION_OF_INTEREST = [
        (260, height),
        (265, 140),
        (325, 140),
        (390, height),
    ]

    # REGION_OF_INTEREST = [(0,height),(width,height),(30,240),(385,275)]
    polygons = np.array([REGION_OF_INTEREST])
    polygon_mask = np.zeros_like(img)  # creating triangle mask for image

    cv2.fillPoly(polygon_mask, polygons, 255)  # fill mask with white triangle
    masked_image = cv2.bitwise_and(img, polygon_mask)

    return masked_image


def main():
    capture = cv2.VideoCapture(2)
    if not capture.isOpened():
        print("Cannot find video source")
        return

    while True:
        ret, img = capture.read()
        if not ret:
            print("Cannot read from video stream")
            return

        # img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        img = cv2.blur(img, (5, 5))
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # plt.imshow(img)
        # plt.show()
        _, img = cv2.threshold(img, 140, 255, cv2.THRESH_BINARY)

        canny = cv2.Canny(img, 100, 200)
        canny = capture_region_of_interest(img=canny)
        lines = cv2.HoughLinesP(
            canny,
            rho=1,
            theta=np.pi / 180,
            threshold=20,
            minLineLength=20,
            maxLineGap=50,
        )
        # img = cv2.resize(img, (150, 150))

        line_img = np.zeros_like(img)
        left_lines = []
        right_lines = []
        direction = ""
        left_slope = right_slope = ""
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                slope = (x2 - x1) / (y2 - y1)

                if slope < 0:
                    left_lines.append(line)
                elif slope > 0:
                    right_lines.append(line)
                left_slope, left_intercept = np.mean(
                    [
                        (y2 - y1) / (x2 - x1)
                        for line in left_lines
                        for x1, y1, x2, y2 in line
                    ]
                ), np.mean(
                    [
                        y1 - (y2 - y1) / (x2 - x1) * x1
                        for line in left_lines
                        for x1, y1, x2, y2 in line
                    ]
                )

                right_slope, right_intercept = np.mean(
                    [
                        (y2 - y1) / (x2 - x1)
                        for line in right_lines
                        for x1, y1, x2, y2 in line
                    ]
                ), np.mean(
                    [
                        y1 - (y2 - y1) / (x2 - x1) * x1
                        for line in right_lines
                        for x1, y1, x2, y2 in line
                    ]
                )

            threshold = 0.2
            if right_slope > threshold and (
                left_slope > -threshold or math.isnan(left_slope)
            ):
                direction = "left"
            elif (
                math.isnan(right_slope)
                or right_slope < threshold
                and left_slope < -threshold
            ):
                direction = "right"
            elif left_slope in np.arange(0.5, -0.5) or right_slope in np.arange(
                0.5, -0.5
            ):
                direction = "stop"
            else:
                direction = "straight"

            cv2.line(line_img, (x1, y1), (x2, y2), (255, 192, 203), 5)

        line_img = cv2.addWeighted(line_img, 1, img, 1, 0)
        cv2.putText(
            line_img,
            f"D: {direction}",
            (0, 50),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            1,
            (255, 192, 203),
            1,
            cv2.LINE_AA,
        )

        cv2.putText(
            line_img,
            f"L {left_slope}",
            (0, (line_img.shape[0] - 50)),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            1,
            (255, 192, 203),
            1,
            cv2.LINE_AA,
        )
        cv2.putText(
            line_img,
            f"R {right_slope}",
            (0, (line_img.shape[0] - 100)),
            cv2.FONT_HERSHEY_COMPLEX_SMALL,
            1,
            (255, 192, 203),
            1,
            cv2.LINE_AA,
        )

        cv2.imshow("img", line_img)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

import cv2 as cv
# from cvzone.FaceDetectionModule import FaceDetector
import numpy as np
import matplotlib.pyplot as plt


class VideoController:
    def __init__(self):
        self.capture = cv.VideoCapture(3)
        # self.detector = FaceDetector()
        if not self.capture.isOpened():
            raise ValueError("No video source found")

    def getVideo(self):
        if self.capture.isOpened():
                ret, img = self.capture.read()
                # return ret, img
                if ret:
                    img = cv.rotate(img,cv.ROTATE_90_CLOCKWISE)
                    grey = self.blurAndGrayscale(img)

                    canny_img = self.canny(grey)
                    # roi = self.capture_region_of_interest(canny_img)

                    # self.map_regions_of_interest(img)
                    # # roi = canny_img
                    lines = cv.HoughLinesP(
                        canny_img,  # Input image
                        rho=1,  # Distance resolution of the accumulator in pixels
                        theta=np.pi / 180,  # Angle resolution of the accumulator in radians
                        threshold=50,  # Minimum number of votes (intersections) to consider a line
                        minLineLength=5,  # Minimum length of a line in pixels
                        maxLineGap=10  # Maximum allowed gap between line segments to treat them as a single line
                    )
                    try:
                        lane_detected_img, direction = self.display_lane_lines(img, lines)
                        font = cv.FONT_HERSHEY_SIMPLEX
                        combo_image = cv.addWeighted(lane_detected_img, 1, img, 1, 0)
                        cv.putText(img, direction, (0, 50), font, 2, (0, 255, 0), 2, cv.LINE_AA)
                        return ret, combo_image,canny_img, direction
                    except Exception as e:
                        print(e)
                        return ret, None, None, None
                else:
                    return ret, None, None, None



    def blurAndGrayscale(self, img):
        gray_image = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        blur_img = cv.GaussianBlur(gray_image, (5, 5), 0)
        return blur_img

    def canny(self, img):
        canny_img = cv.Canny(img, 40, 100)
        return canny_img

    def capture_region_of_interest(self, img):
        height, width = img.shape[0], img.shape[1]  # height of image
        TOP_CENTER = (381,123)
        TOP_LEFT = (58, 180)
        TOP_RIGHT = (420,388)
        BOTTOM_LEFT = (0, height)
        BOTTOM_RIGHT = (width, height)
        REGION_OF_INTEREST = [(0,height),(width,height),(320,50),(170,50)]

        # REGION_OF_INTEREST = [(0,height),(width,height),(30,240),(385,275)]
        polygons = np.array([REGION_OF_INTEREST])
        polygon_mask = np.zeros_like(img)  # creating triangle mask for image

        cv.fillPoly(polygon_mask, polygons, 255)  # fill mask with white triangle
        masked_image = cv.bitwise_and(img, polygon_mask)

        return masked_image

    def map_regions_of_interest(self, img):
        plt.imshow(img)
        plt.show()

    def display_lane_lines(self, img, lines):
        line_image = np.zeros_like(img)
        left_lines = []
        right_lines = []
        straight_lines = []
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line.reshape(4)
                slope = (x2 - x1) / (y2 - y1)
                if slope < 0:
                    left_lines.append(line)
                elif slope > 0:
                    right_lines.append(line)
                else:
                    straight_lines.append(line)

            left_slope, left_intercept = np.mean(
                [(y2 - y1) / (x2 - x1) for line in left_lines for x1, y1, x2, y2 in line]), np.mean(
                [y1 - (y2 - y1) / (x2 - x1) * x1 for line in left_lines for x1, y1, x2, y2 in line])
            right_slope, right_intercept = np.mean(
                [(y2 - y1) / (x2 - x1) for line in right_lines for x1, y1, x2, y2 in line]), np.mean(
                [y1 - (y2 - y1) / (x2 - x1) * x1 for line in right_lines for x1, y1, x2, y2 in line])

            print(f"[{left_slope} {right_slope}]")
            threshold = 1.3
            if left_slope < -threshold and right_slope > threshold:
                direction = 'right'
            elif left_slope > threshold and right_slope < -threshold:
                direction = 'left'
            elif left_slope == 0 == right_slope:
                direction = 'stop'
            else:
                direction = "straight"
            print("SELF_DRIVING: ",direction)
            cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 255), 10)

            return line_image, direction

        return None, "stop"

        # line_image = np.zeros_like(img)
        # left_lines = []
        # right_lines = []
        #
        # if lines is not None:
        #     for line in lines:
        #         x1, y1, x2, y2 = line.reshape(4)
        #         slope = (y2 - y1) / (x2 - x1)  # Calculate the slope in terms of y/x
        #
        #         # Sort the lines into left or right based on the slope
        #         if slope < 0:
        #             left_lines.append(line)
        #         else:
        #             right_lines.append(line)
        #
        #     # Calculate the average slope and intercept for left lines
        #     if left_lines:
        #         left_slope = np.mean([(y2 - y1) / (x2 - x1) for x1, y1, x2, y2 in left_lines])
        #         left_intercept = np.mean([y1 - (y2 - y1) / (x2 - x1) * x1 for x1, y1, x2, y2 in left_lines])
        #     else:
        #         left_slope = 0
        #         left_intercept = 0
        #     print("Lanes detected")
        #     # Calculate the average slope and intercept for right lines
        #     if right_lines:
        #         right_slope = np.mean([(y2 - y1) / (x2 - x1) for x1, y1, x2, y2 in right_lines])
        #         right_intercept = np.mean([y1 - (y2 - y1) / (x2 - x1) * x1 for x1, y1, x2, y2 in right_lines])
        #     else:
        #         right_slope = 0
        #         right_intercept = 0
        #
        #     # print(f"[{left_slope} {right_slope}]")
        #
        #     threshold = 0.5  # Adjust the threshold as needed
        #
        #     if left_slope < -threshold and right_slope < -threshold:
        #         direction = 'right'
        #     elif left_slope > threshold and right_slope > threshold:
        #         direction = 'left'
        #     else:
        #         direction = 'straight'
        #
        #     print("SELF_DRIVING:", direction)
        #
        #     #
        #     # Draw the detected lines on the line_image
        #     for line in left_lines + right_lines:
        #         x1, y1, x2, y2 = line.reshape(4)
        #         cv.line(line_image, (x1, y1), (x2, y2), (255, 0, 255), 10)
        #
        #     return line_image, direction
        #
        # return None, 'stop'

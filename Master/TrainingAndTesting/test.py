import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

def blurAndGrayscale(img):
    gray_image = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    blur_img = cv.GaussianBlur(gray_image,(5,5),0)
    return blur_img

def canny(img):
    canny_img = cv.Canny(img,40,100)
    return canny_img


def capture_region_of_interest(img):
    height,width = img.shape[0],img.shape[1] # height of image
    TOP_LEFT = (70,0)
    TOP_RIGHT = (660,500)
    BOTTOM_LEFT = (300,height)
    BOTTOM_RIGHT = (1000,height)
    REGION_OF_INTEREST = [BOTTOM_LEFT,BOTTOM_RIGHT,TOP_RIGHT]
    polygons = np.array([REGION_OF_INTEREST])
    polygon_mask = np.zeros_like(img) # creating triangle mask for image

    cv.fillPoly(polygon_mask,polygons,255) # fill mask with white triangle
    masked_image = cv.bitwise_and(img,polygon_mask)

    return masked_image

def map_regions_of_interest(img):
    plt.imshow(img)
    plt.show()


def display_lane_lines(img,lines):
    line_image = np.zeros_like(img)
    left_lines = []
    right_lines = []
    straight_lines = []
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2 = line.reshape(4)
            slope = (x2-x1) / (y2-y1)
            if slope<0:
                left_lines.append(line)
            elif slope > 0:
                right_lines.append(line)
            else:
                straight_lines.append(line)

        left_slope, left_intercept = np.mean([(y2 - y1) / (x2 - x1) for line in left_lines for x1, y1, x2, y2 in line]), np.mean([y1 - (y2 - y1) / (x2 - x1) * x1 for line in left_lines for x1, y1, x2, y2 in line])
        right_slope, right_intercept = np.mean([(y2 - y1) / (x2 - x1) for line in right_lines for x1, y1, x2, y2 in line]), np.mean([y1 - (y2 - y1) / (x2 - x1) * x1 for line in right_lines for x1, y1, x2, y2 in line])

        if left_slope < 0 and right_slope > 0:
            direction = 'left'
        elif left_slope > 0 and right_slope < 0:
            direction = 'right'
        else:
            direction = 'straight'

        print('Direction:', direction)
            
        cv.line(line_image, (x1,y1),(x2,y2), (255,0,255),10)
        
        return line_image, direction
    
    return None, "Straight"

    

if __name__ == '__main__':
    cap = cv.VideoCapture("video2.mp4")
    while True:
        _, img = cap.read()
        grey_image = blurAndGrayscale(img)
        canny_img = canny(grey_image)
        # map_regions_of_interest(canny_img)

        cv.imshow("Canny image",canny_img)
        roi_image = capture_region_of_interest(canny_img)

        # roi_GREY = capture_region_of_interest(img)
        # roi_GREY = cv.cvtColor(roi_GREY,cv.COLOR_BGR2GRAY)
        cv.imshow("Region of interest",roi_image)

        lines = cv.HoughLinesP(roi_image, rho=1, theta=np.pi/180, threshold=100, minLineLength=50, maxLineGap=10)

        lane_detected_img, direction = display_lane_lines(img,lines)
        if lane_detected_img is not None:
            font = cv.FONT_HERSHEY_SIMPLEX

            cv.putText(img,direction,(0,50), font,3, (0, 255, 0), 2, cv.LINE_AA)
            combo_image = cv.addWeighted(lane_detected_img,0.8,img,1,0)

            cv.imshow("Lane detected image",combo_image)

        if (cv.waitKey(25) & 0xFF) == ord('q'):
            cv.destroyAllWindows()
            break

       
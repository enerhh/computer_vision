import cv2
import math

camera = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
# output = cv2.VideoWriter('gait.avi', fourcc, 5, (640, 480), 1)
global p1
global p2
global p3
global p4
global center_1


def get_center(contour):
    m = cv2.moments(contour)
    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])
    return cx, cy


def get_angle(p1, p2, p3, p4):
    return math.atan2(p1[1] - p2[1], p1[0] - p2[0]) * 180, \
           math.atan2(p3[1] - p4[1], p3[0] - p4[0]) * 180


while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 230, 255)
    __, contours, __ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    while len(contours) == 4:
        center_1, center_2, center_3, center_4 = get_center(contours[0]), get_center(contours[1]), \
                                                 get_center(contours[2]), get_center(contours[3])

    get_angle(center_1, center_2, center_3, center_4)
    cnt1 = cv2.circle(frame, center_1, 5, (0, 0, 0), 3)
    cnt2 = cv2.circle(frame, center_2, 5, (0, 0, 0), 3)
    cnt3 = cv2.circle(frame, center_3, 5, (0, 0, 0), 3)
    cnt4 = cv2.circle(frame, center_4, 5, (0, 0, 0), 3)
    cv2.line(frame, center_1, center_2, (0, 0, 255), 2)
    cv2.line(frame, center_2, center_3, (0, 255, 0), 2)
    cv2.line(frame, center_3, center_4, (255, 0, 0), 2)

    cv2.namedWindow('gait', cv2.WINDOW_NORMAL)
    cv2.imshow('gait', frame)

    k = cv2.waitKey(1000 / 5) & 0xFF
    if k == 27:
        break
camera.release()
# output.release()
cv2.destroyAllWindows()
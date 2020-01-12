import cv2
import math
import numpy as np

camera = cv2.VideoCapture(0)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 5.0, (1280,720))
font = cv2.FONT_HERSHEY_SIMPLEX
text_file = open("Output.txt", "w")
global p1
global p2
global p3
global p
global theta1
global theta2
global beta
global alfa
global delta


while True:
    ret, frame = camera.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 100, 200)
    blur = cv2.GaussianBlur(canny,(5,5),0)
    __, contours, __ = cv2.findContours(blur, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)


    def get_center(contour):
        m = cv2.moments(contour)
        cx = int(m["m10"] / m["m00"])
        cy = int(m["m01"] / m["m00"])
        return cx, cy


    def get_angle(p1, p2, p3, p4):
        beta = round((math.degrees(math.atan2(p3[0] - p4[0], p3[1] - p4[1]))), 2)
        P2 = math.sqrt(pow((p3[0] - p4[0]), 2) + pow((p3[1] - p4[1]), 2))
        P3 = math.sqrt(pow((p2[0] - p4[0]), 2) + pow((p2[1] - p4[1]), 2))
        P4 = math.sqrt(pow((p2[0] - p3[0]), 2) + pow((p2[1] - p3[1]), 2))
        alfa = round(math.degrees(math.acos((P2 ** 2 + P4 ** 2 - P3 ** 2) / (2 * P2 * P4))))
        Pi1 = math.sqrt(pow((p2[0] - p3[0]), 2) + pow((p2[1] - p3[1]), 2))
        Pi2 = math.sqrt(pow((p1[0] - p3[0]), 2) + pow((p1[1] - p3[1]), 2))
        Pi3 = math.sqrt(pow((p1[0] - p2[0]), 2) + pow((p1[1] - p2[1]), 2))
        delta = round(math.degrees(math.acos((Pi1 ** 2 + Pi3 ** 2 - Pi2 ** 2) / (2 * Pi1 * Pi3))))
        print(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1])
        cv2.putText(frame, "cadera: ", (840, 50), font, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, "rodilla: ", (840, 100), font, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, "tobillo: ", (840, 150), font, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, str(beta), (920, 50), font, 0.5, (255, 255, 255),2)
        cv2.putText(frame, str(alfa), (920, 100), font, 0.5, (255, 255, 255), 2)
        cv2.putText(frame, str(delta), (920, 150), font, 0.5, (255, 255, 255), 2)
        print(beta, alfa, delta, file=text_file)
        return beta, alfa, delta, #theta1, theta2, beta


    cv2.drawContours(frame, contours, 0, (255, 255, 255), 1)
    for c in contours:
        (x, y), rad = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        rad = int(rad)
        cv2.circle(frame, center, rad, (255, 0, 0), 5)
        center_1, center_2, center_3, center_4 = get_center(contours[0]), get_center(contours[1]), \
                                                 get_center(contours[2]), get_center(contours[3])
        print(get_angle(center_1, center_2, center_3, center_4))
        cnt1 = cv2.circle(frame, center_1, 5, (255, 0, 0), -1)
        cnt2 = cv2.circle(frame, center_2, 5, (0, 255, 0), -1)
        cnt3 = cv2.circle(frame, center_3, 5, (0, 0, 255), -1)
        cnt4 = cv2.circle(frame, center_4, 5, (255, 0, 255), -1)
        cv2.line(frame, center_1, center_2, (0, 0, 255), 2)
        cv2.line(frame, center_2, center_3, (0, 255, 0), 2)
        cv2.line(frame, center_3, center_4, (255, 0, 0), 2)

    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    cv2.imshow('frame', frame)
    out.write(frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
camera.release()
out.release()
cv2.destroyAllWindows()
text_file.close()







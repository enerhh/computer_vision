import cv2
import math
import numpy as np
from tkinter import *

camera = cv2.VideoCapture(1)
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter('output.avi',fourcc, 10, (1024,768))
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


    def get_angle(p1):
        print(p1[0], p1[1],file=text_file)#file=text_file
        #cv2.putText(frame, str(delta), (920, 150), font, 0.5, (255, 255, 255), 2)
        return p1[0],p1[1]#beta, alfa, delta, #theta1, theta2, betaop


    cv2.drawContours(frame, contours, 0, (255, 255, 255), 1)
    for c in contours:
        (x, y), rad = cv2.minEnclosingCircle(c)
        center = (int(x), int(y))
        rad = int(rad)
        cv2.circle(frame, center, rad, (255, 0, 0), 5)
        center_1 = get_center(contours[0])
        print(get_angle(center_1))
        cnt1 = cv2.circle(frame, center_1, 5, (255, 0, 0), -1)

    cv2.imshow('frame', frame)
    out.write(frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break
camera.release()
out.release()
cv2.destroyAllWindows()
text_file.close()







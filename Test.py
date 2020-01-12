import cv2
import numpy
import math

# programa de prueba para trigonometria de cadera
# cuando el punto se encuentra en el lado izquierdo de la imagen es negativo y del lado derecho es positivo
img = cv2.imread('der4.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
canny = cv2.Canny(gray, 100, 250)
__, contours, __ = cv2.findContours(canny, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
text_file = open("Output.txt", "w")

global p1
global p2
global p3
global p
global theta1
global theta2


def get_center(contour):
    m = cv2.moments(contour)
    cx = int(m["m10"] / m["m00"])
    cy = int(m["m01"] / m["m00"])
    return cx, cy


def get_angle(p1, p2, p3, p4):
    beta = round((math.degrees(math.atan2(p3[0] - p4[0], p3[1] - p4[1]))), 2)
    P2 = math.sqrt(pow((p3[0]-p4[0]),2)+pow((p3[1]-p4[1]),2))
    P3 = math.sqrt(pow((p2[0]-p4[0]),2)+pow((p2[1]-p4[1]),2))
    P4 = math.sqrt(pow((p2[0]-p3[0]),2)+pow((p2[1]-p3[1]),2))
    alfa = round(math.degrees(math.acos((P2**2 + P4**2 - P3**2)/(2*P2*P4))))
    Pi1 = math.sqrt(pow((p2[0]-p3[0]),2)+pow((p2[1]-p3[1]),2))
    Pi2 = math.sqrt(pow((p1[0]-p3[0]),2)+pow((p1[1]-p3[1]),2))
    Pi3 = math.sqrt(pow((p1[0]-p2[0]),2)+pow((p1[1]-p2[1]),2))
    delta = round(math.degrees(math.acos((Pi1**2 + Pi3**2 - Pi2**2)/(2*Pi1*Pi3))))
    print(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], p4[0], p4[1])
    print((beta,alfa,delta), file=text_file)
    return beta, alfa, delta, #P2, P3, P4

if len(contours) == 4:
    center_1, center_2, center_3, center_4 = get_center(contours[0]), get_center(contours[1]), get_center(contours[2]),\
                                             get_center(contours[3])
    print(get_angle(center_1, center_2, center_3, center_4))

cnt1 = cv2.circle(img, center_1, 5, (255, 0, 0), -1)  # toe
cnt2 = cv2.circle(img, center_2, 5, (0, 255, 0), -1)  # ankle
cnt3 = cv2.circle(img, center_3, 5, (0, 0, 255), -1)  # knee
cnt4 = cv2.circle(img, center_4, 5, (255, 0, 255), -1)  # hip
cv2.line(img, center_1, center_2, (0, 0, 255), 2)
cv2.line(img, center_2, center_3, (0, 255, 0), 2)
cv2.line(img, center_3, center_4, (255, 0, 0), 2)


cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
text_file.close()
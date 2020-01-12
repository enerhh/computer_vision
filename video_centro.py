import cv2
import numpy as np
import math

cam=cv2.VideoCapture(0)
Kernel= np.ones((5,5),np.uint8)
fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
out = cv2.VideoWriter('output.avi',fourcc,5,(1280,720),1)

while True:
    ret,frame=cam.read()
    hsv=cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    rangomin=np.array([150, 200, 0])
    rangomax=np.array([250, 250, 230])
    mascara=cv2.inRange(hsv,rangomin,rangomax)
    opening=cv2.morphologyEx(mascara,cv2.MORPH_OPEN,Kernel)
    x,y,w,h=cv2.boundingRect(opening)

    # Centro de punto de marcador
    px=(x+w/2)
    py=(y+h/2)
    p=(px,py)
    c2=cv2.circle(frame,p,2,(0,0,255),-1)

    # Centro de punto fijo en imagen (isight 640x360)(logitech 320x240)
    p1x=640
    p1y=360
    p1=(p1x,p1y)
    c1=cv2.circle(frame,p1,10,(255,0,0),-1)

    # calculo de distancias entre punto fijo y marcador
    d=math.fabs(p1x-px)
    d1=d/6
    cv2.line(frame,p,p1,(255,0,0),2)
    font = cv2.FONT_HERSHEY_SIMPLEX
    cv2.putText(frame,str(d1),(p1x+20,p1y+30),font,1,(255,0,0))
    out.write(frame)
    print(d1)
    cv2.namedWindow('img', cv2.WINDOW_NORMAL)
    cv2.imshow('img',frame)
    out.write(frame)


    k=cv2.waitKey(1000/5) & 0xFF
    if k==27:
        break
cam.release()
out.release()
cv2.destroyAllWindows()




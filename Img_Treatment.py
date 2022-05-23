import cv2
import numpy as np
import glob
from Arduino_Stream import streamVid

def Cinza(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

def BrilhoContraste(img,B,C):
    return cv2.convertScaleAbs(img, alpha=C, beta=B)

def BGR(img):
    return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

def Thresh(img):
    return cv2.threshold(Cinza(img), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

def Blur(img, X, Y):
    return cv2.blur(img, (X, Y))

def Countor(img,thresh):
    cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for cnt in cnts:
        cv2.drawContours(img,cnt,-1,(0,0,0))
        #approx = cv2.contourArea(cnt)
    return img

def FindCircle(imgRaw,thresh_img,hImg,wImg):
    detected_circles = cv2.HoughCircles(thresh_img, cv2.HOUGH_GRADIENT, 1, 250, param1=50, param2=50, minRadius=0,maxRadius=0)
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]
            if (b - r + 1) < hImg and (a - r + 1) < hImg and (b + r + 1) < wImg and (a + r + 1) < wImg:
                cv2.circle(imgRaw, (a, b), r, (255, 0, 0), 2)
                cv2.circle(imgRaw, (a, b), 1, (0, 0, 255), 3)
                return imgRaw[b - r + 1:b + r + 1, a - r + 1:a + r + 1]

def FindPoints(x1, y1, x2, y2, X1, Y1, X2, Y2):
    x5 = max(x1, X1)
    y5 = max(y1, Y1)
    x6 = min(x2, X2)
    y6 = min(y2, Y2)
    if (x5 > x6 or y5 > y6):
        return False
    else:
        return True

def RecInsideRec(x1, y1, x2, y2, X1, Y1, X2, Y2):
    if X1<x1<X2 and Y1<y1<Y2 and X1<x2<X2 and Y1<y2<Y2:
        return True
    else:
        return False

def RecVideo(name):
    for f in range(30):
        streamVid(f"{name}{f}")

    frameSize = (320, 240)

    out = cv2.VideoWriter(f"C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\Esp32Pics\\Videos\\output_video.avi", cv2.VideoWriter_fourcc(*'DIVX'), 10, frameSize)

    for filename in glob.glob(f"C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\Esp32Pics\\Videos\\Temp\\*.jpg"):
        img = cv2.imread(filename)
        out.write(img)

    out.release()

def CutDisc(Frame):
    return Frame[0:320,0:240]

#RecVideo("test")



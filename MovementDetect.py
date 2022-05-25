import cv2
from Img_Treatment import RecVideo, ClearTempFrames


def Spinnig():
    RecVideo("frame")
    image = cv2.imread('Esp32-Cam\\TempFrames\\frame0.jpg')
    image = image[105:145, 125:170]
    #cv2.imshow("teste", image)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram = cv2.calcHist([gray_image], [0],
                             None, [256], [0, 256])

    # data1 image
    image = cv2.imread('Esp32-Cam\\TempFrames\\frame9.jpg')
    image = image[105:145, 125:170]
    #cv2.imshow("teste2", image)
    gray_image1 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram1 = cv2.calcHist([gray_image1], [0],
                              None, [256], [0, 256])

    # data2 image
    image = cv2.imread('Esp32-Cam\\TempFrames\\frame4.jpg')
    image = image[105:145, 125:170]
    #cv2.imshow("teste3", image)
    #cv2.waitKey(0)
    gray_image2 = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    histogram2 = cv2.calcHist([gray_image2], [0],
                              None, [256], [0, 256])

    c1, c2 = 0, 0

    # Euclidean Distance between data1 and test
    i = 0
    while i < len(histogram) and i < len(histogram1):
        c1 += (histogram[i] - histogram1[i]) ** 2
        i += 1
    c1 = c1 ** (1 / 2)

    # Euclidean Distance between data2 and test
    i = 0
    while i < len(histogram) and i < len(histogram2):
        c2 += (histogram[i] - histogram2[i]) ** 2
        i += 1
    c2 = c2 ** (1 / 2)
    c3 = int((c1+c2)/2)
    if c3 < 67:
        print("Parada",c1,c2,c3)
        #ClearTempFrames()
        return False
    else:
        print("Movendo",c1,c2,c3)
        #ClearTempFrames()
        return True


Spinnig()
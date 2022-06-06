import cv2
import numpy as np
from Arduino_Stream import stream
from Img_Treatment import FindPoints, RecInsideRec



def ExecuteIA(im):

    #Localização dos Digitos na imagem
    '''
    XHi = 20
    XHf = 310
    YHi = 40
    YHf = 140



    XHi = 200
    XHf = 700
    YHi = 250
    YHf = 400

    XHi = 99
    XHf = 197
    YHi = 75
    YHf = 107
    '''
    A_cali_File = open("data\\cali.txt","r")
    A_cali = str(A_cali_File.read()).split()
    XHi, XHf, YHi, YHf = A_cali
    XHi = int(XHi)
    XHf = int(XHf)
    YHi = int(YHi)
    YHf = int(YHf)


    #######   training part    ###############
    samples = np.loadtxt('generalsamples.data', np.float32)
    responses = np.loadtxt('generalresponses.data', np.float32)
    responses = responses.reshape((responses.size, 1))

    model = cv2.ml.KNearest_create()
    trainingData = cv2.ml.TrainData_create(samples, 0, responses)
    # model = function.ModelFunction()
    model.train(trainingData)

    ############################# testing part  #########################

    # im = cv2.imread('C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\imgtest20.png')
    out = np.zeros(im.shape, np.uint8)
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cv2.rectangle(im, (XHi, YHi), (XHf, YHf), (0, 0, 255), 2)
    retlist = []
    for cnt in contours:
        draw = 0
        if 50 < cv2.contourArea(cnt) < 800:
            [x, y, w, h] = cv2.boundingRect(cnt)
            if retlist:
                for r in retlist:
                    if FindPoints(r[0], r[1], r[2], r[3], x, y, x + w, y + h):
                        draw += 1
            if draw == 0 and RecInsideRec(x, y, x + w, y + h, XHi, YHi, XHf, YHf):
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                roismall = roismall.reshape((1, 100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k=1)
                string = str(int((results[0][0])))
                if str(string) != "x":
                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(im, string, (x, y + h), 0, 1, (255, 0, 0))
                    retlist.append([x, y, x + w, y + h])


    cv2.imshow('im', im)
    # cv2.imshow('out',out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    #stream()
    #im = cv2.imread( "Esp32-Cam\\TempPics\\frame.jpg")
    #ExecuteIA(im)



    #stream()
    #im = cv2.imread(f"C:\\Users\\AUGEN12\\PycharmProjects\\HidroReader\\Esp32Pics\\Pics\\frame.jpg")
    #ExecuteIA(im)

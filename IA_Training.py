import numpy as np
import cv2
import time
from Img_Treatment import RecInsideRec
from Arduino_Stream import stream

#XHi = 200
#XHf = 700
#YHi = 250
#YHf = 400


def trainData(im, responses, samples, auto, ent, A_cali):
    XHi, XHf, YHi, YHf = A_cali
    XHi = int(XHi)
    XHf = int(XHf)
    YHi = int(XHi)
    YHf = int(XHf)
    im3 = im.copy()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    #################      Now finding Contours         ###################

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    keys = [i for i in range(48, 58)]

    for cnt in contours:
        cont = -1
        if cv2.contourArea(cnt) > 50:
            [x, y, w, h] = cv2.boundingRect(cnt)

            if h > 28 and RecInsideRec(x, y, x + w, y + h, XHi, YHi, XHf, YHf):
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print(f'x:{x}\ny:{y}\nw:{w}\nh:{h}')
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                cv2.imshow('norm', im)
                if auto:
                    responses.append(ent[cont])
                    sample = roismall.reshape((1, 100))
                    samples = np.append(samples, sample, 0)
                    cont -= 1
                else:
                    key = cv2.waitKey(0)

                    if key == 27:  # (escape to quit)
                        return responses, samples, True
                        # sys.exit()

                    elif key in keys and key != 32:
                        responses.append(int(chr(key)))
                        sample = roismall.reshape((1, 100))
                        samples = np.append(samples, sample, 0)
    if auto:
        print(ent)
        time.sleep(12)
        ent += 1
        if ent <= 200000:
            stream()
            im = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")
            trainData(im, responses, samples, auto, ent, A_cali)
        else:
            SaveTrainData(responses, samples)

    else:
        return responses, samples, False


def SaveTrainData(responses, samples):
    responses = np.array(responses, np.float32)
    responses = responses.reshape((responses.size, 1))
    print("training complete")

    np.savetxt('data\\generalsamples.data', samples)
    np.savetxt('data\\generalresponses.data', responses)


response = []
samples = np.empty((0, 100))
im = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")
# trainData(im, response, samples, True, 199990)

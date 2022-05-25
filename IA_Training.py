import numpy as np
import cv2


def trainData(im, responses, samples):

    im3 = im.copy()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blur, 255, 1, 1, 11, 2)

    #################      Now finding Contours         ###################

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)



    keys = [i for i in range(48, 58)]

    for cnt in contours:
        if cv2.contourArea(cnt) > 50:
            [x, y, w, h] = cv2.boundingRect(cnt)

            if h > 28:
                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
                print(f'x:{x}\ny:{y}\nw:{w}\nh:{h}')
                roi = thresh[y:y + h, x:x + w]
                roismall = cv2.resize(roi, (10, 10))
                cv2.imshow('norm', im)
                key = cv2.waitKey(0)

                if key == 27:  # (escape to quit)
                    return responses, samples, True
                    #sys.exit()

                elif key in keys and key != 32:
                    responses.append(int(chr(key)))
                    sample = roismall.reshape((1, 100))
                    samples = np.append(samples, sample, 0)
    return responses, samples, False


def SaveTrainData(responses, samples):
    responses = np.array(responses, np.float32)
    responses = responses.reshape((responses.size, 1))
    print("training complete")

    np.savetxt('generalsamples.data', samples)
    np.savetxt('generalresponses.data', responses)
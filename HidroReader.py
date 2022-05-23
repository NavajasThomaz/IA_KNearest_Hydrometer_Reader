import cv2
import numpy as np

from Arduino_Stream import stream
from Img_Treatment import *
from IA_Training import *
from Digits_Recognize import *

response = []
samples = np.empty((0, 100))

while True:

    #Chama o stream
    #stream()

    #Abre a imagem crua
    imgRaw = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")

    #Pega as dimensões da imagem crua
    hImg, wImg, _ = imgRaw.shape

    #print(hImg,wImg) #Dimensões

    #Nivel dos filtros
    Contraste = 0.5  # Contrast control (1.0-3.0)
    Brilho = 25  # Brightness control (0-100)
    #adjusted = BrilhoContraste(imgRaw,Brilho,Contraste)

    #Img cinza
    #gray = Cinza(adjusted)

    #ImgBGR
    #bgr = BGR(adjusted)

    #Thresh binário(Preto e branco bruto)
    #thresh_img = Thresh(imgRaw)

    #Img cinza/borrada
    X_Amount = 3
    Y_Amount = 3
    #gray_blurred = Blur(gray,X_Amount,Y_Amount)

    #Desenha os contornos
    #Contornado = Countor(imgRaw,thresh_img)


    #Procura e desenha circulos
    #Circlos = FindCircle(imgRaw,thresh_img,hImg,wImg)

    #faz a leitura dos digitos
    #leitura = pytesseract.image_to_string(bgr)
    #boxes = pytesseract.image_to_boxes(bgr)

    #for b in boxes.splitlines():
        #b = b.split(' ')

    #x, y, w, h = int(b[1]), int(b[2]), int(b[3]), int(b[4])
    #cv2.rectangle(imgRaw, (x, hImg - y), (w, hImg - h), (50, 50, 255), 1)
    #cv2.putText(imgRaw, b[0], (x, hImg - y + 13), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (50, 205, 50), 1)

    #Sem litura
    #if leitura.strip() == "":
        #print(f"(Sem Leitura)")
        #cv2.putText(imgRaw, "Sem Leitura", (int(hImg / 3), int(wImg / 3)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 255), 2)

    #Com leitura
    #else:
        #print(f"{leitura.strip()}")
        #cv2.putText(imgRaw, f"{leitura.strip()}", (int(hImg / 3), int(wImg / 3)), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0), 2)

    #Resultados
    #cv2.imshow('Pre', imgRaw)
    #cv2.imshow('Binary', thresh_img)
    #cv2.imshow('Box', sla)
    #time.sleep(1)
    #cv2.waitKey()
    #cv2.destroyAllWindows()

    response, samples, quit = trainData(imgRaw,response,samples)
    if quit:
        break
    #cv2.waitKey(0)
SaveTrainData(response,samples)
    #ExecuteIA(imgRaw)

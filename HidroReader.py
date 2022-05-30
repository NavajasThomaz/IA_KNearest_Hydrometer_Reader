import cv2
import numpy as np
from Arduino_Stream import stream
from Img_Treatment import *
from IA_Training import *
from Digits_Recognize import *
from tkinter import *
global imgRaw, showing, btBk


showing = False



def CloseAll(showing):
    if showing:
        cv2.destroyAllWindows()
    window.destroy()


def ButtonsGetVid(But, winVidName):
    name = But.get()
    RecVideo(f"{name}")
    winVidName.destroy()


def ButtonsGetBrCo(brilho, constraste, winBrCo):
    # Nivel dos filtros
    # Contraste = 0.5  # Contrast control (1.0-3.0)
    # Brilho = 25  # Brightness control (0-100)
    global imgRaw
    Brilho = brilho.get()
    Contraste = constraste.get()
    winBrCo.destroy()
    imgRaw = BrilhoContraste(imgRaw, int(Brilho), float(Contraste))
    return cv2.imshow("PREVIEW", imgRaw)


def ButtonsGetBlur(X, Y, winBrCo):
    global imgRaw
    X_Amount = X.get()
    Y_Amount = Y.get()
    winBrCo.destroy()
    imgRaw = Blur(imgRaw, int(X_Amount), int(Y_Amount))
    return cv2.imshow("PREVIEW", imgRaw)


def TakePhoto(showing):
    #Fecha se ouver alguma imagem aberta
    if showing:
        cv2.destroyAllWindows()
    BrCoButton["background"] = '#CCDAD1'
    GrayButton["background"] = '#CCDAD1'
    BGRButton["background"] = '#CCDAD1'
    BinButton["background"] = '#CCDAD1'
    BlurButton["background"] = '#CCDAD1'
    ContButton["background"] = '#CCDAD1'
    CircButton["background"] = '#CCDAD1'
    CutsButton["background"] = '#CCDAD1'
    TrainButton["background"] = '#6F6866'

    #Chama o stream
    stream()

    #Abre imagem crua
    #imgRaw = cv2.imread('C:\\Users\\AUGEN12\\PycharmProjects\\IA_KNearest_Hydrometer_Readers\\imgTest20.png')
    global imgRaw
    imgRaw = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")

    # Pega as dimensões da imagem crua


    cv2.imshow("Photo", imgRaw)
    return imgRaw


def TakeVid(showing):
    #Fecha se ouver alguma imagem aberta
    if showing:
        cv2.destroyAllWindows()
    winVidName = Tk()
    nametitle = Label(winVidName, text="Nome para o Video:")
    nametitle.grid(column=0,row=0)
    nameEnt = Entry(winVidName)
    nameEnt.grid(column=0,row=1)
    nameBut = Button(winVidName, text="OK", command=lambda: ButtonsGetVid(nameEnt,winVidName))
    nameBut.grid(column=0,row=2)
    winVidName.mainloop()
    #Chama o stream


    #Abre a imagem crua
    imgRaw = cv2.imread('C:\\Users\\AUGEN12\\PycharmProjects\\IA_KNearest_Hydrometer_Readers\\imgTest20.png')
    #imgRaw = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")
    cv2.imshow("Photo", imgRaw)


def contBri(showing):
    global imgRaw
    if showing:
        copy = imgRaw.copy()
        cv2.destroyAllWindows()
    winBrCo = Tk()
    Btitle = Label(winBrCo, text="Brilho:")
    Btitle.grid(column=0, row=0)
    BEnt = Entry(winBrCo)
    BEnt.grid(column=0, row=1)
    Ctitle = Label(winBrCo, text="Constraste:")
    Ctitle.grid(column=0, row=2)
    CEnt = Entry(winBrCo)
    CEnt.grid(column=0, row=3)
    BCBut = Button(winBrCo, text="OK", command=lambda: ButtonsGetBrCo(BEnt, CEnt, winBrCo))
    BCBut.grid(column=0, row=4)
    winBrCo.mainloop()


def IA_Execute(showing):
    if showing:
        ExecuteIA(imgRaw, showing)


def gray(showing):
    #Img cinza
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    imgRaw = Cinza(imgRaw)
    return cv2.imshow("PREVIEW", imgRaw)


def BGR(showing):
    #ImgBGR
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    imgRaw = BGR(imgRaw)
    return cv2.imshow("PREVIEW", imgRaw)


def bin(showing):
    #Thresh binário(Preto e branco bruto)
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    imgRaw = Thresh(imgRaw)
    return cv2.imshow("PREVIEW", imgRaw)


def blur(showing):
    #Img cinza/borrada
    #X_Amount = 3
    #Y_Amount = 3
    if showing:
        cv2.destroyAllWindows()
    winBlur = Tk()
    Xtitle = Label(winBlur, text="X_Amount:")
    Xtitle.grid(column=0, row=0)
    XEnt = Entry(winBlur)
    XEnt.grid(column=0, row=1)
    Ytitle = Label(winBlur, text="Y_Amount:")
    Ytitle.grid(column=0, row=2)
    YEnt = Entry(winBlur)
    YEnt.grid(column=0, row=3)
    BCBut = Button(winBlur, text="OK", command=lambda: ButtonsGetBlur(XEnt, YEnt, winBlur))
    BCBut.grid(column=0, row=4)
    winBlur.mainloop()


def contour(showing):
    # Desenha os contornos
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    imgRaw = Countor(imgRaw)
    return cv2.imshow("PREVIEW", imgRaw)


def circulo(showing):
    #Procura e desenha circulos
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    return cv2.imshow("PREVIEW", FindCircle(imgRaw))


def train(showing):
    response = []
    samples = np.empty((0, 100))
    #Treina
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    response, samples, quit = trainData(imgRaw, response, samples, auto=True, ent=199999)
    return SaveTrainData(response,samples)


#Inicializa Interface
window = Tk()
window.title("IA_KNearest_Hydrometer_Reader")
window.configure(background="#dde")
#titulo = Label(window, text="|Augen|\nLeitor de Hidrometro", width=10,height=1,padx=20,pady=10)
#titulo.grid(column=0,row=0)

#Cria os Botões
but_wid = 10
but_hei = 1
px = 20
py = 10
btbkC = '#515751'

#Tira Foto
streamButton = Button(window, text="Take Photo", command=lambda: TakePhoto(showing), width=but_wid, height=but_hei, padx=px, pady=py)
showing = True
streamButton.grid(column=0,row=1)

#Faz video
streamVidButton = Button(window, text="Gravar Video", command=lambda: TakeVid(showing), width=but_wid, height=but_hei, padx=px, pady=py)
showing = True
streamVidButton.grid(column=0,row=2)

#Filtro de brilho e contraste
BrCoButton = Button(window, text="Brilho/Contraste", command=lambda: contBri(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
BrCoButton.grid(column=0,row=3)

#Cinza
GrayButton = Button(window, text="Cinza", command=lambda: gray(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
GrayButton.grid(column=0,row=4)

#BGR
BGRButton = Button(window, text="BGR", command=lambda: BGR(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
BGRButton.grid(column=0,row=5)

#Binário
BinButton = Button(window, text="Binário", command=lambda: bin(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
BinButton.grid(column=0,row=6)

#Blur
BlurButton = Button(window, text="Blur", command=lambda: blur(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
BlurButton.grid(column=0,row=7)

#Contornos
ContButton = Button(window, text="Contornos", command=lambda: contour(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
ContButton.grid(column=1,row=1)

#Circulos
CircButton = Button(window, text="Circulos", command=lambda: circulo(showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
CircButton.grid(column=1,row=2)

#Cortes
CutsButton = Button(window, text="Cortes", command=lambda: (showing), width=but_wid, height=but_hei, padx=px, pady=py, background=btbkC)
showing = True
CutsButton.grid(column=1,row=3)

#Giro
GiroButton = Button(window, text="Girando", command=lambda: TakeVid(showing), width=but_wid, height=but_hei, padx=px, pady=py, background='#38302E')
showing = True
GiroButton.grid(column=1,row=5)

#Treino
TrainButton = Button(window, text="Treinar", command=lambda: train(showing), width=but_wid, height=but_hei, padx=px, pady=py, background='#38302E')
showing = True
TrainButton.grid(column=1,row=4)

#Reconhecimento
IAButton = Button(window, text="Reconhecer", command=lambda: IA_Execute(showing), width=but_wid, height=but_hei, padx=px, pady=py, background='#38302E')
showing = True
IAButton.grid(column=1,row=6)

#Quit
QuitButton = Button(window, text="Quit", command=lambda: CloseAll(showing), width=but_wid, height=but_hei, padx=px, pady=py)
showing = True
QuitButton.grid(column=1,row=7)

#Loop Janela

window.mainloop()

#x:99
#y:75
#w:98
#h:32

#im = im[99:75, 98 + 99:75 + 32]
#imgCut = imgRaw#[0:385, 0:700]
#imgZ = image_resize(imgCut,196,64)
#
#cv2.waitKey(0)
#


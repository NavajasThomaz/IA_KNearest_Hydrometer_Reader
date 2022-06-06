import tkinter
import cv2
import numpy as np
from Arduino_Stream import stream
from Img_Treatment import *
from IA_Training import *
from Digits_Recognize import *
from tkinter import *
from tkinter import filedialog

global imgRaw, showing, btBk

showing = False

TreWindow = Tk()
TreWindow.title("Filters")
TreWindow.configure(background="#C4C4C4")
IaWindow = Tk()
IaWindow.title("I.A.")
IaWindow.configure(background='#4361EE')

brco = tkinter.IntVar()
cinza = tkinter.IntVar()
bgr = tkinter.IntVar()
bina = tkinter.IntVar()
blu = tkinter.IntVar()
cont = tkinter.IntVar()
cut = tkinter.IntVar()


def browseFiles(showing):
    global imgRaw
    if showing:
        cv2.destroyAllWindows()
    filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                          filetypes=(("Pngs", "*.png*"), ("Jpegs", "*.jpg*"), ("all files", "*.*")))

    # Change label contents
    label_file_explorer.configure(text=filename.split("/")[-1], fg="green")
    imgRaw = cv2.imread(filename)
    preview = cv2.imshow("PREVIEW", imgRaw)
    return preview


def ButtonsGetVid(But, winVidName):
    name = But.get()
    RecVideo(f"{name}")
    winVidName.destroy()


def TakePhoto(showing):
    # Fecha se ouver alguma imagem aberta
    if showing:
        cv2.destroyAllWindows()

    # Chama o stream
    stream()

    # Abre imagem crua
    # imgRaw = cv2.imread('C:\\Users\\AUGEN12\\PycharmProjects\\IA_KNearest_Hydrometer_Readers\\imgTest20.png')
    global imgRaw
    imgRaw = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")

    # Pega as dimensões da imagem crua

    cv2.imshow("Photo", imgRaw)
    return imgRaw


def TakeVid():
    # Fecha se houver alguma imagem aberta
    winVidName = Tk()
    nametitle = Label(winVidName, text="Nome para o Video:")
    nametitle.grid(column=0, row=0)
    nameEnt = Entry(winVidName)
    nameEnt.grid(column=0, row=1)
    nameBut = Button(winVidName, text="OK", command=lambda: ButtonsGetVid(nameEnt, winVidName))
    nameBut.grid(column=0, row=2)
    winVidName.mainloop()
    # Chama o stream

    # Abre a imagem crua
    imgRaw = cv2.imread('C:\\Users\\AUGEN12\\PycharmProjects\\IA_KNearest_Hydrometer_Readers\\imgTest20.png')
    # imgRaw = cv2.imread("Esp32-Cam\\TempPics\\frame.jpg")
    cv2.imshow("Photo", imgRaw)


def ButtonsGetBrCo(brilho, constraste, winBrCo):
    # Nivel dos filtros
    # Contraste = 0.5  # Contrast control (1.0-3.0)
    # Brilho = 25  # Brightness control (0-100)
    global imgRaw
    Brilho = brilho.get()
    Contraste = constraste.get()
    winBrCo.destroy()
    imgRaw = BrilhoContraste(imgRaw, int(Brilho), float(Contraste))
    return imgRaw


def IA_Execute(imgRaw):
    ExecuteIA(imgRaw)


def circulo():
    # Procura e desenha circulos
    global imgRaw
    return cv2.imshow("PREVIEW", FindCircle(imgRaw))


def Cali(imgRaw):
    imgH, imgW, imgC = imgRaw.shape

    cv2.destroyAllWindows()
    trackWinCv = cv2.namedWindow("Cutting")
    cv2.resizeWindow("Cutting", 640, 240)
    cv2.createTrackbar("X_Amount", "Cutting", 0, imgW, Empty)
    cv2.createTrackbar("Y_Amount", "Cutting", 0, imgH, Empty)
    cv2.createTrackbar("Wid", "Cutting", imgW, imgW, Empty)
    cv2.createTrackbar("Hei", "Cutting", imgH, imgH, Empty)
    while True:
        X_Track = cv2.getTrackbarPos("X_Amount", "Cutting")
        Y_Track = cv2.getTrackbarPos("Y_Amount", "Cutting")
        X_Point = cv2.getTrackbarPos("Wid", "Cutting")
        Y_Point = cv2.getTrackbarPos("Hei", "Cutting")
        key = cv2.waitKey(1)
        if (X_Point != 0) and (Y_Point != 0):
            temp = imgRaw.copy()
            cv2.imshow("PREVIEW", Calibrar(temp, X_Track, Y_Track, X_Point, Y_Point))
        if key == 27:
            A_cali = [X_Track, X_Point, Y_Track, Y_Point]
            cv2.destroyAllWindows()
            save = open("data\\cali.txt",'w')
            save.write(f"{X_Track} {X_Point} {Y_Track} {Y_Point}")
            save.close()
            print(str(A_cali))
            break


def train(imgRaw):
    A_cali_file = open("data\\cali.txt","r")
    A_cali = str(A_cali_file.read()).split()

    # Treina
    response = []
    samples = np.empty((0, 100))
    response, samples, quit = trainData(imgRaw, response, samples, auto=False, ent=199999, A_cali=A_cali)
    return SaveTrainData(response, samples)


def Empty(a):
    pass


def Done(imgRaw):
    if brco.get() == 1:
        cv2.destroyAllWindows()
        trackWinCv = cv2.namedWindow("Brilho e Constraste")
        cv2.resizeWindow("Brilho e Constraste", 640, 240)
        cv2.createTrackbar("Brilho", "Brilho e Constraste", 1, 100, Empty)
        cv2.createTrackbar("Contraste", "Brilho e Constraste", 1, 100, Empty)
        print("Blur")
        while True:
            Brilho = cv2.getTrackbarPos("Brilho", "Brilho e Constraste")
            Contraste = cv2.getTrackbarPos("Contraste", "Brilho e Constraste")
            key = cv2.waitKey(1)
            if (Brilho != 0) and (Contraste != 0):
                preview = cv2.imshow("PREVIEW", BrilhoContraste(imgRaw, Brilho, Contraste))
            if key == 27:
                cv2.destroyAllWindows()
                imgRaw = BrilhoContraste(imgRaw, Brilho, Contraste)
                break
        print("Brilho contraste")
    if cinza.get() == 1:
        imgRaw = Cinza(imgRaw)
        print("Cinza")
    if bgr.get() == 1:
        imgRaw = BGR(imgRaw)
        print("BGR")
    if bina.get() == 1:
        imgRaw = Thresh(imgRaw)
        print("Binário")
    if blu.get() == 1:
        cv2.destroyAllWindows()
        trackWinCv = cv2.namedWindow("Trackers")
        cv2.resizeWindow("Trackers", 640, 240)
        cv2.createTrackbar("X_Amount", "Trackers", 0, 50, Empty)
        cv2.createTrackbar("Y_Amount", "Trackers", 0, 50, Empty)
        print("Blur")
        while True:
            X_Track = cv2.getTrackbarPos("X_Amount", "Trackers")
            Y_Track = cv2.getTrackbarPos("Y_Amount", "Trackers")
            key = cv2.waitKey(1)
            if (X_Track != 0) and (Y_Track != 0):
                cv2.imshow("PREVIEW", Blur(imgRaw, X_Track, Y_Track))
            if key == 27:
                cv2.destroyAllWindows()
                imgRaw = Blur(imgRaw, X_Track, Y_Track)
                break
    if cont.get() == 1:
        imgRaw = Countor(imgRaw)
        print("Contornos")
    if cut.get() == 1:
        imgH, imgW, imgC = imgRaw.shape
        cv2.destroyAllWindows()
        trackWinCv = cv2.namedWindow("Cutting")
        cv2.resizeWindow("Cutting", 640, 240)
        cv2.createTrackbar("X_Amount", "Cutting", imgW, imgW, Empty)
        cv2.createTrackbar("Y_Amount", "Cutting", imgH, imgH, Empty)
        cv2.createTrackbar("X_Point", "Cutting", 0, imgW, Empty)
        cv2.createTrackbar("Y_Point", "Cutting", 0, imgH, Empty)
        while True:
            X_Track = cv2.getTrackbarPos("X_Amount", "Cutting")
            Y_Track = cv2.getTrackbarPos("Y_Amount", "Cutting")
            X_Point = cv2.getTrackbarPos("X_Point", "Cutting")
            Y_Point = cv2.getTrackbarPos("Y_Point", "Cutting")
            key = cv2.waitKey(1)
            if (X_Track != 0) and (Y_Track != 0) and (X_Point != 0) and (Y_Point != 0):
                cv2.imshow("PREVIEW", imgRaw[X_Point:X_Track, Y_Point:Y_Track])
            if key == 27:
                cv2.destroyAllWindows()
                imgRaw = imgRaw[X_Point:X_Track, Y_Point:Y_Track]
                break
        print("Cortes")
    print("")
    return cv2.imshow("PREVIEW", imgRaw)


def CloseAll():
    cv2.destroyAllWindows()
    IniWindow.destroy()
    TreWindow.destroy()
    IaWindow.destroy()
    pass


def DisCinBin(cond):
    DisableCinza(cond)
    DisableBin(cond)


def DisCinCont(cond):
    DisableCinza(cond)
    DisableCont(cond)


def DisBinCont(cond):
    DisableBin(cond)
    DisableCont(cond)


def DisableCinza(cond):
    if cond == 1:
        GrayButton["state"] = DISABLED
    else:
        GrayButton["state"] = NORMAL


def DisableBin(cond):
    if cond == 1:
        BinButton["state"] = DISABLED
    else:
        BinButton["state"] = NORMAL


def DisableCont(cond):
    if cond == 1:
        ContButton["state"] = DISABLED
    else:
        ContButton["state"] = NORMAL


# Inicializa Interface
IniWindow = Tk()
IniWindow.title("IA_KNearest_Hydrometer_Reader")
IniWindow.configure(background="#C4C4C4")

label_file_explorer = Label(IniWindow,
                            text="Sem Imagem",
                            width=10,
                            height=1,
                            fg="red",
                            padx=20,
                            pady=10)
label_file_explorer.grid(column=1, row=1)

# titulo = Label(window, text="|Augen|\nLeitor de Hidrometro", width=10,height=1,padx=20,pady=10)
# titulo.grid(column=0,row=0)

# Cria os Botões
but_wid = 10
but_hei = 1
px = 20
py = 10
btbkF = '#C4C4C4'
btbkI = '#4361EE'
# 33CC99

button_explore = Button(IniWindow,
                        text="Escolher imagem",
                        command=lambda: browseFiles(showing),
                        width=but_wid,
                        height=but_hei,
                        padx=px,
                        pady=py)
button_explore.grid(column=0, row=1)

# Tira Foto
streamButton = Button(IniWindow,
                      text="Tirar Foto",
                      command=lambda: TakePhoto(showing=True),
                      width=but_wid,
                      height=but_hei,
                      padx=px,
                      pady=py)
streamButton.grid(column=0, row=2)

# Faz video
streamVidButton = Button(IniWindow,
                         text="Gravar Video",
                         command=lambda: TakeVid(),
                         width=but_wid,
                         height=but_hei,
                         padx=px,
                         pady=py)
streamVidButton.grid(column=1, row=2)

# Quit
QuitButton = Button(IniWindow,
                    text="Quit",
                    command=lambda: CloseAll(),
                    width=but_wid,
                    height=but_hei,
                    padx=px,
                    pady=py)
QuitButton.grid(column=0, row=3)

# Filtro de brilho e contraste
BrCoButton = Checkbutton(TreWindow,
                         text="Brilho/Contraste",
                         variable=brco,
                         justify=LEFT,
                         width=but_wid,
                         height=but_hei,
                         padx=px,
                         pady=py,
                         background=btbkF)
BrCoButton.grid(column=0, row=0)

# Cinza
GrayButton = Checkbutton(TreWindow,
                         text="Cinza",
                         justify=LEFT,
                         width=but_wid,
                         variable=cinza,
                         command=lambda: DisBinCont(cinza.get()),
                         height=but_hei,
                         padx=px,
                         pady=py,
                         background=btbkF)
GrayButton.grid(column=1, row=0)

# BGR
BGRButton = Checkbutton(TreWindow,
                        text="BGR",
                        justify=LEFT,
                        variable=bgr,
                        width=but_wid,
                        height=but_hei,
                        padx=px,
                        pady=py,
                        background=btbkF)
BGRButton.grid(column=0, row=1)

# Binário
BinButton = Checkbutton(TreWindow,
                        text="Binário",
                        justify=LEFT,
                        variable=bina,
                        command=lambda: DisCinCont(bina.get()),
                        width=but_wid,
                        height=but_hei,
                        padx=px,
                        pady=py,
                        background=btbkF)
BinButton.grid(column=1, row=1)

# Blur
BlurButton = Checkbutton(TreWindow,
                         text="Blur",
                         justify=LEFT,
                         variable=blu,
                         width=but_wid,
                         height=but_hei,
                         padx=px,
                         pady=py,
                         background=btbkF)
BlurButton.grid(column=0, row=2)

# Contornos
ContButton = Checkbutton(TreWindow,
                         text="Contornos",
                         justify=LEFT,
                         variable=cont,
                         command=lambda: DisCinBin(cont.get()),
                         width=but_wid,
                         height=but_hei,
                         padx=px,
                         pady=py,
                         background=btbkF)
ContButton.grid(column=1, row=2)

# Cortes
CutsButton = Checkbutton(TreWindow,
                         text="Cortes",
                         justify=LEFT,
                         variable=cut,
                         width=but_wid,
                         height=but_hei,
                         command=lambda: print(cut.get()),
                         padx=px,
                         pady=py,
                         background=btbkF)
CutsButton.grid(column=0, row=3)

# Pronto
DoneButton = Button(TreWindow,
                    text="Done",
                    command=lambda: Done(imgRaw),
                    width=but_wid,
                    height=but_hei,
                    padx=px,
                    pady=py,
                    background=btbkF)
DoneButton.grid(column=1, row=3)

# Calibração
CaliButton = Button(IaWindow,
                         text="Calibração",
                         justify=LEFT,
                         width=but_wid,
                         height=but_hei,
                         command=lambda: Cali(imgRaw),
                         padx=px,
                         pady=py,
                         background=btbkF)
CaliButton.grid(column=0, row=2)

# Treino
TrainButton = Button(IaWindow,
                     text="Treinar",
                     command=lambda: train(imgRaw),
                     width=but_wid,
                     height=but_hei,
                     padx=px,
                     pady=py,
                     background=btbkI)
TrainButton.grid(column=0, row=0)

# Giro
GiroButton = Button(IaWindow,
                    text="Girando",
                    command=lambda: TakeVid(),
                    width=but_wid,
                    height=but_hei,
                    padx=px,
                    pady=py,
                    background=btbkI)
GiroButton.grid(column=0, row=1)

# Reconhecimento
IAButton = Button(IaWindow,
                  text="Reconhecer",
                  command=lambda: IA_Execute(imgRaw),
                  width=but_wid,
                  height=but_hei,
                  padx=px,
                  pady=py,
                  background=btbkI)
IAButton.grid(column=1, row=0)

# Circulos
CircButton = Button(IaWindow,
                    text="Circulos",
                    command=lambda: circulo(),
                    width=but_wid,
                    height=but_hei,
                    padx=px,
                    pady=py,
                    background=btbkI)
CircButton.grid(column=1, row=1)





# Loop Janela
IniWindow.mainloop()
TreWindow.mainloop()
IaWindow.mainloop()


# x:99
# y:75
# w:98
# h:32

# im = im[99:75, 98 + 99:75 + 32]
# imgCut = imgRaw#[0:385, 0:700]
# imgZ = image_resize(imgCut,196,64)
#
# cv2.waitKey(0)
#

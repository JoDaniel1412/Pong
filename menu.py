from tkinter import *

# Variables
W2, H2 = 800, 600


main = Tk()
main.minsize(W2, H2)
main.resizable(NO, NO)
Fondo_pong = PhotoImage(file="img/Imagen de menu de pong.gif")

# Interface
def load_interface(xPoss, yPoss, xWidth, fgColor, bgColor, fonts):
    #Ventana de ajustes
    def ajustes():
        main.withdraw()
        ventana2 = Toplevel()
        ventana2.title("Ajustes")
        ventana2.minsize(W2, H2)
        ventana2.resizable(width=NO, height=NO)
        canvas2 = Canvas(ventana2, width=W2, height=H2, bg="black")
        canvas2.place(x=-1, y=0)

    mainCanvas = Canvas(main, width=W2, height=H2, bg=bgColor)
    mainCanvas.place(x=xPoss, y=yPoss)

    tittleLabel = Label(mainCanvas, image=Fondo_pong, borderwidth=0)
    tittleLabel.place(x=xPoss+5, y=yPoss-50)

    playersButton1 = Button(mainCanvas, text='1 Player', font=fonts +str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0)
    playersButton1.place(x=xPoss + 290, y=yPoss + 250)

    playersButton2 = Button(mainCanvas, text='2 Player', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0)
    playersButton2.place(x=xPoss + 290, y=yPoss + 310)

    playersOption = Button(mainCanvas, text='Options', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0, command=ajustes)
    playersOption.place(x=xPoss + 290, y=yPoss + 370)

    playersHightscore = Button(mainCanvas, text='Scores', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,justify=RIGHT, borderwidth=0)
    playersHightscore.place(x=xPoss + 290, y=yPoss + 430)


load_interface(0, 0, 10, 'white', 'black', 'Fixedsys ')

main.mainloop()
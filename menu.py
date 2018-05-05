from tkinter import *

# Variables
W2, H2 = 800, 600

main = Tk()
main.minsize(W2, H2)
main.resizable(NO, NO)


# Interface
def load_interface(xPoss, yPoss, xWidth, fgColor, bgColor, fonts):
    mainCanvas = Canvas(main, width=W2, height=H2, bg=bgColor)
    mainCanvas.place(x=xPoss, y=yPoss)

    tittleLabel = Label(mainCanvas, text='Pong', font="NokiaCellphone", fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT)
    tittleLabel.place(x=xPoss + 20, y=yPoss + 20)

    playersLabel = Label(mainCanvas, text='Players', font=fonts, fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT)
    playersLabel.place(x=xPoss + 20, y=yPoss + 100)


load_interface(0, 0, 10, 'white', 'black', 'Arial')

main.mainloop()

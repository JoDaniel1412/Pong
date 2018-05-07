from tkinter import *

# Variables
W2, H2 = 800, 600

main = Tk()
main.minsize(W2, H2)
main.resizable(NO, NO)
main.title('Pong')
Fondo_pong = PhotoImage(file="img/Imagen de menu de pong.gif")


# Interface
def load_interface(xPoss, yPoss, xWidth, fgColor, bgColor, fonts):
    # Ventana de ajustes
    def ajustes():
        def cerrar_ajustes():
            ventana2.destroy()
            main.deiconify()

        main.withdraw()

        ventana2 = Toplevel()
        ventana2.title("Ajustes")

        ventana2.minsize(W2, H2)
        ventana2.resizable(width=NO, height=NO)

        canvas2 = Canvas(ventana2, width=W2, height=H2, bg="black")
        canvas2.place(x=-1, y=0)

        settings = Label(canvas2, text="Ajustes", font=fonts + str(40), fg=fgColor, bg=bgColor)
        settings.place(x=290, y=10)

        dificultad = Label(canvas2, text="Seleccione dificultad", font=fonts + str(20), fg=fgColor, bg=bgColor)
        dificultad.place(x=230, y=420)

        facil = Button(canvas2, text="Facil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        facil.place(x=180, y=470)

        medio = Button(canvas2, text="Medio", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        medio.place(x=330, y=470)

        dificil = Button(canvas2, text="Dificil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        dificil.place(x=480, y=470)

        musica = Label(canvas2, text="Musica:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        musica.place(x=500, y=120)

        musica_on = Button(canvas2, text="On", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        musica_on.place(x=630, y=115)

        musica_off = Button(canvas2, text="Off", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        musica_off.place(x=690, y=115)

        sonido = Label(canvas2, text="Sonido:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        sonido.place(x=500, y=200)

        sonido_on = Button(canvas2, text="On", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        sonido_on.place(x=630, y=195)

        sonido_off = Button(canvas2, text="Off", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        sonido_off.place(x=690, y=195)

        escenario = Label(canvas2, text="Escoja escenario:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        escenario.place(x=40, y=120)

        clasico = Button(canvas2, text="Clasico", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        clasico.place(x=50, y=160)

        neon = Button(canvas2, text="Neon", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        neon.place(x=50, y=210)

        futbol = Button(canvas2, text="Futbol", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0)
        futbol.place(x=50, y=260)

        aceptar_ajustes = Button(canvas2, text="LISTO!", font=fonts + str(20), fg="black", bg="White", borderwidth=0)
        aceptar_ajustes.place(x=670, y=10)

        volver = Button(canvas2, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0,
                        command=cerrar_ajustes)
        volver.place(x=10, y=10)

    def puntuaciones():
        def cerrar_puntuciones():
            main.deiconify()
            ventana_scores.destroy()

        main.withdraw()

        ventana_scores = Toplevel()
        ventana_scores.title("Ingreso de Jugador")

        ventana_scores.minsize(W2, H2)
        ventana_scores.resizable(width=NO, height=NO)

        canvas_scores = Canvas(ventana_scores, width=W2, height=H2, bg="black")
        canvas_scores.place(x=-1, y=0)

        label_scores = Label(canvas_scores, text="Digite nombre de jugador:", font=fonts + str(20), fg=fgColor,
                             bg=bgColor)
        label_scores.place(x=40, y=120)

        escribir_jugadores = Entry(canvas_scores, width=30)
        escribir_jugadores.place(x=200, y=300)

        def agregar_scores():
            agregar_puntuaciones = open('Scores.txt', 'a')
            agregar_puntuaciones.write = (escribir_jugadores.get())

    def mostrar_puntuaciones():
        def cerrar_mostrar_puntuciones():
            main.deiconify()
            ventana__mostrar_scores.destroy()

        main.withdraw()

        ventana__mostrar_scores = Toplevel()
        ventana__mostrar_scores.title("Puntuaciones")

        ventana__mostrar_scores.minsize(W2, H2)
        ventana__mostrar_scores.resizable(width=NO, height=NO)

        canvas_mostrar_scores = Canvas(ventana__mostrar_scores, width=W2, height=H2, bg="black")
        canvas_mostrar_scores.place(x=-1, y=0)

        label_mejores = Label(canvas_mostrar_scores, text="Mejores Puntuaciones:", font=fonts + str(20), fg=fgColor,
                              bg=bgColor)
        label_mejores.place(x=200, y=120)

        canvas_tabla = Canvas(canvas_mostrar_scores, width=W2 // 2, height=H2 // 2)
        canvas_tabla.place(x=200, y=200)

        cerrar_scores = Button(canvas_mostrar_scores, text="BACK!", font=fonts + str(20), fg="black", bg="White",
                               borderwidth=0, command=cerrar_mostrar_puntuciones)
        cerrar_scores.place(x=5, y=0)

        def separarPuntuaciones(i):
            if i == len(listaScores):
                return
            listaScores[i] = listaScores[i].replace("\n", "").split(";")
            separarPuntuaciones(i + 1)

        file = open("Scores.txt", 'r')
        listaScores = file.readlines()
        separarPuntuaciones(0)
        file.close()

        def crearTabla(x, y, columns):
            global tabla
            if x == len(listaScores):
                return ''
            elif y == 2:
                tabla += [columns]
                return crearTabla(x + 1, 0, [])
            else:
                if y == 0:
                    seccion = Entry(canvas_tabla, text='', width=3, justify=CENTER)
                    seccion.grid(row=x, column=y)
                    return crearTabla(x, y + 1, columns + [seccion])
                seccion = Entry(canvas_tabla, text='', width=30)
                seccion.grid(row=x, column=y)
                return crearTabla(x, y + 1, columns + [seccion])

        # Llena la tabla anteriormente creada
        def llenarTabla(x, y):  # funcion que llena la tabla para vendedores con el vendedores.txt
            global tabla
            if x == len(listaScores):
                return
            elif y != 2:
                print(listaScores[x][y])
                tabla[x][y].insert(0, listaScores[x][y])
                return llenarTabla(x, y + 1)
            else:
                return llenarTabla(x + 1, 0)

        crearTabla(0, 0, [])
        llenarTabla(0, 0)
        tabla = []

    mainCanvas = Canvas(main, width=W2, height=H2, bg=bgColor)
    mainCanvas.place(x=xPoss, y=yPoss)

    tittleLabel = Label(mainCanvas, image=Fondo_pong, borderwidth=0)
    tittleLabel.place(x=xPoss + 5, y=yPoss - 50)

    playersButton1 = Button(mainCanvas, text='1 Player', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,
                            justify=RIGHT, borderwidth=0)
    playersButton1.place(x=xPoss + 290, y=yPoss + 250)

    playersButton2 = Button(mainCanvas, text='2 Player', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,
                            justify=RIGHT, borderwidth=0)
    playersButton2.place(x=xPoss + 290, y=yPoss + 310)

    playersOption = Button(mainCanvas, text='Options', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,
                           justify=RIGHT, borderwidth=0, command=ajustes)
    playersOption.place(x=xPoss + 290, y=yPoss + 370)

    playersHighScore = Button(mainCanvas, text='Scores', font=fonts + str(30), fg=fgColor, bg=bgColor, width=xWidth,
                              justify=RIGHT, borderwidth=0)
    playersHighScore.place(x=xPoss + 290, y=yPoss + 430)


load_interface(0, 0, 10, 'white', 'black', 'Fixedsys ')

main.mainloop()

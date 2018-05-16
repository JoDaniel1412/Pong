from tkinter import *
from settings import *
from pong import *

main = Tk()
main.minsize(320, 870)
main.resizable(NO, NO)
main.title('Matrix')
main.config(bg='black')
canvas = Canvas(main, bg='black', width=W2, height=H2)
canvas.place(x=5, y=5)


def draw_matrix():
    for ball in balls:
        size = ball.get_ball_center()
    for n in range(len(M)):
        if n == size[0]:
            square = Label(canvas, text='1', fg='white', bg='green')
            square.grid(row=M[n][0], column=M[n][1])
        else:
            square = Label(canvas, text='0', fg='white', bg='black')
            square.grid(row=M[n][0], column=M[n][1])


draw_matrix()

main.mainloop()
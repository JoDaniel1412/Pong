import random
import time
from threading import Thread
from tkinter import *
import pygame as py

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Variables
W, H = 1400, 800
W1, H1 = 800, 600
W2, H2 = W//2, H//2
HW, HH = W / 2, H / 2
FPS = 60
secs = 3
loop = True
run_game = True
tabla = []
end_game = False
tiempo_funcion = time.time()

# Default Game Variables
pallets_selected = 1
difficulty_selected = 1
style_selected = 0
players_selected = 1
py.mixer.init()

# Sprite Groups
sprites = py.sprite.Group()
players = py.sprite.Group()
balls = py.sprite.Group()
walls = py.sprite.Group()


# Clase usada para iniciar el juego con determinados ajustes
# Instancias: cantidad de jugadores(1 o 2), cantidad de paletas(1 o 2), difficultad(0, 1 o 2), stylo del arte(0, 1, 2)
# Metodos: crear y obtener la mtatriz, iniciar el juego, cargar imagenes, sonidos, dibujar puntaje y frecuencia de muros
class Game:
    def __init__(self, player, pallets, difficulty, style):
        self.players = player
        self.pallets = pallets
        self.difficulty = difficulty
        self.style = style
        self.images = self.load_images()
        self.sound_effects = self.load_sounds()
        self.matrix = []
        self.make_matrix()
        self.score1 = 0
        self.score2 = 0

    # Metodo para generar matriz
    def make_matrix(self):
        n, m = 25, 40
        i, j = 0, 0
        x, y = W // m, H // n
        while W >= i:
            while H >= j:
                self.matrix.append([i, j])
                j += y
            i += x
            j = 0

    # Metodo para obtener la matriz
    def get_matrix(self):
        return self.matrix

    # Metodo para iniciar el juego
    def start_game(self):
        player1_keys = ('py.K_w', 'py.K_s')
        player2_keys = ('py.K_UP', 'py.K_DOWN')
        images = self.images[0]
        poss1 = 38
        poss2 = 1026
        poss3 = poss1 + 7
        poss4 = poss2 + 5
        if self.players == 1:  # En caso de ser un jugador
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane2 = Player(player1_keys, self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                cpu2 = Player('', self.difficulty, poss4, self.matrix, [True, 'CPU'], images[3], self.pallets)
                sprites.add(humane2)
                sprites.add(cpu2)
                players.add(humane2)
                players.add(cpu2)
            humane = Player(player1_keys, self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            cpu = Player('', self.difficulty, poss2, self.matrix, [True, 'CPU'], images[2], self.pallets)
            sprites.add(humane)
            sprites.add(cpu)
            players.add(humane)
            players.add(cpu)

        if self.players == 2:  # En caso de ser dos jugadores
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane1 = Player(player1_keys, self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                humane2 = Player(player2_keys, self.difficulty, poss4, self.matrix, [True, 'HUMANE'], images[3], self.pallets)
                sprites.add(humane1)
                sprites.add(humane2)
                players.add(humane1)
                players.add(humane2)
            humane1 = Player(player1_keys, self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            humane2 = Player(player2_keys, self.difficulty, poss2, self.matrix, [True, 'HUMANE'], images[2], self.pallets)
            sprites.add(humane1)
            sprites.add(humane2)
            players.add(humane1)
            players.add(humane2)
        ball = Ball(self.difficulty, self.images[1], self)
        sprites.add(ball)
        balls.add(ball)

    def load_images(self):  # Metodo para cargar imagenes del juego
        pallet_images = None
        ball = None
        bg = None
        wall_image = None
        if self.style == 0:  # Estilo Clasico
            white_pallet = py.image.load('img/default_pallet.png').convert_alpha()
            ball = py.Surface((10, 10))
            ball.fill(white)
            bg = py.image.load('img/default_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [white_pallet, white_pallet, white_pallet, white_pallet]
            wall_image = white_pallet
        if self.style == 1:  # Estilo Neon
            wall_image = py.image.load('img/neon_wall.png').convert_alpha()
            player_red = py.image.load('img/neon_red.png').convert_alpha()
            player_green = py.image.load('img/neon_green.png').convert_alpha()
            player_pink = py.image.load('img/neon_pink.png').convert_alpha()
            player_blue = py.image.load('img/neon_blue.png').convert_alpha()
            ball = py.image.load('img/neon_ball.png').convert_alpha()
            bg = py.image.load('img/neon_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [player_red, player_green, player_pink, player_blue]
        if self.style == 2:  # Estilo Baseball
            wall_image = py.image.load('img/baseball_wall.png').convert_alpha()
            player_bat = py.image.load('img/baseball_bat.png').convert_alpha()
            ball = py.image.load('img/baseball_ball.png').convert_alpha()
            pallet_images = [player_bat, player_bat, player_bat, player_bat]
            bg = py.image.load('img/baseball_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
        return pallet_images, ball, bg, wall_image

    # Metodo para cargar la musica del juego
    def load_sounds(self):
        bounce = None
        score = None
        music = None
        if self.style == 0:
            bounce = py.mixer.Sound('sound/default_bounce.wav')
            score = py.mixer.Sound('sound/default_score.wav')
            music = py.mixer.Sound('sound/default_music.ogg')
        if self.style == 1:
            bounce = py.mixer.Sound('sound/neon_bounce.wav')
            score = py.mixer.Sound('sound/neon_score.wav')
            music = py.mixer.Sound('sound/neon_music.ogg')
        if self.style == 2:
            bounce = py.mixer.Sound('sound/baseball_bounce.wav')
            score = py.mixer.Sound('sound/baseball_score.wav')
            music = py.mixer.Sound('sound/baseball_music.ogg')
        return bounce, score, music

    # Metodo para obtener los sonidos del juego
    def get_sound_effects(self):
        return self.sound_effects

    # Metodo que ajusta el puntaje del jugador 1
    def add_score1(self):
        self.score1 += 1
        for pallets in players:
            pallets.reset_speed()

    # Metodo que ajusta el puntaje del jugador 2
    def add_score2(self):
        self.score2 += 1
        for pallets in players:
            pallets.reset_speed()

    # Metodo para obtener los puntajes
    def get_scores(self):
        return self.score1, self.score2

    # Metodo para ajustar la frecuencia de muros
    def get_wall_spawn_rate(self):
        spawn_rate = 0
        if self.difficulty == 0:
            spawn_rate = 0.7
        elif self.difficulty == 1:
            spawn_rate = 0.5
        elif self.difficulty == 2:
            spawn_rate = 0.25
        return spawn_rate


# Funcion para dibujar textos
def draw_text(surf, text, poss, font):
    font_type = py.font.match_font(font[0])
    make_font = py.font.Font(font_type, font[1])
    text_surface = make_font.render(text, True, font[2])
    rect = text_surface.get_rect()
    rect.center = poss
    surf.blit(text_surface, rect)


# Clase que crea las paletas de los jugadores
# Instancias: teclas, difficultad, posicion, la matrix, el estado(vivo, humano/computador), imagen y cantidad de paletas
# Metodos: obtener 3 segmentos, ajustar las dimensiones y velocidad, atualizarla en la pantalla
class Player(py.sprite.Sprite):
    def __init__(self, keys, difficulty, poss, matrix, status, image, pallets):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = poss
        self.pallets = pallets
        size = self.set_pallets_size()
        self.pallet_size = matrix[12][1] - matrix[12-size][1]
        self.status = status
        self.keys = keys
        self.matrix = matrix
        self.speed = self.set_speed()
        self.default_speed = self.speed
        self.image = py.transform.scale(image, (25, self.pallet_size))
        self.rect = self.image.get_rect()
        self.rect.center = self.matrix[self.poss]
        self.speed_limit = 40

    # Metodo que retorna una lista con los segmentos de la paleta
    def pallet_segments(self):
        segment = self.pallet_size / 3
        return [self.rect.top] + [self.rect.top+segment] + [self.rect.bottom-segment] + [self.rect.bottom]

    # Metodo que ajusta el largo de la paleta segun dificultad
    def set_pallets_size(self):
        large = 0
        if self.difficulty == 0:
            large = 9
        if self.difficulty == 1:
            large = 6
        if self.difficulty == 2:
            large = 3
        return large

    # Metodo que obtiene las dimensiones de la paleta
    def get_pallet_size(self):
        return self.rect.center, self.pallet_size

    # Metodo que ajusta la velocidad de la paleta segun dificultad
    def set_speed(self):
        speed = 0
        if self.difficulty == 0:
            speed = 7
        if self.difficulty == 1:
            speed = 10
        if self.difficulty == 2:
            speed = 15
        return speed

    # Metodo para aumentar la velocidad progresivamente
    def increase_xSpeed(self):
        if self.speed_limit > self.speed > 0:
            self.speed += 1
        if -self.speed_limit < self.speed < 0:
            self.speed -= 1

    # Metodo par reiniciar la velocidad
    def reset_speed(self):
        self.speed = self.default_speed

    # Metodo para obtener el estado de la paleta
    def set_status(self, boolean):
        self.status[0] = boolean

    # Metodo que actualiza la posicion de la paleta en la pantalla
    def update(self):
        global tiempo_funcion
        k = py.key.get_pressed()

        # En caso de ser 2 paletas
        if self.pallets == 2:
            if self.status[0] and self.status[1] == 'HUMANE':  # Ajusta movimiento del jugador
                if k[eval(self.keys[0])]:
                    self.rect.y -= self.speed
                if k[eval(self.keys[1])]:
                    self.rect.y += self.speed
            if self.status[0] and self.status[1] == 'CPU':  # Ajusta movimiento del cpu y dificultad
                tiempo3 = time.time()
                diferencia = int(tiempo3 - tiempo_funcion)
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        n = 0
                        posicion3 = 0
                        for i in players:
                            if n == 1:
                                posicion3 = i.get_pallet_size()[0][1]
                                i.rect.y = y
                            if n == 3:
                                i.rect.y = posicion3 + 200
                            n += 1
                    if self.difficulty == 1:
                        if diferencia % 2 == 0:
                            n = 0
                            posicion3 = 0
                            for i in players:
                                if n == 1:
                                    posicion3 = i.get_pallet_size()[0][1]
                                    i.rect.y = y
                                if n == 3:
                                    i.rect.y = posicion3 + 200
                                n += 1
                    if self.difficulty == 0:
                        if diferencia % 3 == 0:
                            n = 0
                            posicion3 = 0
                            for i in players:
                                if n == 1:
                                    posicion3 = i.get_pallet_size()[0][1]
                                    i.rect.y = y
                                if n == 3:
                                    i.rect.y = posicion3 + 200
                                n += 1
            if self.rect.bottom < 0:
                self.rect.top = H
            if self.rect.top > H:
                self.rect.bottom = 0

        # En caso de ser una paleta
        else:
            if self.status[0] and self.status[1] == 'HUMANE':  # Ajusta movimiento del jugador
                if k[eval(self.keys[0])] and self.rect.top > 0:
                    self.rect.y -= self.speed
                if k[eval(self.keys[1])] and self.rect.bottom < H:
                    self.rect.y += self.speed
            if self.status[0] and self.status[1] == 'CPU':  # Ajusta movimiento del cpu y dificultad
                tiempo3 = time.time()
                diferencia = int(tiempo3 - tiempo_funcion)
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        self.rect.y = y
                    if self.difficulty == 1:
                        if diferencia % 2 == 0:
                            self.rect.y = y
                    if self.difficulty == 0:
                        if diferencia % 3 == 0:
                            self.rect.y = y


# Clase que crea la pelota
# Instancias: la difficultad, imagenes
# Metodos: animacion de rotar, obtener y ajustar posicion, velocidad, dimensiones y actualizarla en la pantalla
class Ball(py.sprite.Sprite):
    def __init__(self, difficulty, image, game):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = (HW, HH)
        self.game = game
        self.size = self.set_size()
        self.original_image = py.transform.scale(image, (self.size, self.size))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.rect.center = self.poss
        self.speed = self.set_speed()
        self.xSpeed = random.choice(self.speed)
        self.ySpeed = random.choice(self.speed)
        self.sound_effects = game.get_sound_effects()
        self.speed_limit = 55
        self.rotation_speed = 7
        self.last_rotation = 0

    # Metodo para rotar la imagen de la bola
    def rotate(self):
        self.last_rotation += self.rotation_speed
        self.image = py.transform.rotate(self.original_image, self.last_rotation)

    # Metodo para obtener la posicion de la bola
    def get_ball_poss(self):
        return self.rect.center

    # Metodo que obtiene la posicion en Y de la bola
    def get_ball_yPoss(self):
        return self.rect.y

    # Metodo que obtiene el centro de la bola
    def get_ball_center(self):
        return self.rect.center

    # Metodo que hace a la pelota cambiar de direccion en caso de colisionar con la paleta
    def set_ySpeed(self, collision):
        if collision == 'top':
            self.ySpeed = self.speed[0]
        if collision == 'center':
            self.ySpeed = 0
        if collision == 'bottom':
            self.ySpeed = self.speed[1]

    # Metodo para invertir la direccion de la bola al rebotar
    def set_xSpeed(self):
        if self.xSpeed < 0:
            self.xSpeed = abs(self.xSpeed)
        else:
            self.xSpeed = -self.xSpeed

    # Metodo para cambiar la velocidad de la bola
    def top_xSpeed(self):
        if self.xSpeed < 0:
            self.xSpeed = -50
        else:
            self.xSpeed = 50

    # Metodo para aumentar la velocidad progresivamente
    def increase_xSpeed(self):
        if self.speed_limit > self.xSpeed > 0:
            self.xSpeed += 2
        if -self.speed_limit < self.xSpeed < 0:
            self.xSpeed -= 2

    # Metodo que ajusta la velocidad de la pelota segun dificultads
    def set_speed(self):
        speed_range = [0, 0]
        if self.difficulty == 0:
            speed_range = [-6, 6]
        if self.difficulty == 1:
            speed_range = [-8, 8]
        if self.difficulty == 2:
            speed_range = [-10, 10]
        return speed_range

    # Metodo que ajusta el radio de la bola segun dificultad
    def set_size(self):
        ball_size = 0
        if self.difficulty == 0:
            ball_size = 55
        if self.difficulty == 1:
            ball_size = 40
        if self.difficulty == 2:
            ball_size = 25
        return ball_size

    # Metodo que crea una bola cada vez que se anota un punto
    def new_ball(self):
        newBall = Ball(self.difficulty, self.original_image, self.game)
        sprites.add(newBall)
        balls.add(newBall)

    # Metodo que actualiza la posicion de la pelota en la pantalla
    def update(self):
        self.rotate()
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if self.rect.top <= 0:
            self.ySpeed = -self.ySpeed
            self.rect.top = 1
            self.sound_effects[0].play()
        if self.rect.bottom >= H:
            self.ySpeed = -self.ySpeed
            self.rect.bottom = H-1
            self.sound_effects[0].play()
        if self.rect.left < 0:
            self.sound_effects[1].play()
            self.game.add_score2()
            time.sleep(1)
            self.kill()
            self.new_ball()
        if self.rect.right > W:
            self.sound_effects[1].play()
            self.game.add_score1()
            time.sleep(1)
            self.kill()
            self.new_ball()


# Clase que crea la muros
# Instancias: la matriz, imagenes
# Metodos: obtener la posicion del muro
class Wall(py.sprite.Sprite):
    def __init__(self, matrix, image):
        py.sprite.Sprite.__init__(self)
        self.matrix = matrix
        self.width = random.randrange(20, 100, W//40)
        self.height = random.randrange(20, 100, H//25)
        self.image = py.transform.scale(image, (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.center = random.choice(self.matrix[400:800])

    def get_center(self):
        return self.rect.center


# Inicia ventana de matriz
def matrix_loop(M):
    main2 = Tk()
    main2.minsize(320, 870)
    main2.resizable(NO, NO)
    main2.title('Matrix')
    main2.config(bg='black')
    canvas = Canvas(main2, bg='black', width=W2, height=H2)
    canvas.place(x=5, y=5)

    # Funcion que dibuja una matrix en grids
    def draw_matrix():
        size = []
        while True:
            for ball in balls:
                size.append(ball.get_ball_center())
            for each in players:
                size.append(each.get_pallet_size())
            for n in range(len(M)):
                if n == size[0][1]:
                    square = Label(canvas, text='1', fg='white', bg='red')
                    square.grid(row=M[n][0], column=M[n][1])
                elif n == size[1][0] or n == size[2][0]:
                    square = Label(canvas, text='2', fg='white', bg='green')
                    square.grid(row=M[n][0], column=M[n][1])
                else:
                    square = Label(canvas, text='0', fg='white', bg='black')
                    square.grid(row=M[n][0], column=M[n][1])

    matrix = Thread(target=draw_matrix)
    matrix.start()

    main2.mainloop()


# Inicia el menu del juego
def menu_loop():
    main = Tk()
    main.minsize(W1, H1)
    main.resizable(NO, NO)
    main.title('Pong')
    Fondo_pong = PhotoImage(file="img/Imagen de menu de pong.gif")

    # Inicia el juego en modo un jugador vs cpu
    def player1():
        global players_selected
        global run_game
        players_selected = 1
        run_game = True
        main.destroy()

    # Inicia el juego en modo dos jugadores
    def player2():
        global players_selected
        global run_game
        players_selected = 2
        run_game = True
        main.destroy()

    # Funcion que inicia la interfaz del menu
    def load_interface(xPoss, yPoss, xWidth, fgColor, bgColor, fonts):
        # Funcion que abre la ventana de ajustes
        def ajustes():
            def cerrar_ajustes():  # Funcion que cierra la ventana ajustes
                ventana2.destroy()
                main.deiconify()

            # Configura la dificultas a facil
            def easy():
                global difficulty_selected
                difficulty_selected = 0
                facil['bg'], facil['fg'] = fgColor, bgColor
                medio['bg'], medio['fg'] = bgColor, fgColor
                dificil['bg'], dificil['fg'] = bgColor, fgColor

            # Configura la dificultas a medio
            def medium():
                global difficulty_selected
                difficulty_selected = 1
                facil['bg'], facil['fg'] = bgColor, fgColor
                medio['bg'], medio['fg'] = fgColor, bgColor
                dificil['bg'], dificil['fg'] = bgColor, fgColor

            # Configura la dificultas a dificil
            def hard():
                global difficulty_selected
                difficulty_selected = 2
                facil['bg'], facil['fg'] = bgColor, fgColor
                medio['bg'], medio['fg'] = bgColor, fgColor
                dificil['bg'], dificil['fg'] = fgColor, bgColor

            # Configura el estilo a clasico
            def default_set():
                global style_selected
                style_selected = 0
                clasico['bg'], clasico['fg'] = fgColor, bgColor
                neon['bg'], neon['fg'] = bgColor, fgColor
                futbol['bg'], futbol['fg'] = bgColor, fgColor

            # Configura el estilo a neon
            def neon_set():
                global style_selected
                style_selected = 1
                clasico['bg'], clasico['fg'] = bgColor, fgColor
                neon['bg'], neon['fg'] = fgColor, bgColor
                futbol['bg'], futbol['fg'] = bgColor, fgColor

            # Configura el estilo a baseball
            def baseball_set():
                global style_selected
                style_selected = 2
                clasico['bg'], clasico['fg'] = bgColor, fgColor
                neon['bg'], neon['fg'] = bgColor, fgColor
                futbol['bg'], futbol['fg'] = fgColor, bgColor

            # Configura el modo a una paleta
            def pallets_select1():
                global pallets_selected
                pallets_selected = 1
                una_paleta['bg'], una_paleta['fg'] = fgColor, bgColor
                dos_paletas['bg'], dos_paletas['fg'] = bgColor, fgColor

            # Configura el modo a dos paletas
            def pallets_select2():
                global pallets_selected
                pallets_selected = 2
                una_paleta['bg'], una_paleta['fg'] = bgColor, fgColor
                dos_paletas['bg'], dos_paletas['fg'] = fgColor, bgColor

            main.withdraw()

            ventana2 = Toplevel()
            ventana2.title("Ajustes")

            ventana2.minsize(W1, H1)
            ventana2.resizable(width=NO, height=NO)

            canvas2 = Canvas(ventana2, width=W1, height=H1, bg="black")
            canvas2.place(x=-1, y=0)

            settings = Label(canvas2, text="Ajustes", font=fonts + str(40), fg=fgColor, bg=bgColor)
            settings.place(x=290, y=10)

            dificultad = Label(canvas2, text="Seleccione dificultad:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            dificultad.place(x=230, y=420)

            facil = Button(canvas2, text="Facil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=easy)
            facil.place(x=180, y=470)

            medio = Button(canvas2, text="Medio", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=medium)
            medio.place(x=330, y=470)

            dificil = Button(canvas2, text="Dificil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=hard)
            dificil.place(x=480, y=470)

            paletas = Label(canvas2, text="Seleccione paletas:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            paletas.place(x=460, y=120)

            una_paleta = Button(canvas2, text="Una paleta", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=pallets_select1)
            una_paleta.place(x=500, y=180)

            dos_paletas = Button(canvas2, text="Dos paletas", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=pallets_select2)
            dos_paletas.place(x=500, y=240)

            escenario = Label(canvas2, text="Escoja escenario:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            escenario.place(x=40, y=120)

            clasico = Button(canvas2, text="Clasico", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=default_set)
            clasico.place(x=50, y=160)

            neon = Button(canvas2, text="Neon", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=neon_set)
            neon.place(x=50, y=210)

            futbol = Button(canvas2, text="Baseball", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=baseball_set)
            futbol.place(x=50, y=260)

            aceptar_ajustes = Button(canvas2, text="LISTO!", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_ajustes)
            aceptar_ajustes.place(x=670, y=10)

            volver = Button(canvas2, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_ajustes)
            volver.place(x=10, y=10)

        # Funcion que abre la ventana de puntuaciones
        def mostrar_puntuaciones():
            def cerrar_mostrar_puntuciones():  # Funcion que cierra la ventana puntuaciones
                global tabla
                main.deiconify()
                ventana__mostrar_scores.destroy()
                tabla = []

            main.withdraw()

            ventana__mostrar_scores = Toplevel()
            ventana__mostrar_scores.title("Puntuaciones")

            ventana__mostrar_scores.minsize(W2, H2)
            ventana__mostrar_scores.resizable(width=NO, height=NO)

            canvas_mostrar_scores = Canvas(ventana__mostrar_scores, width=W2, height=H2, bg="black")
            canvas_mostrar_scores.place(x=-1, y=0)

            label_mejores = Label(canvas_mostrar_scores, text="Mejores Puntuaciones:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            label_mejores.place(x=200, y=40)

            canvas_tabla = Canvas(canvas_mostrar_scores, width=W2 // 2, height=H2 // 2)
            canvas_tabla.place(x=200, y=100)

            cerrar_scores = Button(canvas_mostrar_scores, text="BACK!", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_mostrar_puntuciones)
            cerrar_scores.place(x=5, y=0)

            # Funcion que lee el txt
            def separarPuntuaciones(i):
                if i == len(listaScores):
                    return
                listaScores[i] = listaScores[i].replace("\n", "").split(";")
                separarPuntuaciones(i + 1)
            file = open("Scores.txt", 'r')
            listaScores = file.readlines()
            separarPuntuaciones(0)
            file.close()

            # Funcion que crea la tabla
            def crearTabla(x, y, columns):
                global tabla
                if x == len(listaScores):
                    return ''
                elif y == 2:
                    tabla += [columns]
                    return crearTabla(x + 1, 0, [])
                else:
                    if y == 0:
                        seccion = Entry(canvas_tabla, text='', width=15, justify=CENTER, bg=bgColor, fg=fgColor)
                        seccion.grid(row=x, column=y)
                        return crearTabla(x, y + 1, columns + [seccion])
                    seccion = Entry(canvas_tabla, text='', width=30, bg=bgColor, fg=fgColor)
                    seccion.grid(row=x, column=y)
                    return crearTabla(x, y + 1, columns + [seccion])

            # Funcion que llena la tabla anteriormente creada
            def llenarTabla(x, y):  # funcion que llena la tabla para vendedores con el vendedores.txt
                global tabla
                if x == len(listaScores):
                    return
                elif y != 2:
                    tabla[x][y].insert(0, listaScores[x][y])
                    return llenarTabla(x, y + 1)
                else:
                    return llenarTabla(x + 1, 0)

            crearTabla(0, 0, [])
            llenarTabla(0, 0)

        mainCanvas = Canvas(main, width=W1, height=H1, bg=bgColor)
        mainCanvas.place(x=xPoss, y=yPoss)

        tittleLabel = Label(mainCanvas, image=Fondo_pong, borderwidth=0)
        tittleLabel.place(x=xPoss+5, y=yPoss-50)

        playersButton1 = Button(mainCanvas, text='1 Player', font=fonts+str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=player1)
        playersButton1.place(x=xPoss + 290, y=yPoss + 250)

        playersButton2 = Button(mainCanvas, text='2 Player', font=fonts+str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=player2)
        playersButton2.place(x=xPoss + 290, y=yPoss + 310)

        playersOption = Button(mainCanvas, text='Options', font=fonts+str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=ajustes)
        playersOption.place(x=xPoss + 290, y=yPoss + 370)

        playersHightscore = Button(mainCanvas, text='Scores', font=fonts+str(30), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=mostrar_puntuaciones)
        playersHightscore.place(x=xPoss + 290, y=yPoss + 430)

    # Funcion abre la ventana de puntuaciones
    def puntuaciones(fgColor, bgColor, fonts):
        def cerrar_puntuaciones():  # Funcion para cerrar ventana puntuacione
            global secs
            agregar_puntuaciones = open('Scores.txt', 'a')
            agregar_puntuaciones.write(escribir_jugadores.get())
            agregar_puntuaciones.write(';')
            agregar_puntuaciones.write("su tiempo es " + str(int(secs)) + " segundos")
            agregar_puntuaciones.write('\n')
            agregar_puntuaciones.close()
            main.deiconify()
            ventana_scores.destroy()

        main.withdraw()

        ventana_scores = Toplevel()
        ventana_scores.title("Ingreso de Jugador")

        ventana_scores.minsize(W2, H2)
        ventana_scores.resizable(width=NO, height=NO)

        canvas_scores = Canvas(ventana_scores, width=W2, height=H2, bg="black")
        canvas_scores.place(x=-1, y=0)

        label_scores = Label(canvas_scores, text="Digite nombre de jugador:", font=fonts + str(20), fg=fgColor, bg=bgColor)
        label_scores.place(x=150, y=120)

        escribir_jugadores = Entry(canvas_scores, width=30)
        escribir_jugadores.place(x=250, y=200)

        insertar_puntuacion = Button(canvas_scores, text="Aceptar", font=fonts, width=20, command=cerrar_puntuaciones)
        insertar_puntuacion.place(x=260, y=260)

    # Funcion para detener la ejecucion del programa
    def Quit():
        global loop
        global run_game
        loop = False
        run_game = False
        main.destroy()

    load_interface(0, 0, 10, 'white', 'black', 'Fixedsys ')

    if end_game:  # Inicia la ventana para ingresar datos de puntaje
        puntuaciones('white', 'black', 'Fixedsys ')

    main.protocol('WM_DELETE_WINDOW', Quit)
    main.mainloop()


# Inicia el juego
def game_loop():
    global secs
    global loop
    global run_game
    time1 = time.time()
    py.init()
    display = py.display.set_mode((W, H))
    py.display.set_caption('Pong')
    clock = py.time.Clock()

    # Inicia la Clase Game
    game = Game(players_selected, pallets_selected, difficulty_selected, style_selected)
    game.start_game()

    # Cargar fondo, sonidos y otros
    back_grounds = game.load_images()[2]
    sound_effects = game.get_sound_effects()
    sound_effects[2].play(loops=-1)
    M = game.get_matrix()
    walls_images = game.load_images()[3]
    walls_spawn = game.get_wall_spawn_rate()

    # Funcion que define cuando se acaba el juego
    def win_game():
        global secs
        global end_game
        global run_game
        time2 = time.time()
        secs = time2 - time1
        run_game = False
        end_game = True

    # Funcion que inicia el menu de pausa
    def show_pause():
        global run_game
        global loop
        pause = True
        while pause:
            clock.tick(FPS)
            for events in py.event.get():
                if events.type == py.QUIT:
                    pause = False
                    run_game = False
                    loop = False
                if events.type == py.KEYUP:
                    pause = False

            # Dibujar textos durante la pausa
            draw_text(display, "PAUSA", (HW, H*3/8), ("Arial", 64, white))
            draw_text(display, "Presione cualquiere tecla para continuar", (HW, H*5/8), ("Arial", 22, white))

            py.display.update()

    # Game loop
    while run_game:
        global secs
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run_game = False
                loop = False
            if event.type == py.KEYDOWN and event.key == py.K_ESCAPE:
                run_game = False
                secs = 3
            if event.type == py.KEYUP and event.key == py.K_p:
                show_pause()
            if event.type == py.KEYUP and event.key == py.K_m:
                tkinter_matrix = Thread(target=matrix_loop)
                matrix_loop(M)

        # Cronometro
        time_lapsed = py.time.get_ticks()//1000
        if secs == time_lapsed:
            secs += 1

        # Colisiones paleta con bola
        hits = py.sprite.groupcollide(players, balls, False, False)
        if hits:
            sound_effects[0].play()
            if random.random() > walls_spawn:
                wall = Wall(M, walls_images)
                sprites.add(wall)
                walls.add(wall)
            for element in balls:
                element.set_xSpeed()
                for pallet in hits:
                    ball_poss = element.get_ball_poss()[1]
                    pallet_segment = pallet.pallet_segments()
                    if pallet_segment[0] <= ball_poss < pallet_segment[1]:  # Revisa si la bola choca en la parte superior
                        element.set_ySpeed('top')
                    if pallet_segment[1] <= ball_poss <= pallet_segment[2]:  # Revisa si la bola choca en la parte central
                        element.set_ySpeed('center')
                    if pallet_segment[2] < ball_poss <= pallet_segment[3]:  # Revisa si la bola choca en la parte inferior
                        element.set_ySpeed('bottom')
                    element.increase_xSpeed()
                    pallet.increase_xSpeed()

        # Colisiones bola con muros
        if py.sprite.groupcollide(balls, walls, False, True):
            sound_effects[0].play()
            for element in balls:
                element.set_xSpeed()

        # Update
        sprites.update()
        game_scores = game.get_scores()
        if game_scores[0] == 5 or game_scores[1] == 5:
            win_game()

        # Draw
        display.blit(back_grounds, (0, 0))
        sprites.draw(display)
        draw_text(display, str(game.get_scores()[0]), M[366], ('arial', 80, white))
        draw_text(display, str(game.get_scores()[1]), M[652], ('arial', 80, white))

        py.display.update()

    for sprite in sprites:
        sprite.kill()
    py.quit()


# Controla los ciclos entre menu y juego
while loop:
    menu_loop()
    if run_game:
        game_loop()
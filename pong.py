import pygame as py
import random
import time
import socket
import serial
from threading import Thread
from tkinter import *
from settings import *


# Loop Variables
pause = False
loop = True
run_game = True
scores_game = False
matrix_running = False
run_lan = False
restard = False
tabla = []
tiempo_funcion = time.time()
py.mixer.init()

# Sprite Groups
sprites = py.sprite.Group()
players = py.sprite.LayeredUpdates()
balls = py.sprite.LayeredUpdates()
walls = py.sprite.Group()

# Lan Variables
Server = None
Cliente = None
lanBall = (HW, HH)
lanPallet = 800

# Arduino Variables
run_arduino = False
cont = 1  # Contador que evita enviar multiples mensajes repetidos al arduino
# noinspection PyBroadException
try:  # Trata de iniciar la conexion de Arduino
    ser = serial.Serial('COM9', 9600, timeout=0)
    print('Arduino Running')
    run_arduino = True
    ser.write(b'0')
except:
    pass

# Time Variables
lastTimePaused = time.time()
lastTimeMuted = time.time()
lastTimeStyle = time.time()


# Clase usada para iniciar el juego con determinados ajustes
# Instancias: cantidad de jugadores(1 o 2), cantidad de paletas(1 o 2), difficultad(0, 1 o 2), stylo del arte(0, 1, 2)
# Metodos: crear y obtener la mtatriz, iniciar el juego, cargwar imagenes, sonidos, dibujar puntaje y frecuencia de muros
class Game:
    def __init__(self, player, pallets, difficulty, style, wall):
        self.players = player
        self.pallets = pallets
        self.difficulty = difficulty
        self.style = style
        self.wall = wall
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
        images = self.images[0]
        poss1 = 38
        poss2 = 1026
        poss3 = poss1 + 7
        poss4 = poss2 + 5
        if self.players == 0:  # En caso de ser modo practica
            if self.pallets == 2:
                poss1 -= 4
                humane2 = Player(player1_keys, self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                sprites.add(humane2)
                players.add(humane2)
            humane = Player(player1_keys, self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            sprites.add(humane)
            players.add(humane)
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

        if self.players == 3:  # En caso de ser Local LAN
            if Cliente is not None:
                humane = Player(player1_keys, self.difficulty, poss2, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
                online = Player('', self.difficulty, poss1, self.matrix, [True, 'ONLINE'], images[2], self.pallets)
                sprites.add(online)
                sprites.add(humane)
                players.add(online)
                players.add(humane)
            if Cliente is None:
                humane = Player(player1_keys, self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
                online = Player('', self.difficulty, poss2, self.matrix, [True, 'ONLINE'], images[2], self.pallets)
                sprites.add(humane)
                sprites.add(online)
                players.add(humane)
                players.add(online)
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
            bg = py.image.load('img/neon_bg.jpg').convert()
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
            bounce = py.mixer.Sound('sound/default_bounce.ogg')
            score = py.mixer.Sound('sound/default_score.ogg')
            music = py.mixer.Sound('sound/default_music.ogg')
        if self.style == 1:
            bounce = py.mixer.Sound('sound/neon_bounce.ogg')
            score = py.mixer.Sound('sound/neon_score.ogg')
            music = py.mixer.Sound('sound/default_music.ogg')
        if self.style == 2:
            bounce = py.mixer.Sound('sound/baseball_bounce.ogg')
            score = py.mixer.Sound('sound/baseball_score.ogg')
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


# Clase usada para establecer un servidor y cliente
# Instancias: ip:str, port:int, message:list, host
# Metodos: ajustar el mensaje, obtener la direccion, obtener datos, ajustar servidor o cliente
class Lan:
    def __init__(self, ip, port):
        self.message = 'start'
        self.receive = ''
        self.local = socket.gethostname()
        self.host = (ip, port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((self.local, 0))
        self.ip = self.sock.getsockname()[0]
        self.port = self.sock.getsockname()[1]
        self.data = []
        print('Local: ' + str(self.ip) + ' :: ' + str(self.port))

    def get_address(self):
        return self.ip, self.port

    def set_message(self, message):  # Metodo para ajustar el mensaje que se va a enviar
        self.message = str(message)

    def get_data(self):  # Metodo para obtener los datos recividos
        return self.data

    def get_receive(self):
        return self.receive

    def server(self):  # Metodo para iniciar servidor
        global lanPallet
        global run_game
        print('Server running, address: ' + str(self.ip) + '::' + str(self.port))
        while True:
            receive_b, address = self.sock.recvfrom(1024)
            self.receive = receive_b.decode('utf-8')
            message_b = self.message.encode('utf-8')
            self.sock.sendto(message_b, address)
            if self.receive == 'quit' or self.message == 'quit':
                self.sock.sendto(b'quit', address)
                run_game = False
                self.sock.close()
                print('Server stop')
                break
            if self.receive != 'start':
                receive_list = self.receive.replace('(', '').replace(')', '').replace(',', '').split(' ')
                for n in receive_list:
                    self.data.append(int(n))
                lanPallet = self.data[0]
                self.data = []

    def client(self):  # Metodo para iniciar cliente
        global lanBall
        global lanPallet
        global run_game
        print('Client running, address: ' + str(self.ip) + '::' + str(self.port))
        while True:
            message_b = self.message.encode('utf-8')
            self.sock.sendto(message_b, self.host)
            receive_b, address = self.sock.recvfrom(1024)
            self.receive = receive_b.decode('utf-8')
            if self.receive == 'quit' or self.message == 'quit':
                self.sock.sendto(b'quit', self.host)
                run_game = False
                self.sock.close()
                print('Client stop')
                break
            if self.receive != 'start':
                receive_list = self.receive.replace('(', '').replace(')', '').replace(',', '').split(' ')
                for n in receive_list:
                    self.data.append(int(n))
                lanPallet = self.data[0]
                lanBall = self.data[1:3]
                self.data = []


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
        self.adjust_speed()

    # Metodo que retorna la posicion de la paleta
    def get_y(self):
        return self.rect.y

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
        if pallets_size > 0:
            large = pallets_size
        return large

    # Metodo que mueve la paleta
    def move_pallet_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed*5

    def move_pallet_down(self):
        if self.rect.bottom < H:
            self.rect.y += self.speed*5

    # Metodo que obtiene las dimensiones de la paleta
    def get_pallet_size(self):
        return self.rect.center, self.pallet_size, self.poss

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

    # Metodo que ajusta la velocidad de la paleta en modo practica
    def adjust_speed(self):
        if starting_game_speed > 0:
            self.speed = starting_game_speed * 3/4
            if self.speed > self.speed_limit:
                self.speed = self.speed_limit

    # Metodo para aumentar la velocidad progresivamente
    def increase_xSpeed(self):
        if self.speed_limit > self.speed > 0:
            self.speed += 1
        if -self.speed_limit < self.speed < 0:
            self.speed -= 1

    # Metodo para reiniciar la velocidad
    def reset_speed(self):
        if starting_game_speed == 0:
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
            if self.status[0] and self.status[1] == 'ONLINE':  # Ajusta movimiento del jugador en LAN
                self.rect.y = lanPallet
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
        self.speed_limit = 50
        self.adjust_speed()
        self.rotation_speed = 7
        self.last_rotation = 0

    # Metodo para rotar la imagen de la bola
    def rotate(self):
        self.last_rotation += self.rotation_speed
        self.image = py.transform.rotate(self.original_image, self.last_rotation)

    # Metodo para obtener la posicion de la bola
    def get_ball_poss(self):
        return self.rect.center

    def get_ball_center(self):
        return self.rect.center

    # Metodo que obtiene la posicion en Y de la bola
    def get_ball_yPoss(self):
        return self.rect.y

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

    # Metodo que ajusta la velocidad de la pelota en modo practica
    def adjust_speed(self):
        if starting_game_speed > 0:
            self.xSpeed = starting_game_speed
            if self.xSpeed > self.speed_limit:
                self.xSpeed = self.speed_limit

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
        self.rect.center = HW, HH
        self.set_speed()
        self.xSpeed = random.choice(self.speed)
        self.ySpeed = random.choice(self.speed)

    # Metodo que actualiza la posicion de la pelota en la pantalla
    def update(self):
        self.rotate()
        if Cliente is not None:  # En caso de modo LAN
            self.rect.center = lanBall
        if self.rect.left < 0:  # Punto a la izquierda
            self.sound_effects[1].play()
            self.game.add_score2()
            time.sleep(0.5)
            self.new_ball()
        if not self.game.players == 0 and self.rect.right > W:  # Punto a la derecha
            self.sound_effects[1].play()
            self.game.add_score1()
            time.sleep(0.5)
            self.new_ball()
        else:  # En caso de juego Local
            self.rect.x += self.xSpeed
            self.rect.y += self.ySpeed
            if self.rect.top <= 0:  # Colision superior
                self.ySpeed = -self.ySpeed
                self.rect.top = 1
                self.sound_effects[0].play()
            if self.rect.bottom >= H:  # Colision inferior
                self.ySpeed = -self.ySpeed
                self.rect.bottom = H-1
                self.sound_effects[0].play()
            if self.game.players == 0 and self.rect.right > W:  # Colision derecha en modo practica
                self.sound_effects[0].play()
                self.set_xSpeed()
                self.ySpeed = random.randrange(-angle_hit, angle_hit)
                self.rect.right = W-1


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
    main2.minsize(W2, H2)
    main2.resizable(NO, NO)
    main2.title('Matrix')
    main2.config(bg='black')
    update = True

    canvas = Canvas(main2, bg='black', width=W2, height=H2)
    canvas.place(x=5, y=5)

    # Funcion para detener la ejecucion de la ventana
    def Quit():
        global update
        global matrix_running
        update = False
        matrix_running = False
        main2.destroy()

    # Funcion que dibuja una matrix en grids
    def draw_matrix():
        size = []
        for ball in balls:
            size.append(ball.get_ball_poss())
        for each in players:
            size.append(each.get_pallet_size())
        for wall in walls:
            size.append(wall.get_center())
        for n in range(len(M)):
            if n == size[0][1]:
                square = Label(canvas, text='1', fg='white', bg='red')
                square.grid(row=M[n][0], column=M[n][1])
            elif n == size[1][2] or n == size[2][2]:
                square = Label(canvas, text='2', fg='white', bg='green')
                square.grid(row=M[n][0], column=M[n][1])
            else:
                square = Label(canvas, text='0', fg='white', bg='black')
                square.grid(row=M[n][0], column=M[n][1])

    button = Button(main2, text='update', command=draw_matrix)
    button.place(x=0, y=0)

    main2.protocol('WM_DELETE_WINDOW', Quit)
    main2.mainloop()


# Inicia el menu del juego
def menu_loop():
    main = Tk()
    main.minsize(W1, H1)
    main.resizable(NO, NO)
    main.title('Pong')
    Fondo_pong = PhotoImage(file="img/Imagen de menu de pong.gif")
    lan_icon = PhotoImage(file='img/lan_icon.png')

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

            # Configura el puntaje maximo a 5
            def puntaje5():
                global top_points
                top_points = 5
                top_points5['bg'], top_points5['fg'] = fgColor, bgColor
                top_points10['bg'], top_points10['fg'] = bgColor, fgColor

            # Configura el puntaje maximo a 10
            def puntaje10():
                global top_points
                top_points = 10
                top_points10['bg'], top_points10['fg'] = fgColor, bgColor
                top_points5['bg'], top_points5['fg'] = bgColor, fgColor

            # Configura si desea jugar con obstaculos
            def activate_walls():
                global walls_able
                if walls_able == 0:
                    walls_able = 1
                    activa_muros['text'] = 'Activos'
                    activa_muros['bg'], activa_muros['fg'] = fgColor, bgColor
                else:
                    walls_able = 0
                    activa_muros['text'] = 'Desactivados'
                    activa_muros['bg'], activa_muros['fg'] = bgColor, fgColor

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
            dificultad.place(x=20, y=360)

            facil = Button(canvas2, text="Facil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=easy)
            facil.place(x=50, y=400)

            medio = Button(canvas2, text="Medio", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=medium)
            medio.place(x=50, y=450)

            dificil = Button(canvas2, text="Dificil", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=hard)
            dificil.place(x=50, y=510)

            top_points = Label(canvas2, text="Seleccione Puntos:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            top_points.place(x=460, y=300)

            top_points5 = Button(canvas2, text="5 Puntos", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=puntaje5)
            top_points5.place(x=500, y=340)

            top_points10 = Button(canvas2, text="10 Puntos", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=puntaje10)
            top_points10.place(x=500, y=390)

            paletas = Label(canvas2, text="Seleccione paletas:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            paletas.place(x=460, y=120)

            una_paleta = Button(canvas2, text="Una paleta", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=pallets_select1)
            una_paleta.place(x=500, y=160)

            dos_paletas = Button(canvas2, text="Dos paletas", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=pallets_select2)
            dos_paletas.place(x=500, y=220)

            escenario = Label(canvas2, text="Seleccione escenario:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            escenario.place(x=20, y=120)

            clasico = Button(canvas2, text="Clasico", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=default_set)
            clasico.place(x=50, y=160)

            neon = Button(canvas2, text="Neon", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=neon_set)
            neon.place(x=50, y=210)

            futbol = Button(canvas2, text="Baseball", font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=baseball_set)
            futbol.place(x=50, y=260)

            muros = Label(canvas2, text="Seleccione Muros:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            muros.place(x=460, y=480)

            activa_muros = Button(canvas2, text='Desactivados', font=fonts + str(20), fg=fgColor, bg=bgColor, borderwidth=0, command=activate_walls)
            activa_muros.place(x=500, y=520)

            aceptar_ajustes = Button(canvas2, text="LISTO!", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_ajustes)
            aceptar_ajustes.place(x=670, y=10)

            volver = Button(canvas2, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_ajustes)
            volver.place(x=10, y=10)

        # Inicia el juego en modo practica
        def practice_mode():
            global players_selected
            global run_game

            def cerrar_practica():  # Funcion que cierra la ventana practica
                ventana3.destroy()
                main.deiconify()

            def star_game():  # Funcion que inicia el juego
                global run_game
                global players_selected
                global starting_game_speed
                global pallets_size
                velocida = velocidadEntry.get()
                largo = paletaEntry.get()
                # noinspection PyBroadException
                try:
                    starting_game_speed = int(velocida)
                    pallets_size = int(largo)
                    if pallets_size > 12:
                        pallets_size = 12
                    players_selected = 0
                    run_game = True
                    main.destroy()
                except:
                    error = Label(canvas, text="Debe ingresar numeros enteros", font=fonts + str(10), fg='red', bg=bgColor)
                    error.place(x=450, y=250)

            main.withdraw()

            ventana3 = Toplevel()
            ventana3.title("Practica")

            ventana3.minsize(W1, H1)
            ventana3.resizable(width=NO, height=NO)

            canvas = Canvas(ventana3, width=W1, height=H1, bg="black")
            canvas.place(x=-1, y=0)

            volver = Button(canvas, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_practica)
            volver.place(x=10, y=10)

            practica = Label(canvas, text="Practica", font=fonts + str(40), fg=fgColor, bg=bgColor)
            practica.place(x=290, y=10)

            velocidad = Label(canvas, text="Ingrese velocidad de juego:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            velocidad.place(x=20, y=120)

            velocidadEntry = Entry(canvas, width=3, font=fonts+str(20))
            velocidadEntry.place(x=500, y=120)

            paletaSize = Label(canvas, text="Ingrese largo de paleta:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            paletaSize.place(x=20, y=200)

            paletaEntry = Entry(canvas, width=3, font=fonts + str(20))
            paletaEntry.place(x=450, y=200)

            start = Button(canvas, text="Iniciar", font=fonts + str(20), fg=bgColor, bg=fgColor, borderwidth=0, command=star_game)
            start.place(x=W1/2-50, y=400)

        # Inicia el juego en modo lan
        def lan_mode():
            def cerrar_lan():  # Funcion que cierra la ventana lan
                ventanaLan.destroy()
                main.deiconify()

            def start_host():  # Funcion que inicia el sevidor
                global Server
                global players_selected
                global run_game
                global run_lan
                Server = Lan('', 0)
                players_selected = 3
                run_game = True
                run_lan = True
                main.destroy()

            def star_client():  # Funcion que inicia el cliente
                global Server
                global Cliente
                global players_selected
                global run_game
                global run_lan

                ip = ipEntry.get()
                ports = int(puertosEntry.get())
                Cliente = Lan(ip, ports)
                players_selected = 3
                run_game = True
                run_lan = True
                main.destroy()

            main.withdraw()

            ventanaLan = Toplevel()
            ventanaLan.title("Lan")

            ventanaLan.minsize(W1, H1)
            ventanaLan.resizable(width=NO, height=NO)

            canvas = Canvas(ventanaLan, width=W1, height=H1, bg="black")
            canvas.place(x=-1, y=0)

            volver = Button(canvas, text="VOLVER", font=fonts + str(20), fg="black", bg="White", borderwidth=0, command=cerrar_lan)
            volver.place(x=10, y=10)

            titulo = Label(canvas, text="LAN", font=fonts + str(40), fg=fgColor, bg=bgColor)
            titulo.place(x=350, y=10)

            ipLabel = Label(canvas, text="Ingrese ip de host:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            ipLabel.place(x=20, y=120)

            ipEntry = Entry(canvas, width=13, font=fonts+str(20))
            ipEntry.place(x=400, y=120)

            puertosLabel = Label(canvas, text="Ingrese puerto:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            puertosLabel.place(x=20, y=200)

            puertosEntry = Entry(canvas, width=5, font=fonts + str(20))
            puertosEntry.place(x=400, y=200)

            joinButton = Button(canvas, text="Unirse", font=fonts + str(20), fg=bgColor, bg=fgColor, borderwidth=0, command=star_client)
            joinButton.place(x=W1/2-200, y=350)

            hostButton = Button(canvas, text="Crear", font=fonts + str(20), fg=bgColor, bg=fgColor, borderwidth=0, command=start_host)
            hostButton.place(x=W1 / 2+100, y=350)

            infoText = '''Para crear una partida no ingrese nada,
            si desea unirse a un juego 
            ingrese la ip del host y puerto.'''

            infoLabel = Label(canvas, text=infoText, justify=LEFT, font=fonts + str(17), fg=fgColor, bg=bgColor)
            infoLabel.place(x=20, y=450)

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

            ventana__mostrar_scores.minsize(HW, HH)
            ventana__mostrar_scores.resizable(width=NO, height=NO)

            canvas_mostrar_scores = Canvas(ventana__mostrar_scores, width=HW, height=HH, bg="black")
            canvas_mostrar_scores.place(x=-1, y=0)

            label_mejores = Label(canvas_mostrar_scores, text="Mejores Puntuaciones:", font=fonts + str(20), fg=fgColor, bg=bgColor)
            label_mejores.place(x=180, y=80)

            names = Label(canvas_mostrar_scores, text="Jugador", font=fonts + str(10), fg=fgColor, bg=bgColor)
            names.place(x=280, y=150)

            record = Label(canvas_mostrar_scores, text="Tiempo", font=fonts + str(10), fg=fgColor, bg=bgColor)
            record.place(x=370, y=150)

            canvas_tabla = Canvas(canvas_mostrar_scores, width=HW // 2, height=H2 // 2)
            canvas_tabla.place(x=270, y=190)

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
                    seccion = Entry(canvas_tabla, text='', width=10, justify=CENTER, bg=bgColor, fg=fgColor)
                    seccion.grid(row=x, column=y)
                    return crearTabla(x, y + 1, columns + [seccion])

            # Funcion que llena la tabla anteriormente creada
            def llenarTabla(x, y):
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

        practiceButton = Button(mainCanvas, text='Practicar', font=fonts+str(20), fg=fgColor, bg=bgColor, width=xWidth, justify=RIGHT, borderwidth=0, command=practice_mode)
        practiceButton.place(x=xPoss + 20, y=yPoss + 540)

        lanButton = Button(mainCanvas, image=lan_icon, borderwidth=2, command=lan_mode)
        lanButton.place(x=xPoss + 720, y=yPoss + 530)

    # Funcion abre la ventana de puntuaciones
    def puntuaciones(fgColor, bgColor, fonts):

        # Funcion que convierte el archivo plano Scores.txt a una lista
        def separarPuntuaciones(i):
            if i == len(listaScores):
                return
            listaScores[i] = listaScores[i].replace("\n", "").split(";")
            separarPuntuaciones(i + 1)

        file = open("Scores.txt", 'r')
        listaScores = file.readlines()
        separarPuntuaciones(0)
        file.close()

        # Funcion para cerrar ventana puntuacione
        def cerrar_puntuaciones():
            jugador = escribir_jugadores.get()
            tiempo = int(secs)
            if revisarTop(listaScores, jugador, tiempo):
                agregar_puntuaciones = open('Scores.txt', 'w')
                agregar_puntuaciones.write(listaScores[0][0] + ';' + listaScores[0][1])
                agregar_puntuaciones.write('\n')
                agregar_puntuaciones.write(listaScores[1][0] + ';' + listaScores[1][1])
                agregar_puntuaciones.write('\n')
                agregar_puntuaciones.write(listaScores[2][0] + ';' + listaScores[2][1])
                agregar_puntuaciones.write('\n')
                agregar_puntuaciones.close()
            main.deiconify()
            ventana_scores.destroy()

        # Funcion para revisar la lista y ordenar el top 3
        def revisarTop(listaScores, jugador, tiempo):
            if int(listaScores[0][1]) > tiempo:
                record1 = listaScores[0]
                record2 = listaScores[1]
                listaScores[0] = [jugador, str(tiempo)]
                listaScores[1] = record1
                listaScores[2] = record2
                return True
            elif int(listaScores[1][1]) > tiempo:
                tmp = listaScores[1]
                listaScores[1][0] = jugador
                listaScores[1][1] = str(tiempo)
                listaScores[2][0] = tmp
                return True
            elif int(listaScores[2][1]) > tiempo:
                listaScores[2][0] = jugador
                listaScores[2][1] = str(tiempo)
            else:
                return False

        main.withdraw()

        ventana_scores = Toplevel()
        ventana_scores.title("Ingreso de Jugador")

        ventana_scores.minsize(HW, HH)
        ventana_scores.resizable(width=NO, height=NO)

        canvas_scores = Canvas(ventana_scores, width=HW, height=HH, bg="black")
        canvas_scores.place(x=-1, y=0)

        label_scores = Label(canvas_scores, text="Digite iniciales del jugador:", font=fonts + str(20), fg=fgColor, bg=bgColor)
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

    if scores_game:  # Inicia la ventana para ingresar datos de puntaje
        puntuaciones('white', 'black', 'Fixedsys ')

    main.protocol('WM_DELETE_WINDOW', Quit)
    main.mainloop()


# Inicia el juego
def game_loop():
    global pause
    global secs
    global loop
    global run_game
    global starting_game_speed
    global pallets_size
    global Server
    global Cliente
    global lanBall
    global lanPallet
    global restard
    global run_lan
    global style_selected
    time1 = time.time()
    py.init()
    display = py.display.set_mode((W, H))
    py.display.set_caption('Pong')
    clock = py.time.Clock()

    # Funcion que mantiene en espera el juego en LAN mientras alguien se une
    def waiting_screen():
        global run_game
        global loop
        global Cliente
        while Server.get_receive() != 'start':
            clock.tick(FPS)
            for events in py.event.get():
                if events.type == py.QUIT:
                    Cliente = False
                    run_game = False
                    loop = False
                if events.type == py.KEYUP:
                    Cliente = False

            # Dibujar textos durante la espera
            draw_text(display, "Esperando jugador...", (HW, H * 3 / 8), ("Arial", 64, white))
            py.display.update()

    # Lan init
    if Server is not None:
        lan1 = Thread(target=Server.server)
        lan1.start()
        waiting_screen()
    if Cliente is not None:
        lan2 = Thread(target=Cliente.client)
        lan2.start()

    # Inicia la Clase Game
    game = Game(players_selected, pallets_selected, difficulty_selected, style_selected, walls_able)
    game.start_game()
    time1 = time.time()
    if run_arduino:
        ser.write(b'0')

    # Cargar fondo, sonidos y otros
    back_grounds = game.load_images()[2]
    sound_effects = game.get_sound_effects()
    music = sound_effects[2].play(loops=-1)
    M = game.get_matrix()
    walls_images = game.load_images()[3]
    walls_spawn = game.get_wall_spawn_rate()

    # Funcion que define cuando se acaba el juego
    def win_game():
        global secs
        global scores_game
        global run_game
        time2 = time.time()
        secs = time2 - time1
        run_game = False
        if game.players == 2 or game.players == 1:
            scores_game = True

    # Funcion que inicia el menu de pausa
    def show_pause():
        global run_game
        global loop
        global pause
        pause = True
        while pause:
            clock.tick(FPS)
            leerArduino()
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

    # Funcion que cambia el estilo del juego
    def switchStyle():
        global run_game
        global restard
        global style_selected
        run_game = False
        restard = True
        if style_selected == 2:
            style_selected = 0
        else:
            style_selected += 1

    # Funcion que lee los datos que envia el Arduino
    # noinspection PyArgumentList,PyBroadException
    def leerArduino():
        global volume
        global pause
        global lastTimePaused
        global lastTimeMuted
        global lastTimeStyle
        try:
            entrada = str(ser.readline())
            datos = entrada[entrada.index("'") + 1: entrada.index("\\")]
            player1 = players.get_sprite(0)
            # print(datos)

            if datos == "w":
                player1.move_pallet_up()

            if datos == "s":
                player1.move_pallet_down()

            if datos == "pause":
                pauseTime = time.time()
                if not pause and pauseTime-lastTimePaused > buttonsDelay:
                    lastTimePaused = pauseTime
                    show_pause()
                elif pause and pauseTime - lastTimePaused > buttonsDelay:
                    pause = False
                    lastTimePaused = pauseTime

            if datos == "mute":
                muteTime = time.time()
                if volume == 0 and muteTime-lastTimeMuted > buttonsDelay:
                    lastTimeMuted = muteTime
                    volume = 1
                if volume == 1 and muteTime-lastTimeMuted > buttonsDelay:
                    volume = 0
                    lastTimeMuted = muteTime

            if datos == "style":
                styleTime = time.time()
                if styleTime-lastTimeStyle > buttonsDelay:
                    lastTimeStyle = styleTime
                    switchStyle()

            if datos == '0':
                volume = 0

            if datos == '0.3':
                volume = 0.3

            if datos == '0.5':
                volume = 0.5

            if datos == '0.7':
                volume = 0.7

            if datos == '1':
                volume = 1

        except:
            pass

    # Funcion que envia los datos del contador al Arduino
    def sendArduino(score):
        global cont
        if score == cont:
            if score == 1:
                ser.write(b'1')
            elif score == 2:
                ser.write(b'2')
            elif score == 3:
                ser.write(b'3')
            elif score == 4:
                ser.write(b'4')
            elif score == 5:
                ser.write(b'5')
            elif score == 6:
                ser.write(b'6')
            elif score == 7:
                ser.write(b'7')
            elif score == 8:
                ser.write(b'8')
            elif score == 9:
                ser.write(b'9')
            cont += 1

    # Game loop
    while run_game:
        global secs
        global matrix_running
        clock.tick(FPS)
        for event in py.event.get():
            if event.type == py.QUIT:
                run_game = False
                run_lan = False
                loop = False
                if Server is not None:
                    Server.set_message('quit')
                if Cliente is not None:
                    Cliente.set_message('quit')
            if event.type == py.KEYDOWN and event.key == eval(return_key):
                run_game = False
                run_lan = False
                secs = 3
                if Server is not None:
                    Server.set_message('quit')
                if Cliente is not None:
                    Cliente.set_message('quit')
            if event.type == py.KEYUP and event.key == eval(pause_key) and Cliente is None:
                show_pause()
            if event.type == py.KEYUP and event.key == eval(matrix_key) and Cliente is None:
                if not matrix_running:
                    def star_matrix():
                        matrix_loop(M)
                    tkinter_matrix = Thread(target=star_matrix)
                    tkinter_matrix.start()
                    matrix_running = True
            if event.type == py.KEYDOWN and event.key == eval(switch_style):
                switchStyle()

        # Cronometro
        time_lapsed = py.time.get_ticks()//1000
        if secs == time_lapsed:
            secs += 1

        # Colisiones paleta con bola
        hits = py.sprite.groupcollide(players, balls, False, False)
        if hits:
            sound_effects[0].play()
            if game.wall == 1 and random.random() > walls_spawn:
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
                element.ySpeed = random.randrange(-angle_hit, angle_hit)

        # LAN mensajes del Servidor-Cliente
        if run_lan:
            localPallet = players.get_sprite(0).get_y()
            clientPallet = players.get_sprite(1).get_y()
            localBall = balls.get_top_sprite().get_ball_center()
            if Server is not None:
                Server.set_message((localPallet, localBall))
            if Cliente is not None:
                Cliente.set_message((clientPallet, localBall))

        # Arduino
        if run_arduino:
            leerArduino()
            game_scores = game.get_scores()
            score1 = game_scores[0]
            sendArduino(score1)

        # Update
        sprites.update()
        game_scores = game.get_scores()
        music.set_volume(volume)
        if game_scores[0] == top_points or game_scores[1] == top_points:
            win_game()

        # Draw
        display.blit(back_grounds, (0, 0))
        sprites.draw(display)
        draw_text(display, str(game.get_scores()[0]), M[366], ('arial', 80, white))
        draw_text(display, str(game.get_scores()[1]), M[652], ('arial', 80, white))

        py.display.update()

    # Finaliza y reinicia las variables del juego
    starting_game_speed = 0
    pallets_size = 0
    for sprite in sprites:
        sprite.kill()
    Server = None
    Cliente = None
    if run_arduino:
        ser.write(b'0')
    py.quit()


# Controla los ciclos entre menu y juego
while loop:
    menu_loop()
    if run_game:
        game_loop()
    while restard:
        run_game = True
        restard = False
        game_loop()
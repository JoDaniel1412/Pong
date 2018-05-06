import pygame as py
import sys
import random
import time

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)

# Variables
W, H = 1400, 800
HW, HH = W / 2, H / 2
FPS = 60


# Clase usada para iniciar el juego con determinados ajustes
# Instancias: cantidad de jugadores(1 o 2), cantidad de paletas(1 o 2), difficultad(0, 1 o 2)
class Game:
    def __init__(self, player, pallets, difficulty):
        self.players = player
        self.pallets = pallets
        self.difficulty = difficulty
        self.matrix = []

    def get_matrix(self):  # Metodo para generar matriz
        n, m = 25, 40
        i, j = 0, 0
        x, y = W // m, H // n
        while W >= i:
            while H >= j:
                self.matrix.append([i, j])
                j += y
            i += x
            j = 0

    def start_game(self):  # Metodo para iniciar el juego
        self.get_matrix()
        poss1 = 38
        poss2 = 1000
        if self.players == 1:
            humane = Player(('py.K_w', 'py.K_s'), self.difficulty, self.matrix[poss1], self.matrix, (True, 'HUMANE'))
            cpu = Player('', self.difficulty, self.matrix[poss2], self.matrix, (True, 'CPU'))
            sprites.add(humane)
            sprites.add(cpu)
            players.add(humane)
            players.add(cpu)
        if self.players == 2:
            humane1 = Player(('py.K_w', 'py.K_s'), self.difficulty, self.matrix[poss1], self.matrix, (True, 'HUMANE'))
            humane2 = Player(('py.K_UP', 'py.K_DOWN'), self.difficulty, self.matrix[poss2], self.matrix, (True, 'HUMANE'))
            sprites.add(humane1)
            sprites.add(humane2)
            players.add(humane1)
            players.add(humane2)
        ball = Ball(self.difficulty)
        sprites.add(ball)
        balls.add(ball)


# Clase que crea las paletas de los jugadores
# Instancias: controles del jugador, difficultad, posicion de las paletas, la matrix, el estado(vivo, humano/computador)
class Player(py.sprite.Sprite):
    def __init__(self, keys, difficulty, poss, matrix, status):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        size = self.set_pallets_size()
        self.pallet_size = matrix[12][1] - matrix[12-size][1]
        self.status = status
        self.keys = keys
        self.speed = self.set_speed()
        self.image = py.Surface((15, self.pallet_size))
        self.rect = self.image.get_rect()
        self.image.fill(white)
        self.rect.center = poss

    def pallet_segments(self):  # Metodo que retorna una lista con los segmentos de la paleta
        segment = self.pallet_size / 3
        return [self.rect.top] + [self.rect.top+segment] + [self.rect.bottom-segment] + [self.rect.bottom]

    def set_pallets_size(self):  # Metodo que ajusta el largo de la paleta segun dificultad
        if self.difficulty == 0:
            return 9
        if self.difficulty == 1:
            return 6
        if self.difficulty == 2:
            return 3

    def set_speed(self):  # Metodo que ajusta la velocidad de la paleta segun dificultad
        if self.difficulty == 0:
            return 7
        if self.difficulty == 1:
            return 10
        if self.difficulty == 2:
            return 15

    def update(self):  # Metodo que actualiza la posicion de la paleta en la pantalla
        k = py.key.get_pressed()
        if self.status[0] and self.status[1] == 'HUMANE':
            if k[eval(self.keys[0])] and self.rect.top > 0:
                self.rect.y -= self.speed
            if k[eval(self.keys[1])] and self.rect.bottom < H:
                self.rect.y += self.speed
        if self.status[0] and self.status[1] == 'CPU':
            pass


# Clase que crea la pelota
# Instancias: la difficultad
class Ball(py.sprite.Sprite):
    def __init__(self, difficulty):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = (HW, HH)
        self.size = self.set_size()
        self.image = py.Surface((self.size, self.size))
        self.image.fill(white)
        self.rect = self.image.get_rect()
        self.rect.center = self.poss
        self.speed = self.set_speed()
        self.xSpeed = random.choice(self.speed)
        self.ySpeed = random.choice(self.speed)

    def get_ball_poss(self):
        return self.rect.center

    def set_ySpeed(self, collision):  # Metodo que hace a la pelota cambiar de direccion en caso de colisionar con la paleta
        if collision == 'top':
            self.ySpeed = self.speed[0]
        if collision == 'center':
            self.ySpeed = 0
        if collision == 'bottom':
            self.ySpeed = self.speed[1]

    def set_xSpeed(self):
        self.xSpeed = -self.xSpeed

    def set_speed(self):  # Metodo que ajusta la velocidad de la pelota segun dificultad
        if self.difficulty == 0:
            return [-6, 6]
        if self.difficulty == 1:
            return [-8, 8]
        if self.difficulty == 2:
            return [-10, 10]

    def set_size(self):  # Metodo que ajusta el radio de la bola segun dificultad
        if self.difficulty == 0:
            return 30
        if self.difficulty == 1:
            return 20
        if self.difficulty == 2:
            return 10

    def new_ball(self):  # Metodo que crea una bola cada vez que se anota un punto
        newBall = Ball(self.difficulty)
        sprites.add(newBall)
        balls.add(newBall)

    def update(self):  # Metodo que actualiza la posicion de la pelota en la pantalla
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if self.rect.y < 0 or self.rect.y > H:
            self.ySpeed = -self.ySpeed
        if self.rect.left < 0:
            time.sleep(1)
            self.kill()
            self.new_ball()

        if self.rect.right > W:
            time.sleep(1)
            self.kill()
            self.new_ball()


# Initialize PyGame
py.init()
py.mixer.init()
display = py.display.set_mode((W, H))
py.display.set_caption('Pong')
clock = py.time.Clock()

# Sprite Groups
sprites = py.sprite.Group()
players = py.sprite.Group()
balls = py.sprite.Group()

game = Game(2, 1, 1)
game.start_game()

# Game loop
loop = True
while loop:
    clock.tick(FPS)
    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            loop = False
            py.quit()
            sys.exit()

    # Collisions
    if py.sprite.groupcollide(balls, players, False, False):
        for element in balls:
            element.set_xSpeed()
            for pallet in players:
                ball_poss = element.get_ball_poss()[1]
                pallet_segment = pallet.pallet_segments()
                print(ball_poss, pallet_segment)
                if pallet_segment[0] <= ball_poss < pallet_segment[1]:  # Revisa si la bola choca en la parte superior
                    element.set_ySpeed('top')
                if pallet_segment[1] <= ball_poss <= pallet_segment[2]:  # Revisa si la bola choca en la parte central
                    element.set_ySpeed('center')
                if pallet_segment[2] < ball_poss <= pallet_segment[3]:  # Revisa si la bola choca en la parte inferior
                    element.set_ySpeed('bottom')

    # Update
    sprites.update()

    # Draw
    display.fill(black)
    sprites.draw(display)

    py.display.update()
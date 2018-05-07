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
W, H = 1500, 800
HW, HH = W / 2, H / 2
FPS = 60


# Clase usada para iniciar el juego con determinados ajustes
# Instancias: cantidad de jugadores(1 o 2), cantidad de paletas(1 o 2), difficultad(0, 1 o 2)
class Game:
    def __init__(self, player, pallets, difficulty, style):
        self.players = player
        self.pallets = pallets
        self.difficulty = difficulty
        self.style = style
        self.images = self.load_images()
        self.sound_effects = self.load_sounds()
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
        images = self.images[0]
        poss1 = 38
        poss2 = 1026
        poss3 = poss1 + 5
        poss4 = poss2 + 5
        if self.players == 1:
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane2 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                cpu2 = Player('', self.difficulty, poss4, self.matrix, [True, 'CPU'], images[3], self.pallets)
                sprites.add(humane2)
                sprites.add(cpu2)
                players.add(humane2)
                players.add(cpu2)
            humane = Player(('py.K_w', 'py.K_s'), self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            cpu = Player('', self.difficulty, poss2, self.matrix, [True, 'CPU'], images[2], self.pallets)
            sprites.add(humane)
            sprites.add(cpu)
            players.add(humane)
            players.add(cpu)

        if self.players == 2:
            if self.pallets == 2:
                poss1 -= 4
                poss2 -= 4
                humane1 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss3, self.matrix, [True, 'HUMANE'], images[1], self.pallets)
                humane2 = Player(('py.K_UP', 'py.K_DOWN'), self.difficulty, poss4, self.matrix, [True, 'HUMANE'], images[3], self.pallets)
                sprites.add(humane1)
                sprites.add(humane2)
                players.add(humane1)
                players.add(humane2)
            humane1 = Player(('py.K_w', 'py.K_s'), self.difficulty, poss1, self.matrix, [True, 'HUMANE'], images[0], self.pallets)
            humane2 = Player(('py.K_UP', 'py.K_DOWN'), self.difficulty, poss2, self.matrix, [True, 'HUMANE'], images[2], self.pallets)
            sprites.add(humane1)
            sprites.add(humane2)
            players.add(humane1)
            players.add(humane2)
        ball = Ball(self.difficulty, self.images[1])
        sprites.add(ball)
        balls.add(ball)

    def load_images(self):  # Metodo para cargar imagenes
        pallet_images = []
        if self.style == 0:
            white_pallet = py.Surface((10, 20))
            white_pallet.fill(white)
            ball = py.Surface((10, 10))
            ball.fill(white)
            bg = py.image.load('img/deffault_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [white_pallet, white_pallet, white_pallet, white_pallet]
        if self.style == 1:
            player_red = py.image.load('img/player_red.png').convert_alpha()
            player_green = py.image.load('img/player_green.png').convert_alpha()
            player_pink = py.image.load('img/player_pink.png').convert_alpha()
            player_blue = py.image.load('img/player_blue.png').convert_alpha()
            ball = py.image.load('img/neon_ball.png').convert_alpha()
            bg = py.image.load('img/neon_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [player_red, player_green, player_pink, player_blue]
        if self.style == 2:
            player_bat = py.image.load('img/player_bat.png').convert_alpha()
            ball = py.image.load('img/baseball_ball.png').convert_alpha()
            pallet_images = [player_bat, player_bat, player_bat, player_bat]
            bg = py.image.load('img/baseball_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
        return pallet_images, ball, bg

    def load_sounds(self):
        if self.style == 0:
            bounce = py.mixer.Sound('sound/deffault_bounce.wav')
            score = py.mixer.Sound('sound/deffault_score.wav')
        if self.style == 1:
            bounce = py.mixer.Sound('sound/neon_bounce.wav')
            score = py.mixer.Sound('sound/neon_score.wav')
        if self.style == 2:
            bounce = py.mixer.Sound('sound/baseball_bounce.wav')
            score = py.mixer.Sound('sound/baseball_bounce.wav')
        return bounce, score

    def get_sound_effects(self):
        return self.sound_effects



# Clase que crea las paletas de los jugadores
# Instancias: controles del jugador, difficultad, posicion de las paletas, la matrix, el estado(vivo, humano/computador)
class Player(py.sprite.Sprite):
    def __init__(self, keys, difficulty, poss, matrix, status, image, pallets):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.pallets = pallets
        size = self.set_pallets_size()
        self.pallet_size = matrix[12][1] - matrix[12-size][1]
        self.status = status
        self.keys = keys
        self.matrix = matrix
        self.speed = self.set_speed()
        self.image = py.transform.scale(image, (20, self.pallet_size))
        self.rect = self.image.get_rect()
        self.rect.center = self.matrix[poss]

    def pallet_segments(self):  # Metodo que retorna una lista con los segmentos de la paleta
        segment = self.pallet_size / 3
        return [self.rect.top] + [self.rect.top+segment] + [self.rect.bottom-segment] + [self.rect.bottom]

    def set_pallets_size(self):  # Metodo que ajusta el largo de la paleta segun dificultad
        if self.difficulty == 0:
            large = 9
        if self.difficulty == 1:
            large = 6
        if self.difficulty == 2:
            large = 3
        return large

    def set_speed(self):  # Metodo que ajusta la velocidad de la paleta segun dificultad
        if self.difficulty == 0:
            speed =  7
        if self.difficulty == 1:
            speed = 10
        if self.difficulty == 2:
            speed = 15
        return speed

    def increase_xSpeed(self):
        self.speed_limit = 30
        if self.speed_limit > self.speed > 0:
            self.speed += 1
        if -self.speed_limit < self.speed < 0:
            self.speed -= 1

    def set_status(self, boolean):
        self.status[0] = boolean

    def update(self):  # Metodo que actualiza la posicion de la paleta en la pantalla
        k = py.key.get_pressed()
        if self.pallets == 2:
            if self.status[0] and self.status[1] == 'HUMANE':
                if k[eval(self.keys[0])]:
                    self.rect.y -= self.speed
                if k[eval(self.keys[1])]:
                    self.rect.y += self.speed
            if self.status[0] and self.status[1] == 'CPU':
                pass
            if self.rect.bottom < 0:
                self.rect.top = H
            if self.rect.top > H:
                self.rect.bottom = 0
        else:
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
    def __init__(self, difficulty, image):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = (HW, HH)
        self.size = self.set_size()
        self.image = py.transform.scale(image, (self.size, self.size))
        self.rect = self.image.get_rect()
        self.rect.center = self.poss
        self.speed = self.set_speed()
        self.xSpeed = random.choice(self.speed)
        self.ySpeed = random.choice(self.speed)
        self.sound_effects = game.get_sound_effects()

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

    def increase_xSpeed(self):
        self.speed_limit = 30
        if self.speed_limit > self.xSpeed > 0:
            self.xSpeed += 1
        if -self.speed_limit < self.xSpeed < 0:
            self.xSpeed -= 1

    def set_speed(self):  # Metodo que ajusta la velocidad de la pelota segun dificultad
        if self.difficulty == 0:
            speed_range = [-6, 6]
        if self.difficulty == 1:
            speed_range = [-8, 8]
        if self.difficulty == 2:
            speed_range = [-10, 10]
        return speed_range

    def set_size(self):  # Metodo que ajusta el radio de la bola segun dificultad
        if self.difficulty == 0:
            ball_size = 55
        if self.difficulty == 1:
            ball_size = 40
        if self.difficulty == 2:
            ball_size = 25
        return  ball_size

    def new_ball(self):  # Metodo que crea una bola cada vez que se anota un punto
        newBall = Ball(self.difficulty, self.image)
        sprites.add(newBall)
        balls.add(newBall)

    def update(self):  # Metodo que actualiza la posicion de la pelota en la pantalla
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if self.rect.top < 0 or self.rect.bottom > H:
            self.ySpeed = -self.ySpeed
            self.sound_effects[0].play()
        if self.rect.left < 0:
            self.sound_effects[1].play()
            time.sleep(1)
            self.kill()
            self.new_ball()

        if self.rect.right > W:
            self.sound_effects[1].play()
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

game = Game(2, 1, 1, 0)
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

    # Sound
    sound_effects = game.get_sound_effects()
    back_grounds = game.load_images()[2]

    # Collisions
    if py.sprite.groupcollide(balls, players, False, False):
        sound_effects[0].play()
        for element in balls:
            element.set_xSpeed()
            for pallet in players:
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

    # Update
    sprites.update()

    # Draw
    display.blit(back_grounds, (0, 0))
    sprites.draw(display)

    py.display.update()
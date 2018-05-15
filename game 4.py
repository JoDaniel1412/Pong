import pygame as py
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
W, H = 1600, 900
HW, HH = W / 2, H / 2
FPS = 60
secs = 0


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
        self.make_matrix()
        self.score1 = 0
        self.score2 = 0

    def make_matrix(self):  # Metodo para generar matriz
        n, m = 25, 40
        i, j = 0, 0
        x, y = W // m, H // n
        while W >= i:
            while H >= j:
                self.matrix.append([i, j])
                j += y
            i += x
            j = 0

    def get_matrix(self):
        return self.matrix

    def start_game(self):  # Metodo para iniciar el juego
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

    def load_images(self):  # Metodo para cargar imagenes del juego
        pallet_images = None
        ball = None
        bg = None
        if self.style == 0:
            white_pallet = py.image.load('img/default_pallet.png').convert_alpha()
            ball = py.Surface((10, 10))
            ball.fill(white)
            bg = py.image.load('img/default_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [white_pallet, white_pallet, white_pallet, white_pallet]
        if self.style == 1:
            player_red = py.image.load('img/neon_red.png').convert_alpha()
            player_green = py.image.load('img/neon_green.png').convert_alpha()
            player_pink = py.image.load('img/neon_pink.png').convert_alpha()
            player_blue = py.image.load('img/neon_blue.png').convert_alpha()
            ball = py.image.load('img/neon_ball.png').convert_alpha()
            bg = py.image.load('img/neon_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
            pallet_images = [player_red, player_green, player_pink, player_blue]
        if self.style == 2:
            player_bat = py.image.load('img/baseball_bat.png').convert_alpha()
            ball = py.image.load('img/baseball_ball.png').convert_alpha()
            pallet_images = [player_bat, player_bat, player_bat, player_bat]
            bg = py.image.load('img/baseball_bg.png').convert()
            bg = py.transform.scale(bg, (W, H))
        return pallet_images, ball, bg

    def load_sounds(self):  # Metodo para cargar la musica del juego
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

    def get_sound_effects(self):  # Metodo para obtener los sonidos del juego
        return self.sound_effects

    def add_score1(self):  # Metodo que ajusta el puntaje del jugador 1
        self.score1 += 1
        for pallets in players:
            pallets.reset_speed()

    def add_score2(self):  # Metodo que ajusta el puntaje del jugador 2
        self.score2 += 1
        for pallets in players:
            pallets.reset_speed()

    def get_scores(self):
        return self.score1, self.score2


def draw_text(surf, text, poss, font):
    font_type = py.font.match_font(font[0])
    make_font = py.font.Font(font_type, font[1])
    text_surface = make_font.render(text, True, font[2])
    rect = text_surface.get_rect()
    rect.center = poss
    surf.blit(text_surface, rect)


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
        self.default_speed = self.speed
        self.image = py.transform.scale(image, (25, self.pallet_size))
        self.rect = self.image.get_rect()
        self.rect.center = self.matrix[poss]
        self.speed_limit = 40

    def pallet_segments(self):  # Metodo que retorna una lista con los segmentos de la paleta
        segment = self.pallet_size / 3
        return [self.rect.top] + [self.rect.top+segment] + [self.rect.bottom-segment] + [self.rect.bottom]

    def set_pallets_size(self):  # Metodo que ajusta el largo de la paleta segun dificultad
        large = 0
        if self.difficulty == 0:
            large = 9
        if self.difficulty == 1:
            large = 6
        if self.difficulty == 2:
            large = 3
        return large

    def set_speed(self):  # Metodo que ajusta la velocidad de la paleta segun dificultad
        speed = 0
        if self.difficulty == 0:
            speed = 7
        if self.difficulty == 1:
            speed = 10
        if self.difficulty == 2:
            speed = 15
        return speed

    def increase_xSpeed(self):  # Metodo para aumentar la velocidad progresivamente
        if self.speed_limit > self.speed > 0:
            self.speed += 1
        if -self.speed_limit < self.speed < 0:
            self.speed -= 1

    def reset_speed(self):
        self.speed = self.default_speed

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
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        self.rect.y = y
                    if self.difficulty == 1:
                        if secs % 2 == 0:
                            self.rect.y = y
                    if self.difficulty == 0:
                        if secs % 3 == 0:
                            self.rect.y = y
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
                for ball in balls:
                    y = ball.get_ball_yPoss()
                    if self.difficulty == 2:
                        self.rect.y = y
                    if self.difficulty == 1:
                        if secs % 2 == 0:
                            self.rect.y = y
                    if self.difficulty == 0:
                        if secs % 3 == 0:
                            self.rect.y = y


# Clase que crea la pelota
# Instancias: la difficultad
class Ball(py.sprite.Sprite):
    def __init__(self, difficulty, image):
        py.sprite.Sprite.__init__(self)
        self.difficulty = difficulty
        self.poss = (HW, HH)
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

    def rotate(self):  # Metodo para rotar la imagen de la bola
        self.last_rotation += self.rotation_speed
        self.image = py.transform.rotate(self.original_image, self.last_rotation)

    def get_ball_poss(self):  # Metodo para obtener la posicion de la bola
        return self.rect.center

    def get_ball_yPoss(self):
        return self.rect.y

    def set_ySpeed(self, collision):  # Metodo que hace a la pelota cambiar de direccion en caso de colisionar con la paleta
        if collision == 'top':
            self.ySpeed = self.speed[0]
        if collision == 'center':
            self.ySpeed = 0
        if collision == 'bottom':
            self.ySpeed = self.speed[1]

    def set_xSpeed(self):  # Metodo para invertir la direccion de la bola al rebotar
        self.xSpeed = -self.xSpeed

    def increase_xSpeed(self):  # Metodo para aumentar la velocidad progresivamente
        if self.speed_limit > self.xSpeed > 0:
            self.xSpeed += 1
        if -self.speed_limit < self.xSpeed < 0:
            self.xSpeed -= 1

    def set_speed(self):  # Metodo que ajusta la velocidad de la pelota segun dificultads
        speed_range = [0, 0]
        if self.difficulty == 0:
            speed_range = [-6, 6]
        if self.difficulty == 1:
            speed_range = [-8, 8]
        if self.difficulty == 2:
            speed_range = [-10, 10]
        return speed_range

    def set_size(self):  # Metodo que ajusta el radio de la bola segun dificultad
        ball_size = 0
        if self.difficulty == 0:
            ball_size = 55
        if self.difficulty == 1:
            ball_size = 40
        if self.difficulty == 2:
            ball_size = 25
        return ball_size

    def new_ball(self):  # Metodo que crea una bola cada vez que se anota un punto
        newBall = Ball(self.difficulty, self.original_image)
        sprites.add(newBall)
        balls.add(newBall)

    def update(self):  # Metodo que actualiza la posicion de la pelota en la pantalla
        self.rotate()
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        if self.rect.top <= 0 or self.rect.bottom >= H:
            self.ySpeed = -self.ySpeed
            self.sound_effects[0].play()
        if self.rect.left < 0:
            self.sound_effects[1].play()
            game.add_score2()
            time.sleep(1)
            self.kill()
            self.new_ball()
        if self.rect.right > W:
            self.sound_effects[1].play()
            game.add_score1()
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

# Inicia la Clase Game
game = Game(1, 1, 1, 0)
game.start_game()

# Cargar fondo y sonidos
back_grounds = game.load_images()[2]
sound_effects = game.get_sound_effects()
sound_effects[2].play(loops=-1)
M = game.get_matrix()

# Game loop
loop = True
while loop:
    clock.tick(FPS)
    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            loop = False

    # Time
    start_time = py.time.get_ticks()//1000
    if secs == start_time:
        secs += 1

    # Collisions
    hits = py.sprite.groupcollide(players, balls, False, False)
    if hits:
        sound_effects[0].play()
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

    # Update
    sprites.update()

    # Draw
    display.blit(back_grounds, (0, 0))
    sprites.draw(display)
    draw_text(display, str(game.get_scores()[0]), M[366], ('arial', 80, white))
    draw_text(display, str(game.get_scores()[1]), M[652], ('arial', 80, white))

    py.display.update()


py.quit()
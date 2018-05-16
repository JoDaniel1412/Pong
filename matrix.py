import pygame as py
from settings import *
from pong import game


# Initialize PyGame
py.init()
display = py.display.set_mode((W2, H2))
clock = py.time.Clock()


def draw_matrix():
    M = game.get_matrix()
    for n in range(0, H2, H2//25):
        py.draw.line(display, white, (0, n), (W2, n))
    for m in range(0, W2, W2//40):
        py.draw.line(display, white, (m, 0), (m, H2))


# Main loop
running = True
while running:
    clock.tick(FPS)
    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            running = False

    # Draw
    draw_matrix()

    py.display.update()


py.quit()
import pygame as py
from settings import *
from pong import game


# Initialize PyGame
py.init()
display = py.display.set_mode((W//2, H//2))
clock = py.time.Clock()


def draw_matrix():
    M = game.get_matrix()
    for n in range(H):
        py.draw.line()


# Main loop
running = True
while running:
    clock.tick(FPS)
    for event in py.event.get():
        if event.type == py.QUIT or (event.type == py.KEYDOWN and event.key == py.K_ESCAPE):
            running = False

    py.display.update()


py.quit()
import pygame
import random
import sys

from pygame import QUIT

DISPLAYSURF = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

tick = 0


def getRect():
    return pygame.Rect((50, 50, 50, 50))


def colorChange():
    global tick
    if tick == FPS:
        tick = 0
        DISPLAYSURF.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    else:
        tick += 1


while True:
    colorChange()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()

    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), getRect())

    pygame.display.update()
    fpsClock.tick(FPS)

import pygame
import random
import sys

from pygame import QUIT

DISPLAYSURF = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

tick = 0


def drawRect(pos):
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (pos[0], pos[1], 50, 50))


def colorChange():
    global tick
    if tick == FPS:
        tick = 1
        DISPLAYSURF.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        drawRect([random.randint(0, 750), random.randint(0, 750)])
    else:
        tick += 1


while True:
    colorChange()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()

    pygame.display.update()
    fpsClock.tick(FPS)

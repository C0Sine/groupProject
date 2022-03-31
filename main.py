import pygame
import random
import sys

from pygame import QUIT

DISPLAYSURF = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

tick = 0
linetick = 0

def drawCircle(radius,x,y,color):
    global tick
    if tick == FPS:
        tick = 0
        pygame.draw.circle(DISPLAYSURF,color,(x,y),radius)
    else:
        tick += 1
def colorChange():
    global tick
    if tick == FPS:
        tick = 1
        DISPLAYSURF.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    else:
        tick += 1


def drawLine():
    global linetick
    if linetick == FPS:
        linetick = 1
        pygame.draw.line(DISPLAYSURF, (0, 0, 0), (random.randint(0, DISPLAYSURF.get_width()), random.randint(0, DISPLAYSURF.get_height())), (random.randint(0, DISPLAYSURF.get_width()), random.randint(0, DISPLAYSURF.get_height())))
        print("lol")
    else:
        linetick += 1


while True:
    drawCircle(random.randint(10, 50), random.randint(0, 800), random.randint(0, 800),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
    colorChange()
    drawLine()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
    pygame.display.update()
    fpsClock.tick(FPS)

import pygame
import random
import sys

from pygame import QUIT

DISPLAYSURF = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

tick = 0
linetick = 0
circleTick=30

def drawRect(pos):
    pygame.draw.rect(DISPLAYSURF, (0, 0, 0), (pos[0], pos[1], 50, 50))






def drawCircle(radius,x,y,color,keyHit):
    global circleTick
    if keyHit:
        pygame.draw.circle(DISPLAYSURF, color, (x, y), radius)
    if circleTick == FPS:
        circleTick = 0
        pygame.draw.circle(DISPLAYSURF,color,(x,y),radius)
    else:
        circleTick += 1
def colorChange():
    global tick
    if tick == FPS:
        tick = 1
        DISPLAYSURF.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        drawRect([random.randint(0, 750), random.randint(0, 750)])
    else:
        tick += 1


def drawLine():
    global linetick
    if linetick == FPS:
        linetick = 60
        pygame.draw.line(DISPLAYSURF, (0, 0, 0), (random.randint(0, DISPLAYSURF.get_width()), random.randint(0, DISPLAYSURF.get_height())), (random.randint(0, DISPLAYSURF.get_width()), random.randint(0, DISPLAYSURF.get_height())))
        print("lol")
    else:
        linetick += 1


while True:
    colorChange()
    drawCircle(random.randint(50, 100), random.randint(0, 800), random.randint(0, 800),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),False)
    drawLine()
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                drawRect([random.randint(0, 750), random.randint(0, 750)])
            if event.key == pygame.K_c:
                drawCircle(random.randint(50, 100), random.randint(0, 800), random.randint(0, 800),(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),True)
            if event.key == pygame.K_l:
                for i in range(0, 1000):
                    pygame.draw.line(DISPLAYSURF, (0, 0, 0), (random.randint(0, DISPLAYSURF.get_width()), random.randint(0, DISPLAYSURF.get_height())), (random.randint(0, DISPLAYSURF.get_width()),random.randint(0, DISPLAYSURF.get_height())))

    pygame.display.update()
    fpsClock.tick(FPS)

import pygame
import random
import sys

from pygame import QUIT

surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

maskimage = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
mask = pygame.mask.from_surface(maskimage)

while True:
    surface.fill((255, 255, 255))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()

    surface.blit(maskimage, (0, 0))

    pygame.display.update()
    fpsClock.tick(FPS)

import keyboard as keyboard
import pygame
import random
import sys

from pygame import QUIT

surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60

# maskimage = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
# mask = pygame.mask.from_surface(maskimage)

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
        self.image.set_colorkey((255, 255, 255))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


testMap = Map()


class wallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('wallTest2.png'), (800, 800))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


weirdWall = wallTest()
weirdWall.rect.x, weirdWall.rect.y = 100, 100


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create a player mask from a given sprite
        self.image = pygame.image.load('datBoi.png')
        self.mask = pygame.mask.from_surface(self.image)
        self.oldX, self.oldY = 0, 0
        self.rect = self.image.get_rect()
        # X and Y position variables for player movement
        self.posX, self.posY = 300, 300

    def updatePosition(self, xDif, yDif):
        # Method that runs every tick to update the position if velX/velY != 0
        self.rect.x += xDif
        self.rect.y += yDif

    # def updateSelf(self):
    #     self.rect = pygame.image.


player = Player()
player.rect.x, player.rect.y = 300, 300

while True:
    surface.fill((255, 255, 255))
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()

    if keyboard.is_pressed('a') or keyboard.is_pressed('Left'):
        player.updatePosition(-5, 0)
    if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):
        player.updatePosition(5, 0)
    if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):
        player.updatePosition(0, 5)
    if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):
        player.updatePosition(0, -5)

    if pygame.sprite.collide_mask(player, weirdWall):
        player.rect.x, player.rect.y = player.oldX, player.oldY


    surface.blit(testMap.image, (0, 0))
    surface.blit(player.image, player.rect)
    surface.blit(weirdWall.image, weirdWall.rect)
    pygame.display.update()
    fpsClock.tick(FPS)

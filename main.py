import keyboard as keyboard
import pygame
import random
import sys
import math

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
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


testMap = Map()


class WallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('shapeTest.png'), (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


weirdWall = WallTest()
weirdWall.rect.x, weirdWall.rect.y = 100, 100

class LightSource():
    def __init__(self, location, direction, width, strength):
        # direction and width in degrees

        self.location = location
        self.direction = direction
        self.width = width
        self.strength = strength
        self.points = []

    def calculateLights(self):

        for angle in range(self.direction, self.direction + self.width):
            point, lastLocation = [], []
            len = 1
            while point == []:

                lastLocation[0], lastLocation[1] = point[0], point[1]
                point = [self.location[0] + math.cos(angle), self.location[1] * math.cos(angle)]

                if pygame.sprite.collide_mask(pygame.draw.line((0, 255, 255), (self.location[0], self.location[1]), (self.location[0], self.location[1]), (self.location[0] + math.cos(angle), self.location[1] * math.cos(angle))), testMap):
                    self.points.append(lastLocation)

                else:  # Increment Len
                    len += 1


    def drawLights(self):
        pygame.draw.line((0, 255, 255), (self.location[0], self.location[1]), (self.location[0], self.location[1]),
                          (self.points[0][0], self.points[0][1]))
        pygame.draw.line((0, 255, 255), (self.location[0], self.location[1]), (self.location[0], self.location[1]),
                         (self.points[len(self.points) - 1][0], self.points[len(self.points) - 1][1]))

        #loop through points and draw lines between the ones that follow each other in the array

    #def makeLayer(self):


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
fakePlayer = Player()
# Fake player is an invisible "Player" used to detect collisions
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

    if pygame.sprite.collide_mask(player, testMap) or pygame.sprite.collide_mask(player, weirdWall):
        # Takes the fake player and, using the oldX or oldY, checks to see if it can move in the opposite direction
        # For example, if it takes oldY, it will check to see if it could move left or right from the original position
        # Any instance of which it would collide, returns it to the original X or Y, independently, allowing for diagonal movement
        fakePlayer.rect.x, fakePlayer.rect.y = player.rect.x - 5, player.oldY
        if pygame.sprite.collide_mask(fakePlayer, testMap) or pygame.sprite.collide_mask(fakePlayer, weirdWall):
            player.rect.x = player.oldX

        fakePlayer.rect.x, fakePlayer.rect.y = player.rect.x + 5, player.oldY
        if pygame.sprite.collide_mask(fakePlayer, testMap) or pygame.sprite.collide_mask(fakePlayer, weirdWall):
            player.rect.x = player.oldX

        fakePlayer.rect.x, fakePlayer.rect.y = player.oldX, player.rect.y - 5
        if pygame.sprite.collide_mask(fakePlayer, testMap) or pygame.sprite.collide_mask(fakePlayer, weirdWall):
            player.rect.y = player.oldY

        fakePlayer.rect.x, fakePlayer.rect.y = player.oldX, player.rect.y + 5
        if pygame.sprite.collide_mask(fakePlayer, testMap) or pygame.sprite.collide_mask(fakePlayer, weirdWall):
            player.rect.y = player.oldY

    surface.blit(testMap.image, testMap.rect)
    surface.blit(player.image, player.rect)
    surface.blit(weirdWall.image, weirdWall.rect)
    pygame.display.update()
    fpsClock.tick(FPS)

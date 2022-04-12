import keyboard as keyboard
import pygame
import random
import sys

from pygame import QUIT

surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60


class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()

    def loadMap(self, file):  # takes text file of map
        with open(file) as ins:
            arr = []
            for line in ins:  # creates an array based on the text file
                number_strings = line.split()
                numbers = [n for n in number_strings]
                arr.append(numbers)
        tempsurf = pygame.Surface((len(arr[0]) * 25, len(arr) * 25))  # surface for walls
        tempsurf.fill((255, 255, 255))  # whitespace will be non-collideable
        for i in range(0, len(arr)):  # parses array to create walls on tempsurf
            for j in range(0, len(arr[0])):
                if arr[i][j] == 'x':  # x is used to assign a wall, any other character works for empty space
                    pygame.draw.rect(tempsurf, (0, 0, 0), (j * 25, i * 25, 25, 25))
        tempsurf.set_colorkey((255, 255, 255))  # sets white to transparent, allowing movement in those areas
        self.image = tempsurf  # sets map to the loaded map
        self.mask = pygame.mask.from_surface(tempsurf)
        self.rect = self.mask.get_rect()


testMap = Map()

testMap.loadMap('map1.txt')


class WallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('shapeTest.png'), (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


weirdWall = WallTest()
weirdWall.rect.x, weirdWall.rect.y = 100, 100


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create a player mask from a given sprite
        self.image = pygame.transform.scale(pygame.image.load('datBoi.png'), (50, 50))
        self.mask = pygame.mask.from_surface(self.image)
        self.oldX, self.oldY = 0, 0
        self.rect = self.image.get_rect()
        # X and Y position variables for player movement
        self.posX, self.posY = 300, 300

    def updatePosition(self, xDif, yDif):
        # Method that runs every tick to update the position if velX/velY != 0
        self.rect.x += xDif
        self.rect.y += yDif

    def updateCollisionPosition(self, direction):
        offset = (self.rect.x - testMap.rect.x, self.rect.y - testMap.rect.y)
        while pygame.sprite.collide_mask(self, testMap):
            if direction.__contains__('Left'):
                self.rect.x += self.mask.overlap_mask(testMap.mask, offset).get_rect().width - self.rect.width + 1
            if direction.__contains__('Right'):
                self.rect.x -= self.mask.overlap_mask(testMap.mask, offset).get_rect().width - self.rect.width + 1
            if direction.__contains__('Down'):
                self.rect.y -= self.mask.overlap_mask(testMap.mask, offset).get_rect().height - self.rect.width + 1
            if direction.__contains__('Up'):
                self.rect.y += self.mask.overlap_mask(testMap.mask, offset).get_rect().height - self.rect.width + 1

    # def updateSelf(self):
    #     self.rect = pygame.image.

    def createLOSLine(self, Target):
        LOSLine = pygame.draw.line(surface, (0, 0, 0),
                                   (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
                                   (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
        # pygame.draw.line(surface, (0, 0, 0), (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
        if LOSLine.colliderect(Target):
            LOSLine = pygame.draw.line(surface, (0, 255, 0),
                                       (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
                                       (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
        # else: LOSLine = pygame.draw.line(surface, (0, 255, 0), (self.rect.x + self.rect.width / 2, self.rect.y +
        # self.rect.height / 2), (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('dave.jpg'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()


dave = Enemy()
dave.rect.x, dave.rect.y = 200, 200

player = Player()


class LOSBullet(pygame.sprite.Sprite):
    def __init__(self, Origin, Target):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'), (10, 10))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.origin, self.target = Origin, Target
        self.rect.center = self.origin.rect.center

    def checkLOS(self):
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'), (10, 10))  # Ensures the default image is a black 10x10 square
        self.rect.x = self.origin.rect.x + self.origin.rect.width / 2  # Align the start of the bullets with the start of the origin(X direction)
        self.rect.y = self.origin.rect.y + self.origin.rect.height / 2  # Align the start of the bullets with the start of the origin(Y direction)
        moveX = int(self.target.rect.centerx - self.rect.centerx)  # Creates the X component of the "slope"
        moveY = int(self.target.rect.centery - self.rect.centery)  # Creates the Y component of the "slope"
        lostLOS = False  # A variable that will read TRUE if line of sight is ever broken

        for i in range(29):  # Create and check 29 points
            self.rect.centerx += moveX / 29  # Moves the bullet 1 29th of the total center-to-center distance(X)
            self.rect.centery += moveY / 29  # Moves the bullet 1 29th of the total center-to-center distance(Y)

            if pygame.sprite.collide_mask(self, testMap):  # If even ONE 'bullet' collides with our map, lostLOS becomes TRUE
                lostLOS = True
                self.image = pygame.transform.scale(pygame.image.load('LOSBroken.png'), (10, 10))  # Make it so the colliding bullets and everything past appear red

            surface.blit(self.image, self.rect)  # Blit an individual bullet

        if lostLOS:  # Returns are based on if lostLOS is TRUE or not, acts as a simple Boolean method
            return True
        else:
            return False



playerLOS = LOSBullet(player, dave)
player.rect.x, player.rect.y = 100, 100
playerspeed = 3

while True:
    surface.fill((255, 255, 255))
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    playerLOS.checkLOS()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()

    if True:  # Movement
        if (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (
                keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(0 - round(playerspeed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, 0 - round(playerspeed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
        elif (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (
                keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(0 - round(playerspeed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, playerspeed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (
                keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(playerspeed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, playerspeed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (
                keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(playerspeed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, 0 - round(playerspeed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
        else:
            if keyboard.is_pressed('a') or keyboard.is_pressed('Left'):  # Cardinal movement
                player.updatePosition(-playerspeed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Left')
            if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):  # Cardinal movement
                player.updatePosition(playerspeed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Right')
            if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):  # Cardinal movement
                player.updatePosition(0, playerspeed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Down')
            if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):  # Cardinal movement
                player.updatePosition(0, -playerspeed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Up')

    surface.blit(testMap.image, testMap.rect)
    surface.blit(dave.image, dave.rect)
    surface.blit(player.image, player.rect)
    pygame.display.update()
    fpsClock.tick(FPS)

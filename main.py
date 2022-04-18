import keyboard as keyboard
import pygame
import random
import sys

from pygame import QUIT

surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
fpsClock = pygame.time.Clock()
FPS = 60
pygame.font.init()

class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()

    def loadMap(self, file):    # takes text file of map
        with open(file) as ins:
            arr = []
            for line in ins:    # creates an array based on the text file
                number_strings = line.split()
                numbers = [n for n in number_strings]
                arr.append(numbers)
        tempsurf = pygame.Surface((len(arr[0]) * 25, len(arr) * 25))    # surface for walls
        tempsurf.fill((255, 255, 255))  # whitespace will be non-collideable
        for i in range(0, len(arr)):    # parses array to create walls on tempsurf
            for j in range(0, len(arr[0])):
                if arr[i][j] == 'x':    # x is used to assign a wall, any other character works for empty space
                    pygame.draw.rect(tempsurf, (0, 0, 0), (j * 25, i * 25, 25, 25))
        tempsurf.set_colorkey((255, 255, 255))  # sets white to transparent, allowing movement in those areas
        self.image = tempsurf   # sets map to the loaded map
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


#Menu class
class Menu:
    output=pygame.Surface((800,800))
    def __init__(self,items,isTitle,itemSize,textColor):
        self.font = pygame.font.SysFont('arial', itemSize)
        self.isTitle=isTitle
        self.itemSize=itemSize
        self.items=items
        displace=0
        #if its the main menu put game logo on top and move down options
        if isTitle:
            self.output.blit(pygame.image.load("titlescreen.png"),(0,0))
            displace=400
        for n in range(len(items)):
            self.output.blit(self.font.render(items[n],0,textColor),(20,displace+n*itemSize))
    def getMenu(self):
        return(self.output)
    def click(self,pos):
        offset=0
        if self.isTitle:
            offset=400
        itemClicked=int((pos[1]-offset)/self.itemSize)
        if itemClicked>=len(self.items):
            itemClicked=None
        return itemClicked





player = Player()
fakePlayer = Player()
# Fake player is an invisible "Player" used to detect collisions
player.rect.x, player.rect.y = 100, 100
playerspeed = 3
menu=Menu(["option1","option2","etc"],False,50,(255,255,255))
while True:

    surface.fill((255, 255, 255))
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            menu.click(pos)
    if True:    # Movement
        if (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):   # Diagonal movement
            player.updatePosition(0 - round(playerspeed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, 0 - round(playerspeed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
        elif (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(0 - round(playerspeed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, playerspeed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(playerspeed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, playerspeed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
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
            if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):    # Cardinal movement
                player.updatePosition(playerspeed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Right')
            if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):  # Cardinal movement
                player.updatePosition(0, playerspeed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Down')
            if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):   # Cardinal movement
                player.updatePosition(0, -playerspeed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Up')

    # if pygame.sprite.collide_mask(player, testMap):
    #     # Takes the fake player and, using the oldX or oldY, checks to see if it can move in the opposite direction
    #     # For example, if it takes oldY, it will check to see if it could move left or right from the original position
    #     # Any instance of which it would collide, returns it to the original X or Y, independently, allowing for diagonal movement
    #     fakePlayer.rect.x, fakePlayer.rect.y = player.rect.x - 5, player.oldY
    #     if pygame.sprite.collide_mask(fakePlayer, testMap):
    #         player.rect.x = player.oldX
    #
    #     fakePlayer.rect.x, fakePlayer.rect.y = player.rect.x + 5, player.oldY
    #     if pygame.sprite.collide_mask(fakePlayer, testMap):
    #         player.rect.x = player.oldX
    #
    #     fakePlayer.rect.x, fakePlayer.rect.y = player.oldX, player.rect.y - 5
    #     if pygame.sprite.collide_mask(fakePlayer, testMap):
    #         player.rect.y = player.oldY
    #
    #     fakePlayer.rect.x, fakePlayer.rect.y = player.oldX, player.rect.y + 5
    #     if pygame.sprite.collide_mask(fakePlayer, testMap):
    #         player.rect.y = player.oldY

    surface.blit(testMap.image, (0, 0))
    surface.blit(player.image, player.rect)
    surface.blit(menu.getMenu(),(0,0))
    pygame.display.update()
    fpsClock.tick(FPS)

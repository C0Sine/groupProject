import keyboard as keyboard
import pygame
import random
import sys
import math

from pygame import QUIT
pygame.init()
surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
surface.convert_alpha()
fpsClock = pygame.time.Clock()
FPS = 60

# maskimage = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
# mask = pygame.mask.from_surface(maskimage)

font = pygame.font.SysFont("Jokerman", 30)
def update_fps():
    fps = str(int(fpsClock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("coral"))
    return fps_text
class Map(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('wallTest.png'), (800, 800))
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

temp = surface.copy()
temp.convert_alpha()


class WallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('shapeTest.png'), (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


weirdWall = WallTest()
weirdWall.rect.x, weirdWall.rect.y = 100, 100

class LightSource():
    def __init__(self, location, direction, width, strength=None):
        # direction and width in degrees

        self.location = location
        self.direction = direction
        self.width = width
        self.strength = strength
        self.points = []

    def changeLocation(self, x, y):
        self.location = [x, y]
        self.calculateLights()

    def changeDirection(self, direction):
        self.direction = direction
        self.calculateLights()

    def calculateLights(self):
        self.points = []

        for angle in range(self.direction, self.direction + self.width + 1):
            point = [-1, -1]  # stores current point
            lastLocation = [-1, -1]  # stores previous point so if point is in a wall
            lastLocation[0] = self.location[0]
            lastLocation[1] = self.location[1]
            len = 1

            run = True

            # Increments len until point is inside a wall and then sets the previous point as the boundary
            while run:

                point = [round(self.location[0] + len * math.cos(math.radians(angle))), round(self.location[1] + len * math.sin(math.radians(angle)))]
                lastLocation[0] = point[0]
                lastLocation[1] = point[1]

                if testMap.mask.get_at(point) != 0:

                    self.points.append(lastLocation)
                    run = False

                else:  # Increment Len
                    len += 10 #change it to 2 and then check the point behind it if it detects a wall

    def drawLights(self):
        # Drawns ligns from start location to the edge points

        self.points.append(self.location)

        temp.fill((0, 0, 0, 255))
        pygame.draw.circle(temp, (255,255,255,0),player.rect.center,player.rect.w*.75)
        pygame.draw.polygon(temp, (255, 255, 255, 0), self.points)

        surface.blit(temp, (0, 0))

    #def makeLayer(self):



class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create a player mask from a given sprite
        self.image = pygame.transform.scale(pygame.image.load('player.png'), (40, 40))
        self.image.set_colorkey((255, 255, 255))
        self.hitbox = pygame.transform.scale(pygame.image.load('hitbox.png'), (30, 30))
        self.mask = pygame.mask.from_surface(self.hitbox)
        self.rect = self.hitbox.get_rect()
        # X and Y position variables for player movement
        self.rect.x, self.rect.y = 100, 100
        self.imageX = self.rect.x - abs((self.rect.width - self.image.get_width()) / 2)     # Changes image location to center hitbox
        self.imageY = self.rect.y - abs((self.rect.height - self.image.get_height()) / 2)   # Changes image location to center hitbox

    def updatePosition(self, xDif, yDif):
        # Method that runs every tick to update the position if velX/velY != 0
        self.rect.x += xDif
        self.rect.y += yDif
        self.imageX = self.rect.x - abs((self.rect.width - self.image.get_width()) / 2)     # Changes image location to center hitbox
        self.imageY = self.rect.y - abs((self.rect.height - self.image.get_height()) / 2)   # Changes image location to center hitbox

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
        self.imageX = self.rect.x - abs((self.rect.width - self.image.get_width()) / 2)     # Changes image location to center hitbox
        self.imageY = self.rect.y - abs((self.rect.height - self.image.get_height()) / 2)   # Changes image location to center hitbox


def blitRotate(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image.set_colorkey((255, 255, 255))
    new_rect = rotated_image.get_rect(center = image.get_rect(topleft = topleft).center)
    surf.blit(rotated_image, new_rect.topleft)


player = Player()

source = LightSource([player.rect.centerx, player.rect.centery], 155, 60)
source.calculateLights()

player_speed = 3
frame = 0
mouse_x, mouse_y = 0, 0
player_angle = 0
target_angle = 0
while True:
    frame += 1
    surface.fill((255, 255, 255))
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

    if True:    # Movement
        if (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):   # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
            source.changeLocation(player.rect.centerx, player.rect.centery)
            print('change')
        elif (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, player_speed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
            source.changeLocation(player.rect.centerx, player.rect.centery)
            print('change')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, player_speed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
            source.changeLocation(player.rect.centerx, player.rect.centery)
            print('change')
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
            source.changeLocation(player.rect.centerx, player.rect.centery)
            print('change')
        else:
            if keyboard.is_pressed('a') or keyboard.is_pressed('Left'):  # Cardinal movement
                player.updatePosition(-player_speed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Left')
                source.changeLocation(player.rect.centerx, player.rect.centery)
                print('change')
            if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):    # Cardinal movement
                player.updatePosition(player_speed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Right')
                source.changeLocation(player.rect.centerx, player.rect.centery)
                print('change')
            if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):  # Cardinal movement
                player.updatePosition(0, player_speed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Down')
                source.changeLocation(player.rect.centerx, player.rect.centery)
                print('change')
            if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):   # Cardinal movement
                player.updatePosition(0, -player_speed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Up')
                source.changeLocation(player.rect.centerx, player.rect.centery)
                print('change')

    source.drawLights()
    surface.blit(testMap.image, (0, 0))
    if mouse_x > player.rect.x + (player.rect.width / 2):
        target_angle = 270 - math.degrees(math.atan((mouse_y - player.rect.y - (player.rect.height / 2)) / (mouse_x - player.rect.x - (player.rect.width / 2))))
    elif mouse_x < player.rect.x + (player.rect.width / 2):
        target_angle = 90 - math.degrees(math.atan((mouse_y - player.rect.y - (player.rect.height / 2)) / (mouse_x - player.rect.x - (player.rect.width / 2))))
    if player_angle < 90 and target_angle > 270:
        player_angle -= (player_angle - target_angle) / 10
    else:
        player_angle -= (player_angle - target_angle) / 10

    if int(player_angle) != int(target_angle):
        source.changeDirection(int(-(source.width / 2) - player_angle - 90))

    surface.blit(update_fps(), (10, 0))
    blitRotate(surface, player.image, (player.imageX, player.imageY), player_angle)
    pygame.display.update()
    fpsClock.tick(FPS)

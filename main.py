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


class Chunk():
    def __init__(self, var, rotation):
        self.var = var
        self.rotation = rotation

    def __str__(self):
        return str(self.var) + ' ' + str(self.rotation)

    def __repr__(self):
        return self.__str__()


class OutdoorMap():
    def __init__(self):
        mapsize = 5
        self.map_array = []
        for i in range(mapsize):
            current_array = []
            for j in range(mapsize):
                current_array.append(Chunk(random.randint(0, 9), random.randint(0, 3)))
            self.map_array.append(current_array.copy())
        key_loc = random.randint(0, mapsize - 1), random.randint(0, mapsize - 1)
        self.map_array[key_loc[0]][key_loc[1]] = Chunk(10, 0)
        print(self.map_array)

map = OutdoorMap()


class IndoorMap(pygame.sprite.Sprite):
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


testMap = IndoorMap()

testMap.loadMap('map1.txt')


class WallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('shapeTest.png'), (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


temp = pygame.Surface((800,800),pygame.SRCALPHA)
temp.convert_alpha()


class Flashlight:
    def __init__(self, powerMultiplier, battery):
        self.powerMultiplier = powerMultiplier
        self.battery = battery
        self.ticks = 0

    def recharge(self):
        self.battery = 400
        self.ticks = 0

    def getPower(self):
        return self.powerMultiplier * self.battery

    def tick(self):
        self.ticks += 1

        if self.ticks % 60 == 0 and self.ticks / 60 > 0:
            self.battery -= 1
            if self.battery <= 0:
                self.battery = 0

            return True
        return False

    def getTicks(self):
        return self.ticks

    def type(self):
        return "flashlight"


class Battery:

    def __init__(self):
        self.power = 400

    def type(self):
        return "battery"


class Blank:

    def __init__(self):
        self.blank = True

    def type(self):
        return "blank"


class Inventory:
    def __init__(self):
        self.items = [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()]
        self.heldObjectPos = -1
        self.heldObject = Blank()

    def appendObject(self, obj):
        for i in range(0, 9):
            if self.items[i].type() == "blank":
                self.items[i] = obj
                break

    def moveObject(self, place):
        if self.items[place].type() == "blank":
            self.items[place] = self.heldObject

        else:
            self.items[self.heldObjectPos] = self.heldObject

        self.heldObjectPos = -1
        self.heldObject = Blank()

    def returnObj(self):
        self.items[self.heldObjectPos] = self.heldObject
        self.heldObject = Blank()
        self.heldObjectPos = -1
        print("YEAH BOIIII")

    def holdingObject(self, place):
        if not self.items[place].type() == "blank":
            self.heldObjectPos = place
            self.heldObject = self.items[place]
            self.items[place] = Blank()
            print(self.items)

    def getHoldPlace(self):
        return self.heldObjectPos

    def getObjectType(self):
        return self.heldObject.type()

    def blitInventory(self):
        x = 50
        y = 50
        for i in range(1, 10):

            pygame.draw.rect(surface, (100, 100, 100), (x, y, 75, 75))
            pygame.draw.rect(surface, (50, 50, 50), (x + 7, y + 7, 61, 61))

            x += 100
            if i % 3 == 0:
                y += 100
                x = 50

        x = 50
        y = 50

        for item in self.items:
            if item.type() == "flashlight":
                pygame.draw.rect(surface, (20, 20, 20), (x + 20, y + 10, 35, 15))
                pygame.draw.rect(surface, (20, 20, 20), (x + 30, y + 25, 15, 40))

                x += 100
                if i % 3 == 0:
                    y += 100
                    x = 50

            if item.type() == "battery":
                pygame.draw.rect(surface, (150, 150, 150), (x + 30, y + 10, 15, 15))
                pygame.draw.rect(surface, (200, 200, 0), (x + 20, y + 20, 35, 45))

                x += 100
                if i % 3 == 0:
                    y += 100
                    x = 50


class LightSource:
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

    def changeStrength(self, new):
        self.strength = new

    def calculateLights(self):
        self.points = []

        angle = self.direction
        while angle < self.direction + self.width + 1:
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

                if testMap.mask.get_at(point) != 0 or len > self.strength:

                    self.points.append(lastLocation)
                    run = False

                else:  # Increment Len
                    if self.strength - len < 10:
                        len += self.strength - len + 1
                    else:
                        len += 10
            angle += 1

    def drawLights(self):
        # Drawns ligns from start location to the edge points

        self.points.append(self.location)

        temp.fill((0, 0, 0, 230))
        pygame.draw.circle(temp, (255, 255, 255, 0), player.rect.center, player.rect.w * 0.75)
        pygame.draw.polygon(temp, (255, 255, 255, 0), self.points)

        surface.blit(temp, (400-player.imageX, 400-player.imageY))

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

source = LightSource([player.rect.centerx, player.rect.centery], 155, 60, 300)
source.calculateLights()

flashlight = Flashlight(1, 400)
battery = Battery()

source.changeStrength(flashlight.getPower())

player_speed = 3
frame = 0
mouse_x, mouse_y = 0, 0
player_angle = 0
target_angle = 0

inv = False
inventory = Inventory()
inventory.appendObject(flashlight)
inventory.appendObject(battery)

while True:
    frame += 1
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and inv:
            itterationX = 50
            itterationY = 50
            for place in range(0, 9):
                if itterationX < mouse_x < itterationX + 75:
                    if itterationY < mouse_y < itterationY + 75:
                        inventory.holdingObject(place)
                        break

                itterationX += 100
                if itterationX == 300:
                    itterationX = 0
                    itterationY += 100

        if event.type == pygame.MOUSEBUTTONUP and inv and inventory.heldObjectPos != -1:
            itterationX = 50
            itterationY = 50
            for place in range(0, 10):
                if itterationX < mouse_x < itterationX + 75:
                    if itterationY < mouse_y < itterationY + 75:
                        if not inventory.items[place] == "blank":
                            inventory.moveObject(place)
                            break
                            print("WHEN DO THE")

                if place == 9:
                    inventory.returnObj()
                    print("RETURURRN")

                itterationX += 100
                if itterationX == 300:
                    itterationX = 0
                    itterationY += 100

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            inv = not inv

    if True:  # Movement
        if (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):   # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
            source.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Left')
            player.updatePosition(0, player_speed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
            source.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, player_speed * 0.707)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Down')
            source.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Right')
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if pygame.sprite.collide_mask(player, testMap):
                player.updateCollisionPosition('Up')
            source.changeLocation(player.rect.centerx, player.rect.centery)
        else:
            if keyboard.is_pressed('a') or keyboard.is_pressed('Left'):  # Cardinal movement
                player.updatePosition(-player_speed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Left')
                source.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):    # Cardinal movement
                player.updatePosition(player_speed, 0)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Right')
                source.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):  # Cardinal movement
                player.updatePosition(0, player_speed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Down')
                source.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):   # Cardinal movement
                player.updatePosition(0, -player_speed)
                if pygame.sprite.collide_mask(player, testMap):
                    player.updateCollisionPosition('Up')
                source.changeLocation(player.rect.centerx, player.rect.centery)

    if player_angle < 0:
        player_angle += 360
        #print("flip")

    if player_angle > 359:
        player_angle -= 360
        #print("FLIP")

    if mouse_x > 400 + (player.rect.width / 2):
        target_angle = 270 - math.degrees(math.atan((mouse_y - 400 - (player.rect.height / 2)) / (mouse_x - 400 - (player.rect.width / 2))))
    elif mouse_x < 400 + (player.rect.width / 2):
        target_angle = 90 - math.degrees(math.atan((mouse_y - 400 - (player.rect.height / 2)) / (mouse_x - 400 - (player.rect.width / 2))))

    #print(f"angle: {player_angle} target: {target_angle}")
    if player_angle < 90 and target_angle > 270:
        player_angle -= (player_angle - target_angle) % 360 / 10
        #print("WORKS")

    elif player_angle > 270 and target_angle < 90:
        player_angle += (target_angle - player_angle) % 360 / 10
        #print("works")

    else:
        player_angle -= (player_angle - target_angle) / 10

    if int(player_angle) != int(target_angle):
        source.changeDirection(int(-(source.width / 2) - player_angle - 90))
    surface.fill((25, 25, 25))
    pygame.draw.rect(surface, (255, 255, 255), (400 - player.imageX, 400 - player.imageY, 800, 800))
    source.drawLights()
    surface.blit(testMap.image, (400 - player.imageX, 400 - player.imageY))
    blitRotate(surface, player.image, (400, 400), player_angle)
    if inv:
        inventory.blitInventory()
    surface.blit(update_fps(), (10, 0))

    if flashlight.tick():
        source.changeStrength(flashlight.getPower())
        source.calculateLights()

    if inventory.getHoldPlace() >= 0:
        print(inventory.getObjectType())
        if inventory.getObjectType() == "flashlight":
            pygame.draw.rect(surface, (20, 20, 20), (mouse_x - 17.5, mouse_y - 7.5, 35, 15))
            pygame.draw.rect(surface, (20, 20, 20), (mouse_x - 7.5, mouse_y + 7.5, 15, 40))

        if inventory.getObjectType() == "battery":
            pygame.draw.rect(surface, (150, 150, 150), (mouse_x - 7.5, mouse_y - 7.5, 15, 15))
            pygame.draw.rect(surface, (200, 200, 0), (mouse_x - 17.5, mouse_y - 22.5, 35, 45))

    pygame.display.update()
    fpsClock.tick(FPS)

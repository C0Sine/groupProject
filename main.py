import keyboard as keyboard
import pygame
import random
import sys
import math
import time

from pygame import QUIT

pygame.init()
surface = pygame.display.set_mode((800, 800), pygame.RESIZABLE)
surface.convert_alpha()
fpsClock = pygame.time.Clock()
FPS = 60
player_chunk = [0, 0]

# maskimage = pygame.transform.scale(pygame.image.load('pixil-frame-0.png'), (800, 800))
# mask = pygame.mask.from_surface(maskimage)

font = pygame.font.SysFont("Arial", 20)


def update_fps():
    fps = str(int(fpsClock.get_fps()))
    fps_text = font.render(fps, 1, pygame.Color("white"))
    return fps_text


def parse_file(file):
    with open(file) as ins:
        arr = []
        for line in ins:  # creates an array based on the text file
            number_strings = line.split()
            numbers = [n for n in number_strings]
            arr.append(numbers)
    # print(arr)
    processedArr = []
    for item in arr:
        items = []
        for string in item:
            for i in range(0, len(string)):
                items.append(string[i])

        if not items == []:
            processedArr.append(items)
        # print(items)

    return processedArr


def player_in_chunk(x, y):
    return [int(x / 400), int(y / 400)]


class Chunk(pygame.sprite.Sprite):
    def __init__(self, loc):
        pygame.sprite.Sprite.__init__(self)
        self.loc = loc
        # print(loc)
        self.loaded = False

        self.area = parse_file('chunks\\chunk(' + str(self.loc[0]) + ', ' + str(self.loc[1]) + ').txt')
        # print(self.area)

        tempsurf = pygame.Surface((400, 400))
        for i in range(0, 16):
            for j in range(0, 16):

                if self.area[i][j] == 'c':
                    pygame.draw.circle(tempsurf, (0, 0, 0), (j * 25 + 12.5, i * 25 + 12.5), 12.5)

                elif self.area[i][j] == 'o':
                    pygame.draw.rect(tempsurf, (255, 255, 255), (j * 25, i * 25, 25, 25))

                elif self.area[i][j] == 'x':
                    surface.blit(pygame.image.load("wall2.png"), (j * 25, i * 25))

        tempsurf.set_colorkey((255, 255, 255))
        self.image = tempsurf
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.loc[0] * 400, self.loc[1] * 400

    def __str__(self):
        return str(self.loc)

    def __repr__(self):
        return self.__str__()


# class
class IndoorMap(pygame.sprite.Sprite):
    def __init__(self):
        mapsize = 7
        self.map_array = []
        self.loaded_chunks = []
        for i in range(mapsize):
            current_array = []
            for j in range(mapsize):
                current_array.append(Chunk((j, i)))
            self.map_array.append(current_array.copy())

    def load_close_chunks(self):
        self.loaded_chunks.clear()
        for i in self.map_array:
            for j in i:
                j.loaded = False
                if player_chunk[0] - 1 <= j.loc[0] <= player_chunk[0] + 1 and player_chunk[1] - 1 <= j.loc[1] <= \
                        player_chunk[1] + 1:
                    j.loaded = True
                    self.loaded_chunks.append(j)


testMap = IndoorMap()


class WallTest(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('shapeTest.png'), (200, 200))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.mask.get_rect()


temp = pygame.Surface((800, 800), pygame.SRCALPHA)
temp.convert_alpha()
light_map_surf = pygame.Surface((2800, 2800))
light_map_surf.fill((255, 255, 255))
for i in testMap.map_array:
    for j in i:
        light_map_surf.blit(j.image, (j.loc[0] * 400, j.loc[1] * 400))
light_map_surf.set_colorkey((255, 255, 255))
light_map_mask = pygame.mask.from_surface(light_map_surf)


class Flashlight:
    def __init__(self, powerMultiplier, battery):
        self.powerMultiplier = powerMultiplier
        self.battery = battery
        self.ticks = 0
        self.type = "flashlight"
        self.image = pygame.transform.scale(pygame.image.load('flashlight.png'), (55, 55))

    def recharge(self):
        self.battery = 401
        self.ticks = 59

    def getPower(self):
        return self.powerMultiplier * self.battery

    def getBattery(self):
        return self.battery

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
        self.type = "battery"
        self.image = pygame.transform.scale(pygame.image.load('battery.png'), (50, 50))

    def type(self):
        return "battery"


class Blank:

    def __init__(self):
        self.blank = True
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'), (1, 1))
        self.type = "blank"

    def type(self):
        return "blank"


class Bear(pygame.sprite.Sprite):
    def __init__(self, Name, centerX, centerY):
        pygame.sprite.Sprite.__init__(self)
        self.name = Name
        self.onStar = False
        if self.name == "firstBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (65, 65))
        elif self.name == "secondBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (65, 65))
        elif self.name == "thirdBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (65, 65))
        elif self.name == "fourthBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (65, 65))
        elif self.name == "fifthBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (65, 65))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = centerX, centerY
        self.hoverY = 0
        self.target = 1
        self.type = "bear"

    def hover(self):
        if self.target == 1:
            if self.hoverY >= self.target:
                self.target = -1
            else:
                self.hoverY += 0.05
        elif self.target == -1:
            if self.hoverY <= self.target:
                self.target = 1
            else:
                self.hoverY -= 0.05


bearList = []
firstBear = Bear("firstBear", 250, 250)
secondBear = Bear("secondBear", 2650, 250)
thirdBear = Bear("thirdBear", 50, 1150)
fourthBear = Bear("fourthBear", 1000, 1000)
fifthBear = Bear("fifthBear", 2620, 2515)
bearList.extend([firstBear, secondBear, thirdBear, fourthBear, fifthBear])

flashlight = Flashlight(1, 200)
battery = Battery()


class Inventory:
    def __init__(self):
        self.items = [Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank(), Blank()]
        self.heldObjectPos = -1
        self.heldObject = Blank()

    def appendObject(self, obj):
        for i in range(0, 9):
            if self.items[i].type == "blank":
                self.items[i] = obj
                break

    def moveObject(self, place):

        print(self.items[place].type)
        if self.items[place].type == "blank":
            self.items[place] = self.heldObject
            print("BOO")

        elif self.items[place].type == "flashlight" and self.heldObject.type == "battery":
            flashlight.recharge()
            print("RECHARGE")

        else:
            self.items[self.heldObjectPos] = self.heldObject
            print("FAKE")

        self.heldObjectPos = -1
        self.heldObject = Blank()

    def returnObj(self):
        self.items[self.heldObjectPos] = self.heldObject
        self.heldObject = Blank()
        self.heldObjectPos = -1
        # print("YEAH BOIIII")

    def holdingObject(self, place):
        if not self.items[place].type == "blank":
            self.heldObjectPos = place
            self.heldObject = self.items[place]
            self.items[place] = Blank()
            # print(self.items)

    def getHoldPlace(self):
        return self.heldObjectPos

    def placeObject(self, place, obj):
        self.items[place] = obj

    def getObjectType(self):
        return self.heldObject.type

    def returnBears(self):
        returnList = []
        for i in self.items:
            if i.type == "bear":
                i.onStar = True
                returnList.append(i)
                i.type = "blank"
        return returnList

    def blitInventory(self):
        x = 50
        y = 50

        for i in range(1, 10):


            surface.blit(pygame.transform.scale(pygame.image.load("item tile.png"), (75, 75)), (x, y))
            #pygame.draw.rect(surface, (100, 100, 100), (x, y, 75, 75))
            #pygame.draw.rect(surface, (50, 50, 50), (x + 7, y + 7, 61, 61))

            if self.items[i - 1].type == "flashlight":
                surface.blit(self.items[i - 1].image, (x + 10, y + 12))
            elif self.items[i - 1].type == "bear":
                surface.blit(self.items[i - 1].image, (x + 5, y + 5))
            elif self.items[i - 1].type == "battery":
                surface.blit(self.items[i - 1].image, (x + 13, y + 10))

            x += 100
            if i % 3 == 0:
                y += 100
                x = 50


class Star(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("fivePointStar.png"), (425, 425))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x, self.rect.y = 1175, 1200
        self.bears = 0


star = Star()


class LightSource(pygame.sprite.Sprite):
    def __init__(self, location, direction, width, strength=None):
        pygame.sprite.Sprite.__init__(self)
        # direction and width in degrees

        self.location = location
        self.direction = direction
        self.width = width
        self.strength = strength
        self.points = []
        self.mask = player.mask
        self.rect = player.rect

    def changeLocation(self, x, y):
        self.location = [x, y]

    def changeDirection(self, direction):
        self.direction = direction

    def changeStrength(self, new):
        self.strength = new

    def calculateLights(self):
        self.points = []

        angle = self.direction

        while angle < self.direction + self.width + 1:
            global player_chunk
            lastLocation = [-1, -1]  # stores previous point so if point is in a wall
            lastLocation[0] = self.location[0]
            lastLocation[1] = self.location[1]
            len = 1

            run = True

            # Increments len until point is inside a wall and then sets the previous point as the boundary

            while run:

                point = [round(self.location[0] + len * math.cos(math.radians(angle))),
                         round(self.location[1] + len * math.sin(math.radians(angle)))]
                lastLocation[0] = point[0]
                lastLocation[1] = point[1]

                if point[0] < 0 or point[0] >= 2800 or point[1] < 0 or point[1] >= 2800 or light_map_mask.get_at(
                        point) != 0 or len > self.strength:

                    self.points.append(lastLocation)
                    run = False

                else:  # Increment Len
                    if self.strength - len < 10:
                        len += self.strength - len + 1
                    else:
                        len += 10
            angle += 1

        for i in self.points:
            i[0] = i[0] - player.rect.centerx + 420
            i[1] = i[1] - player.rect.centery + 420

    def drawLights(self, surfopacity, lightopacity):
        self.calculateLights()
        # Drawns ligns from start location to the edge points

        self.points.append((420, 420))

        global temp

        temp.fill((0, 0, 0, surfopacity))
        pygame.draw.circle(temp, (255, 255, 150, lightopacity), (420, 420), player.rect.w * .75)
        pygame.draw.polygon(temp, (255, 255, 150, lightopacity), self.points)

        self.mask = pygame.mask.from_surface(temp)
        self.rect = temp.get_rect()

        return temp

    # def makeLayer(self):


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # Create a player mask from a given sprite
        self.image = pygame.transform.scale(pygame.image.load('player.png'), (40, 40))
        self.image.set_colorkey((255, 255, 255))
        self.hitbox = pygame.transform.scale(pygame.image.load('hitbox.png'), (30, 30))
        self.mask = pygame.mask.from_surface(self.hitbox)
        self.rect = self.hitbox.get_rect()
        self.health = 5
        self.hitTime, self.noHitTime = 0, 0
        # X and Y position variables for player movement
        self.rect.x, self.rect.y = 100, 100
        self.imageX = self.rect.x - abs(
            (self.rect.width - self.image.get_width()) / 2)  # Changes image location to center hitbox
        self.imageY = self.rect.y - abs(
            (self.rect.height - self.image.get_height()) / 2)  # Changes image location to center hitbox

    def updatePosition(self, xDif, yDif):
        # Method that runs every tick to update the position if velX/velY != 0
        self.rect.x += xDif
        self.rect.y += yDif
        self.imageX = self.rect.x - abs(
            (self.rect.width - self.image.get_width()) / 2)  # Changes image location to center hitbox
        self.imageY = self.rect.y - abs(
            (self.rect.height - self.image.get_height()) / 2)  # Changes image location to center hitbox

    def updateCollisionPosition(self, direction, collider):
        while pygame.sprite.collide_mask(self, collider):
            if direction.__contains__('Left'):
                self.rect.x += self.mask.overlap_mask(collider.mask, (0, 0)).get_rect().width - self.rect.width + 1
            if direction.__contains__('Right'):
                self.rect.x -= self.mask.overlap_mask(collider.mask, (0, 0)).get_rect().width - self.rect.width + 1
            if direction.__contains__('Down'):
                self.rect.y -= self.mask.overlap_mask(collider.mask, (0, 0)).get_rect().height - self.rect.width + 1
            if direction.__contains__('Up'):
                self.rect.y += self.mask.overlap_mask(collider.mask, (0, 0)).get_rect().height - self.rect.width + 1
        self.imageX = self.rect.x - abs(
            (self.rect.width - self.image.get_width()) / 2)  # Changes image location to center hitbox
        self.imageY = self.rect.y - abs(
            (self.rect.height - self.image.get_height()) / 2)  # Changes image location to center hitbox

    def blitStatus(self):
        surface.blit(pygame.image.load("power bar.png"), (555, 40))
        #pygame.draw.rect(surface, (100, 100, 100), (575, 60, 210, 20))
        pygame.draw.rect(surface, (0, 255, 0), (580, 65, flashlight.getBattery() / 2, 10))
        heart = pygame.transform.scale(pygame.image.load("playerHeart.png"), (40, 40))
        for i in range(self.health):
            surface.blit(heart, (575 + (i * 40), 15))

    def checkCollisions(self):
        for i in bearList:  # Pick up bear
            if pygame.sprite.collide_mask(self, i) and not i.onStar:
                inventory.appendObject(i)
                i.rect.x = -10000
                # print("added item")
        if pygame.sprite.collide_mask(self, star):  # Player touches Star, check for bears, place in order
            heldBears = inventory.returnBears()
            counter = 0
            if len(heldBears) != 0:
                for i in range(len(heldBears)):
                    print(star.bears)
                    if star.bears == 0:
                        heldBears[i].rect.centerx, heldBears[i].rect.centery = star.rect.x + 225, star.rect.y + 25
                        star.bears += 1
                    elif star.bears == 1:
                        heldBears[i].rect.centerx, heldBears[i].rect.centery = star.rect.x + 355, star.rect.y + 125
                        star.bears += 1
                    elif star.bears == 2:
                        heldBears[i].rect.centerx, heldBears[i].rect.centery = star.rect.x + 290, star.rect.y + 325
                        star.bears += 1
                    elif star.bears == 3:
                        heldBears[i].rect.centerx, heldBears[i].rect.centery = star.rect.x + 110, star.rect.y + 310
                        star.bears += 1
                    elif star.bears == 4:
                        heldBears[i].rect.centerx, heldBears[i].rect.centery = star.rect.x + 70, star.rect.y + 160
                        star.bears += 1
        self.noHitTime = time.time()
        for i in enemList:
            if pygame.sprite.collide_mask(self, i) and (int(self.noHitTime - self.hitTime) > 3):
                self.health -= 1
                self.hitTime = time.time()


player = Player()


def blitRotate(surf, image, topleft, angle):
    rotated_image = pygame.transform.rotate(image, angle)
    rotated_image.set_colorkey((255, 255, 255))
    new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
    surf.blit(rotated_image, new_rect.topleft)

    # def createLOSLine(self, Target):
    #     LOSLine = pygame.draw.line(surface, (0, 0, 0),
    #                                (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
    #                                (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
    #     # pygame.draw.line(surface, (0, 0, 0), (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2), (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
    #     if LOSLine.colliderect(Target):
    #         LOSLine = pygame.draw.line(surface, (0, 255, 0),
    #                                    (self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2),
    #                                    (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))
    #     # else: LOSLine = pygame.draw.line(surface, (0, 255, 0), (self.rect.x + self.rect.width / 2, self.rect.y +
    #     # self.rect.height / 2), (Target.rect.x + Target.rect.width / 2, Target.rect.y + Target.rect.height / 2))


class LOSBullet(pygame.sprite.Sprite):
    def __init__(self, Origin):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'), (10, 10))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.origin = Origin
        self.rect.center = self.origin.rect.center

    def checkLOS(self):
        # ONLY CHANGE NEEDED: MAKE IT SO LOS NOT LOST ON LEFT WALL/CENTER BETTER ON PLAYER :)
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'),
                                            (10, 10))  # Ensures the default image is a black 10x10 square
        self.rect.center = self.origin.rect.center
        # print("origin center = " + str(self.origin.rect.center))
        moveX = player.rect.centerx - self.rect.centerx  # Creates the X component of the "slope"
        moveY = player.rect.centery - self.rect.centery  # Creates the Y component of the "slope"
        # print("moveX = " + str(moveX))
        # print("moveY = " + str(moveY))
        # print("Target Center = " + str(player.rect.center))
        lostLOS = False  # A variable that will read TRUE if line of sight is ever broken

        for i in range(25):  # Create and check 25 points
            self.rect.centerx += moveX / 25  # Moves the bullet 1 29th of the total center-to-center distance(X)
            self.rect.centery += moveY / 25  # Moves the bullet 1 29th of the total center-to-center distance(Y)

            for i in testMap.loaded_chunks:
                if pygame.sprite.collide_mask(self,
                                              i):  # If even ONE 'bullet' collides with our map, lostLOS becomes TRUE
                    lostLOS = True
                    self.image = pygame.transform.scale(pygame.image.load('LOSBroken.png'), (
                        10, 10))  # Make it so the colliding bullets and everything past appear red

            # surface.blit(self.image, ((400 - player.imageX) + self.rect.x, (400 - player.imageY) + self.rect.y))  # Blit an individual bullet, not needed unless testing

            if pygame.sprite.collide_mask(self, player) and not lostLOS:
                self.image = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (10, 10))

        # print(lostLOS)
        return [lostLOS, player.rect.centerx,
                player.rect.centery]  # Returns True/False based on if LOS was broken and a last seen location


class Enemy(pygame.sprite.Sprite):
    def __init__(self, Type, Name):
        pygame.sprite.Sprite.__init__(self)
        self.lastSeenX, self.lastSeenY = 0, 0
        self.noMove = False
        self.name = Name
        self.xcol = False
        self.ycol = False
        self.tempseenX, self.tempseenY = 0, 0
        self.angle, self.targetAngle = 0, 0
        self.type = Type
        self.time, self.startTime = 0, 0
        self.inLight = False
        self.loaded = False
        if self.type == "zombie":
            self.image = pygame.transform.scale(pygame.image.load('zombrotest.png'), (60, 60))
            self.hitbox = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (40, 40))
            self.mask = pygame.mask.from_surface(self.hitbox)
            self.rect = self.image.get_rect()
        elif self.type == "goober":
            self.image = pygame.transform.scale(pygame.image.load('goober.png'), (40, 40))
            self.hitbox = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (40, 40))
            self.mask = pygame.mask.from_surface(self.hitbox)
            self.rect = self.image.get_rect()
        self.LOS = LOSBullet(self)

    def goToLastSeen(self, LOSCoords, Target):  # Requires a True/False input from checkLOS AND a target
        moveX, moveY = 0, 0
        # print("daveRectX = " + str(self.rect.x) + ", daveRectY = " + str(self.rect.y))
        if not LOSCoords[0]:
            # print("Moving to LOS")
            self.noMove = False
            moveX = Target.rect.centerx - self.rect.centerx  # Creates an X difference to move along
            moveY = Target.rect.centery - self.rect.centery  # Creates a Y difference to move along
            self.lastSeenX = LOSCoords[1]  # Store last seen location
            self.lastSeenY = LOSCoords[2]
            # pygame.draw.line(surface, (0, 0, 0), (Target.rect.centerx, Target.rect.centery), (self.rect.centerx, self.rect.centery))
        if LOSCoords[0] and not self.noMove:
            # print("Moving to LAST SEEN")
            # pygame.draw.circle(surface, (0, 255, 0), (self.lastSeenX, self.lastSeenY), 4)
            moveX = self.lastSeenX - self.rect.centerx  # If there is NO LOS, move to last seen X and Y
            moveY = self.lastSeenY - self.rect.centery
            # pygame.draw.line(surface, (0, 0, 0), (self.lastSeenX, self.lastSeenY), (self.rect.centerx, self.rect.centery))
        elif LOSCoords[0] and self.noMove:  # If movement is blocked, move to a direction cardinal to the last Seen
            # print("Moving to Temp")
            # pygame.draw.circle(surface, (255, 0, 0), (self.tempseenX, self.tempseenY), 4)
            moveX = self.tempseenX - self.rect.centerx
            moveY = self.tempseenY - self.rect.centery
            if moveX == 0 and moveY == 0:
                self.noMove = False
                moveX = self.lastSeenX - self.rect.centerx
                moveY = self.lastSeenY - self.rect.centery

        delx, dely = 0, 0
        if moveX == 0 and moveY != 0:
            delx = 0
            if moveY > 0:
                dely = 1
            else:
                dely = -1
            if 0 < moveY < 1:
                dely = moveY
        if moveY == 0 and moveX != 0:
            delx, dely = 1, 0
            if moveX > 0:
                delx = 1
            else:
                delx = -1
            if 0 < moveX < 1:
                delx = moveX
        if moveX != 0 and moveY != 0:
            if moveX < 0:
                delx = (1 / math.sqrt(1 + math.pow(moveY / moveX, 2))) * -1
            else:
                delx = (1 / math.sqrt(1 + math.pow(moveY / moveX, 2)))
            dely = delx * (moveY / moveX)
        if pygame.sprite.collide_mask(self, Target):  # Don't move if Enemy collides with Target
            delx, dely = 0, 0
        if moveX == 0 and moveY == 0:
            delx, dely = 0, 0

        # print(math.sqrt(math.pow(delx, 2) + math.pow(dely, 2)))
        self.xcol, self.ycol = False, False
        self.rect.centerx += round(delx)
        for i in testMap.loaded_chunks:
            if pygame.sprite.collide_mask(self, i):  # Move in x direction, move back if col
                self.xcol = True
                self.rect.centerx -= round(delx)
                # print("X collision moved back x")
        self.rect.centery += round(dely)
        # if self.xcol:  # Move in y directoin
        #     self.rect.centery += 2  # Move 2 if no horizontal movement
        # else:
        #     self.rect.centery += round(dely)  # Move x and y
        #     print("ADD DELY")
        for i in testMap.loaded_chunks:
            if pygame.sprite.collide_mask(self, i):  # Check collision for y
                self.ycol = True
                # print("Y collision moved back y")
                if self.xcol:
                    self.rect.centery -= 2  # Move back 2 if moved forward 2
                    # print("SUB  NEG 2")
                else:
                    self.rect.centery -= round(dely)  # Move back dely if moved dely
                    # print("SUB DELY")
        # if not self.ycol and not self.xcol:
        #     #print("Moved X AND Y")
        # if self.xcol and not self.ycol:
        #     #print("Moved Y but not X")

    def lightTimer(self):
        if not pygame.sprite.collide_mask(self, vision):
            self.timer = time.time()
            # print("subtraction: " + str(self.timer - self.startTime))
            if int(self.timer - self.startTime) == 2:
                self.rect.x = -10000
                self.inLight = False


dave = Enemy("zombie", "dave")
dave.rect.x, dave.rect.y = 250, 250
dave1 = Enemy("zombie", "dave1")
dave1.rect.x, dave1.rect.y = 2620, 2650
dave2 = Enemy("zombie", "dave2")
dave2.rect.x, dave2.rect.y = 2650, 250
enemList = [dave, dave1, dave2]


# Menu class
class Menu:
    output = pygame.Surface((800, 800))

    def __init__(self, items, isTitle, itemSize, textColor):
        self.font = pygame.font.SysFont('arial', itemSize)
        self.isTitle = isTitle
        self.itemSize = itemSize
        self.items = items
        self.color = textColor
        self.create()

    def create(self):
        self.output.fill((0, 0, 0))
        displace = (self.itemSize / 2)
        # if its the main menu put game logo on top and move down options
        if self.isTitle:
            self.output.blit(pygame.transform.scale(pygame.image.load("titlescreen.png"), (800, 400)), (0, 0))
            displace = 400 + (self.itemSize / 2)
        for n in range(len(self.items)):
            text = self.font.render(self.items[n], 0, self.color)
            text_rect = text.get_rect(center=(400, (n * self.itemSize) + displace))
            self.output.blit(text, text_rect)

    def getMenu(self):
        return (self.output)

    def update(self, items, newSize=None):
        self.items = items
        if newSize != None:
            self.itemSize = newSize
        self.create()

    def click(self, pos):
        # finds and returns what item is clicked
        offset = 0
        if self.isTitle:
            offset = 400
        itemClicked = int((pos[1] - offset) / self.itemSize)
        if 0 > itemClicked >= len(self.items) or 200 > pos[0] or 600 < pos[0]:
            itemClicked = None
        return itemClicked


class Item(pygame.sprite.Sprite):
    def __init__(self, Name, centerX, centerY):
        pygame.sprite.Sprite.__init__(self)
        self.name = Name
        if self.name == "firstBear":
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (80, 80))
        else:
            self.name = "flashlight"
            self.image = pygame.transform.scale(pygame.image.load(self.name + ".png"), (80, 80))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx, self.rect.centery = centerX, centerY
        self.hoverY = 0
        self.target = 1

    def hover(self):
        if self.target == 1:
            if self.hoverY >= self.target:
                self.target = -1
            else:
                self.hoverY += 0.05
        elif self.target == -1:
            if self.hoverY <= self.target:
                self.target = 1
            else:
                self.hoverY -= 0.05


itemList = []
firstAnimal = Item("firstBear", 110, 110)

# Fake player is an invisible "Player" used to detect collisions
player.rect.x, player.rect.y = 100, 100
playerspeed = 3

testMap.load_close_chunks()
vision = LightSource([player.rect.centerx, player.rect.centery], 155, 60, 300)
vision.calculateLights()

flashlight = Flashlight(1, 300)
battery = Battery()

vision.changeStrength(flashlight.getPower())
vision.changeStrength(flashlight.getPower())

player_speed = 3
frame = 0
mouse_x, mouse_y = 0, 0
player_angle = 0
target_angle = 0

inv = False
inventory = Inventory()
inventory.placeObject(8, flashlight)
inventory.placeObject(7, battery)

# game pause variable
# game pause variable
gaming = False
# game pause variable


menu = Menu(["Play", "Close", "Credits"], True, 50, (255, 255, 255))
credits = None
currentMenu = menu


def collide_chunk():
    for i in testMap.loaded_chunks:
        if pygame.sprite.collide_mask(player, i):
            return i
    return None


inv = False
inventory = Inventory()
inventory.placeObject(8, flashlight)
inventory.placeObject(7, battery)

while True:
    frame += 1
    player.oldX, player.oldY = player.rect[0], player.rect[1]

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            print('l8r sk8r')
            sys.exit()
        if event.type == pygame.MOUSEBUTTONUP and not gaming:  # menu click handling
            pos = pygame.mouse.get_pos()
            item = currentMenu.click(pos)
            if item == 0:
                if currentMenu == menu:
                    gaming = True
                    currentMenu = None
            elif item == 1:
                if currentMenu == menu:
                    pygame.quit()
                    print('l8r sk8r')
                    sys.exit()
                elif player.health == 0 and currentMenu == respawnMenu:
                    gaming = True
                    player.health = 5
                    player.rect.x, player.rect.y = 100, 100
                    player.updatePosition(1, 1)
                    player_angle = 0
                    player.update()
                    star.bears = 0
                    bearList.clear()
                    firstBear = Bear("firstBear", 250, 250)
                    secondBear = Bear("secondBear", 2650, 250)
                    thirdBear = Bear("thirdBear", 50, 1150)
                    fourthBear = Bear("fourthBear", 1000, 1000)
                    fifthBear = Bear("fifthBear", 2620, 2515)
                    bearList.extend([firstBear, secondBear, thirdBear, fourthBear, fifthBear])
                    enemList.clear()
                    dave = Enemy("zombie", "dave")
                    dave.rect.x, dave.rect.y = 250, 250
                    enemList = [dave]
                    if collide_chunk() is not None:
                        player.updateCollisionPosition('Up', collide_chunk())
                    vision.changeLocation(player.rect.centerx, player.rect.centery)
                elif currentMenu == victoryMenu:
                    pygame.quit()
                    print('l8r sk8r')
                    sys.exit()

            elif item == 2:
                if currentMenu == menu:
                    credits = Menu(
                        ["Sam: Came in Clutch", "Brandon: Smart Chunk Stuff", "Jude: Said Dumb Things and Drove People Crazy",
                         "Rowen: Git Master", "Back"], False, 30, (255, 255, 255))
                    currentMenu = credits
                elif currentMenu == respawnMenu:
                    pygame.quit()
                    print('l8r sk8r')
                    sys.exit()
            elif item == 4:
                if currentMenu == credits:
                    currentMenu = menu
                    currentMenu.create()
                    # print("aaa")
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN and inv:
            # print("BOOMSHAKALAKA")
            itterationX = 50
            itterationY = 50
            for place in range(0, 9):
                if itterationX < mouse_x < itterationX + 75:
                    if itterationY < mouse_y < itterationY + 75:
                        # print("DOO DOO")
                        inventory.holdingObject(place)
                        break

                itterationX += 100
                if itterationX >= 350:
                    itterationX = 50
                    itterationY += 100
                    # print("RESET")

        if event.type == pygame.MOUSEBUTTONUP and inv and inventory.heldObjectPos != -1:
            itterationX = 50
            itterationY = 50
            # print("x: "+str(mouse_x)+", y: "+str(mouse_y))
            for place in range(0, 10):
                # print("ix: "+str(itterationX)+", iy: "+str(itterationY))
                if itterationX < mouse_x < itterationX + 75:
                    if itterationY < mouse_y < itterationY + 75:
                        inventory.moveObject(place)
                        break

                itterationX += 100
                if itterationX >= 350:
                    itterationX = 50
                    # print("RESET")
                    itterationY += 100

                if place == 9:
                    inventory.returnObj()
                    # print("RETURURRN")

        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            inv = not inv

    if gaming:  # Movement
        collider = None
        player_chunk = player_in_chunk(player.rect.centerx, player.rect.centery)
        testMap.load_close_chunks()

        if (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (
                keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Left', collide_chunk())
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if collide_chunk() is not None:
                player.updateCollisionPosition('Up', collide_chunk())
            vision.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('a') or keyboard.is_pressed('Left')) and (
                keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(0 - round(player_speed * 0.707), 0)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Left', collide_chunk())
            player.updatePosition(0, player_speed * 0.707)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Down', collide_chunk())
            vision.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (
                keyboard.is_pressed('s') or keyboard.is_pressed('Down')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Right', collide_chunk())
            player.updatePosition(0, player_speed * 0.707)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Down', collide_chunk())
            vision.changeLocation(player.rect.centerx, player.rect.centery)
        elif (keyboard.is_pressed('d') or keyboard.is_pressed('Right')) and (
                keyboard.is_pressed('w') or keyboard.is_pressed('Up')):  # Diagonal movement
            player.updatePosition(player_speed * 0.707, 0)
            if collide_chunk() is not None:
                player.updateCollisionPosition('Right', collide_chunk())
            player.updatePosition(0, 0 - round(player_speed * 0.707))
            if collide_chunk() is not None:
                player.updateCollisionPosition('Up', collide_chunk())
            vision.changeLocation(player.rect.centerx, player.rect.centery)
        else:
            if keyboard.is_pressed('a') or keyboard.is_pressed('Left'):  # Cardinal movement
                player.updatePosition(-player_speed, 0)
                if collide_chunk() is not None:
                    player.updateCollisionPosition('Left', collide_chunk())
                vision.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('d') or keyboard.is_pressed('Right'):  # Cardinal movement
                player.updatePosition(player_speed, 0)
                if collide_chunk() is not None:
                    player.updateCollisionPosition('Right', collide_chunk())
                vision.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('s') or keyboard.is_pressed('Down'):  # Cardinal movement
                player.updatePosition(0, player_speed)
                if collide_chunk() is not None:
                    player.updateCollisionPosition('Down', collide_chunk())
                vision.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('w') or keyboard.is_pressed('Up'):  # Cardinal movement
                player.updatePosition(0, -player_speed)
                if collide_chunk() is not None:
                    player.updateCollisionPosition('Up', collide_chunk())
                vision.changeLocation(player.rect.centerx, player.rect.centery)
            if keyboard.is_pressed('r'):
                print(player.rect)

    if player_angle < 0:
        player_angle += 360
        # print("flip")

    if player_angle > 359:
        player_angle -= 360
        # print("FLIP")

    if mouse_x > 400 + (player.rect.width / 2):
        target_angle = 270 - math.degrees(
            math.atan((mouse_y - 400 - (player.rect.height / 2)) / (mouse_x - 400 - (player.rect.width / 2))))
    elif mouse_x < 400 + (player.rect.width / 2):
        target_angle = 90 - math.degrees(
            math.atan((mouse_y - 400 - (player.rect.height / 2)) / (mouse_x - 400 - (player.rect.width / 2))))

    if player_angle < 90 and target_angle > 270:
        player_angle -= (player_angle - target_angle) % 360 / 10
        # print("WORKS")
    elif player_angle > 270 and target_angle < 90:
        player_angle += (target_angle - player_angle) % 360 / 10
        # print("works")
    else:
        player_angle -= (player_angle - target_angle) / 10

    for i in enemList:
        if i.loaded:
            if i.angle < 0:
                i.angle += 360

            if i.angle > 359:
                i.angle -= 360

            if player.rect.centerx > i.rect.centerx:
                i.targetAngle = 270 - math.degrees(
                    math.atan((player.rect.centery - i.rect.centery) / (player.rect.centerx - i.rect.centerx)))
            elif player.rect.centerx < dave.rect.centerx:
                i.targetAngle = 90 - math.degrees(
                    math.atan((player.rect.centery - i.rect.centery) / (player.rect.centerx - i.rect.centerx)))

            if i.angle < 90 and i.targetAngle > 270:
                i.angle -= (i.angle - i.targetAngle) % 360 / 10
            elif i.angle > 270 and i.targetAngle < 90:
                i.angle += (i.angle - i.targetAngle) % 360 / 10
            else:
                i.angle -= (i.angle - i.targetAngle) / 10

    if int(player_angle) != int(target_angle):
        vision.changeDirection(int(-(vision.width / 2) - player_angle - 90))

    surface.fill((25, 25, 25))
    if gaming:
        tempsurf = pygame.surface.Surface((800, 800))
        tempsurf.blit(star.image, (400 - player.imageX + star.rect.x, 400 - player.imageY + star.rect.y))
        for i in enemList:
            for j in testMap.loaded_chunks:
                if player_in_chunk(i.rect.x, i.rect.y) == list(j.loc):
                    i.loaded = True
            if i.loaded:
                i.goToLastSeen(i.LOS.checkLOS(), player)
                blitRotate(tempsurf, i.image, ((400 - player.imageX) + i.rect.x, 400 - player.imageY + i.rect.y),
                           i.angle + 90)
            #print(i.name + str(i.loaded))
        for i in bearList:
            if not i.onStar:
                i.hover()
            tempsurf.blit(i.image, (400 - player.imageX + i.rect.x, 400 - player.imageY + i.rect.y + (i.hoverY * 5)))
        tempsurf.blit(vision.drawLights(255, 0), (0, 0))
        tempsurf.set_colorkey((0, 0, 0))
        pygame.draw.rect(surface, (255, 255, 255), (0, 0, 800, 800))
        surface.blit(vision.drawLights(230, 100), (0, 0))
        surface.blit(tempsurf, (0, 0))
        for i in testMap.loaded_chunks:
            surface.blit(i.image, (400 - player.imageX + i.rect.x, 400 - player.imageY + i.rect.y))
        # print(player_in_chunk(dave.rect.x, dave.rect.y))
        # if not pygame.sprite.collide_mask(dave, vision):
        #     surface.blit(dave.image, ((400 - player.imageX) + dave.rect.x, 400 - player.imageY + dave.rect.y))
        blitRotate(surface, player.image, (400, 400), player_angle)
        surface.blit(update_fps(), (10, 0))
        player.checkCollisions()
        player.blitStatus()
        if player.health == 0:
            gaming = False
            respawnMenu = Menu(["RESPAWN", "Yes", "No"], False, 50, (255, 255, 255))
            currentMenu = respawnMenu

            flashlight = Flashlight(1, 300)
            battery = Battery()
            vision.changeStrength(flashlight.getPower())
            inventory = Inventory()
            inventory.placeObject(8, flashlight)
            inventory.placeObject(7, battery)
        if inv:
            inventory.blitInventory()
        if star.bears == 5:
            gaming = False
            victoryMenu = Menu(["Congratulations!", "Close"], False, 100, (255, 255, 255))
            currentMenu = victoryMenu
    else:
        surface.blit(currentMenu.getMenu(), (0, 0))
    surface.blit(update_fps(), (10, 0))

    if flashlight.tick():
        vision.changeStrength(flashlight.getPower())
        vision.calculateLights()

    if inventory.getHoldPlace() >= 0:
        surface.blit(inventory.heldObject.image, (mouse_x - 25, mouse_y - 25))

    pygame.display.update()
    fpsClock.tick(FPS)

import keyboard as keyboard
import pygame
import random
import sys
import math

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

                point = [round(self.location[0] + len * math.cos(math.radians(angle))),
                         round(self.location[1] + len * math.sin(math.radians(angle)))]
                lastLocation[0] = point[0]
                lastLocation[1] = point[1]

                if testMap.mask.get_at(point) != 0:

                    self.points.append(lastLocation)
                    run = False

                else:  # Increment Len
                    len += 1

    def drawLights(self):
        # Drawns ligns from start location to the edge points
        pygame.draw.line(surface, (255, 0, 0), (self.location[0], self.location[1]),
                         (self.points[0][0], self.points[0][1]))
        pygame.draw.line(surface, (255, 0, 0), (self.location[0], self.location[1]),
                         (self.points[len(self.points) - 1][0], self.points[len(self.points) - 1][1]))

        for index in range(0, len(self.points) - 1):  # goes through points and draws lines between them
            pygame.draw.line(surface, (255, 0, 0), (self.points[index][0], self.points[index][1]),
                             (self.points[index + 1][0], self.points[index + 1][1]))

    # def makeLayer(self):


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
        self.image = pygame.transform.scale(pygame.image.load('fakeEnemy.png'), (40, 40))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.lastSeenX, self.lastSeenY = 0, 0
        self.noMove = False
        self.tempseenX, self.tempseenY = 0, 0

    def goToLastSeen(self, LOSCoords, Target):  # Requires a True/False input from checkLOS AND a target
        moveX, moveY = 0, 0
        if not LOSCoords[0]:
            print("Moving to LOS")
            self.noMove = False
            moveX = Target.rect.centerx - self.rect.centerx  # Creates an X difference to move along
            moveY = Target.rect.centery - self.rect.centery  # Creates a Y difference to move along
            self.lastSeenX = LOSCoords[1]  # Store last seen location
            self.lastSeenY = LOSCoords[2]
        if LOSCoords[0] and not self.noMove:
            print("Moving to LAST SEEN")
            pygame.draw.circle(surface, (0, 255, 0), (self.lastSeenX, self.lastSeenY), 4)
            moveX = self.lastSeenX - self.rect.centerx  # If there is NO LOS, move to last seen X and Y
            moveY = self.lastSeenY - self.rect.centery
        elif LOSCoords[0] and self.noMove:  # If movement is blocked, move to a direction cardinal to the last Seen
            print("Moving to Temp")
            pygame.draw.circle(surface, (255, 0, 0), (self.tempseenX, self.tempseenY), 4)
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
                dely = 2
            else:
                dely = -2
            if 0 < moveY < 2:
                dely = moveY
        if moveY == 0 and moveX != 0:
            delx, dely = 2, 0
            if moveX > 0:
                delx = 2
            else:
                delx = -2
            if 0 < moveX < 2:
                delx = moveX
        if moveX != 0 and moveY != 0:
            if moveX < 0:
                delx = (2 / math.sqrt(1 + math.pow(moveY / moveX, 2))) * -1
            else:
                delx = (2 / math.sqrt(1 + math.pow(moveY / moveX, 2)))
            dely = delx * (moveY / moveX)
        if pygame.sprite.collide_mask(self, Target):  # Don't move if Enemy collides with Target
            delx, dely = 0, 0
        if moveX == 0 and moveY == 0:
            delx, dely = 0, 0

        #print(math.sqrt(math.pow(delx, 2) + math.pow(dely, 2)))
        self.rect.centerx += delx
        self.rect.centery += dely

        if pygame.sprite.collide_mask(self, testMap):
            if LOSCoords[0]:
                self.noMove = True
            colX, colY = 0, 0
            while pygame.sprite.collide_mask(self, testMap):
                if delx >= 0:
                    self.rect.centerx -= 1
                    colX -= 1
                elif delx < 0:
                    self.rect.centerx += 1
                    colX += 1
                if dely >= 0:
                    self.rect.centery -= 1
                    colY -= 1
                elif dely < 0:
                    self.rect.centery += 1
                    colY += 1
            if colX >= colY:
                if not self.noMove:
                    print("moving Y by " + str(dely))
                    self.rect.centery += 2
                self.tempseenY = self.lastSeenY
                self.tempseenX = self.rect.centerx
            elif colX < colY:
                if not self.noMove:
                    print("moving X by " + str(delx))
                    self.rect.centerx += 2
                self.tempseenY = self.rect.centery
                self.tempseenX = self.lastSeenX


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
        # ONLY CHANGE NEEDED: MAKE IT SO LOS NOT LOST ON LEFT WALL/CENTER BETTER ON PLAYER :)
        self.image = pygame.transform.scale(pygame.image.load('LOSTest.png'),
                                            (10, 10))  # Ensures the default image is a black 10x10 square
        self.rect.center = self.origin.rect.center
        moveX = self.target.rect.centerx - self.rect.centerx  # Creates the X component of the "slope"
        moveY = self.target.rect.centery - self.rect.centery  # Creates the Y component of the "slope"
        lostLOS = False  # A variable that will read TRUE if line of sight is ever broken

        for i in range(25):  # Create and check 25 points
            self.rect.centerx += moveX / 25  # Moves the bullet 1 29th of the total center-to-center distance(X)
            self.rect.centery += moveY / 25  # Moves the bullet 1 29th of the total center-to-center distance(Y)

            if pygame.sprite.collide_mask(self,
                                          testMap):  # If even ONE 'bullet' collides with our map, lostLOS becomes TRUE
                lostLOS = True
                self.image = pygame.transform.scale(pygame.image.load('LOSBroken.png'), (
                10, 10))  # Make it so the colliding bullets and everything past appear red

            surface.blit(self.image, self.rect)  # Blit an individual bullet, not needed unless testing

            if pygame.sprite.collide_mask(self, self.target) and not lostLOS:
                self.image = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (10, 10))

        return [lostLOS, self.target.rect.centerx,
                self.target.rect.centery]  # Returns True/False based on if LOS was broken and a last seen location


daveLOS = LOSBullet(dave, player)
source = LightSource([player.rect.centerx, player.rect.centery], 155, 30)
source.calculateLights()

# Fake player is an invisible "Player" used to detect collisions
player.rect.x, player.rect.y = 100, 100
playerspeed = 3

while True:
    surface.fill((255, 255, 255))
    player.oldX, player.oldY = player.rect[0], player.rect[1]
    source.changeLocation(player.rect.centerx, player.rect.centery)
    source.drawLights()
    dave.goToLastSeen(daveLOS.checkLOS(), player)

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
    source.drawLights()
    pygame.display.update()
    fpsClock.tick(FPS)

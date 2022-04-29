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



testMap = IndoorMap()

testMap.loadMap('map1.txt')

temp = pygame.Surface((800,800),pygame.SRCALPHA)
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
                    len += 10 #change it to 2 and then check the point behind it if it detects a wall
            angle += 1

    def drawLights(self):
        # Drawns ligns from start location to the edge points

        self.points.append(self.location)

        temp.fill((0, 0, 0, 230))
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
        self.hitbox = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (35, 35))
        self.mask = pygame.mask.from_surface(self.hitbox)
        self.rect = self.image.get_rect()
        self.lastSeenX, self.lastSeenY = 0, 0
        self.noMove = False
        self.xcol = False
        self.ycol = False
        self.tempseenX, self.tempseenY = 0, 0

    def goToLastSeen(self, LOSCoords, Target):  # Requires a True/False input from checkLOS AND a target
        moveX, moveY = 0, 0
        if not LOSCoords[0]:
            #print("Moving to LOS")
            self.noMove = False
            moveX = Target.rect.centerx - self.rect.centerx  # Creates an X difference to move along
            moveY = Target.rect.centery - self.rect.centery  # Creates a Y difference to move along
            self.lastSeenX = LOSCoords[1]  # Store last seen location
            self.lastSeenY = LOSCoords[2]
            #pygame.draw.line(surface, (0, 0, 0), (Target.rect.centerx, Target.rect.centery), (self.rect.centerx, self.rect.centery))
        if LOSCoords[0] and not self.noMove:
            #print("Moving to LAST SEEN")
            #pygame.draw.circle(surface, (0, 255, 0), (self.lastSeenX, self.lastSeenY), 4)
            moveX = self.lastSeenX - self.rect.centerx  # If there is NO LOS, move to last seen X and Y
            moveY = self.lastSeenY - self.rect.centery
            #pygame.draw.line(surface, (0, 0, 0), (self.lastSeenX, self.lastSeenY), (self.rect.centerx, self.rect.centery))
        elif LOSCoords[0] and self.noMove:  # If movement is blocked, move to a direction cardinal to the last Seen
            #print("Moving to Temp")
            #pygame.draw.circle(surface, (255, 0, 0), (self.tempseenX, self.tempseenY), 4)
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
        self.xcol, self.ycol = False, False
        self.rect.centerx += round(delx)
        if pygame.sprite.collide_mask(self, testMap):  # Move in x direction, move back if col
            self.xcol = True
            self.rect.centerx -= round(delx)
            #print("X collision moved back x")
        self.rect.centery += round(dely)
        # if self.xcol:  # Move in y directoin
        #     self.rect.centery += 2  # Move 2 if no horizontal movement
        # else:
        #     self.rect.centery += round(dely)  # Move x and y
        #     print("ADD DELY")
        if pygame.sprite.collide_mask(self, testMap):  # Check collision for y
            self.ycol = True
            #print("Y collision moved back y")
            if self.xcol:
                self.rect.centery -= 2  # Move back 2 if moved forward 2
                #print("SUB  NEG 2")
            else:
                self.rect.centery -= round(dely)  # Move back dely if moved dely
                #print("SUB DELY")
        # if not self.ycol and not self.xcol:
        #     #print("Moved X AND Y")
        # if self.xcol and not self.ycol:
        #     #print("Moved Y but not X")


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

            #surface.blit(self.image, self.rect)  # Blit an individual bullet, not needed unless testing

            if pygame.sprite.collide_mask(self, self.target) and not lostLOS:
                self.image = pygame.transform.scale(pygame.image.load('LOSTarget.png'), (10, 10))

        return [lostLOS, self.target.rect.centerx,
                self.target.rect.centery]  # Returns True/False based on if LOS was broken and a last seen location


daveLOS = LOSBullet(dave, player)
source = LightSource([player.rect.centerx, player.rect.centery], 155, 30)
#source.calculateLights()

# Fake player is an invisible "Player" used to detect collisions
player.rect.x, player.rect.y = 100, 100
playerspeed = 3

source = LightSource([player.rect.centerx, player.rect.centery], 155, 60, 300)
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
    dave.goToLastSeen(daveLOS.checkLOS(), player)

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
        print("flip")

    if player_angle > 359:
        player_angle -= 360
        print("FLIP")

    if mouse_x > player.rect.x + (player.rect.width / 2):
        target_angle = 270 - math.degrees(math.atan((mouse_y - player.rect.y - (player.rect.height / 2)) / (mouse_x - player.rect.x - (player.rect.width / 2))))
    elif mouse_x < player.rect.x + (player.rect.width / 2):
        target_angle = 90 - math.degrees(math.atan((mouse_y - player.rect.y - (player.rect.height / 2)) / (mouse_x - player.rect.x - (player.rect.width / 2))))

    #print(f"angle: {player_angle} target: {target_angle}")
    if player_angle < 90 and target_angle > 270:
        player_angle -= (player_angle - target_angle) % 360 / 10
        #print("WORKS")

    elif player_angle > 270 and target_angle < 90:
        player_angle += (target_angle - player_angle) % 360 / 10
        print("works")

    else:
        player_angle -= (player_angle - target_angle) / 10

    if int(player_angle) != int(target_angle):
        source.changeDirection(int(-(source.width / 2) - player_angle - 90))

    source.drawLights()
    surface.blit(testMap.image, (0, 0))
    blitRotate(surface, player.image, (player.imageX, player.imageY), player_angle)
    surface.blit(dave.image, dave.rect)
    surface.blit(update_fps(), (10, 0))
    pygame.display.update()
    fpsClock.tick(FPS)

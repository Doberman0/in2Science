#Tank trouble in PyGame

import pygame, math, sys
from pygame.locals import *

#CONSTANTS NEEDED
WHITE = (255,255,255)
BLUE  = (  0,  0,255)
BLACK = (  0,  0,  0)
SCREEN_SIZE = 600
BLOCK_SIZE = 15
DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE),0,32) #initializes the screen
FPS = 60 #60FPS masterrace
FPS_CLOCK = pygame.time.Clock()

Positions = {'Projectiles':[], 'Tanks':[], 'WallTiles':[]} #stores the positions of all the objects in the game


class Tile: #Square tile in a maze
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.width = SCREEN_SIZE//BLOCK_SIZE #should be set to 40 (size of sprite)
        self.sprite = pygame.image.load('Wall.png')
        self.rect = pygame.Rect(self.pos_x,self.pos_y, self.width, self.width)#self.sprite.get_rect()

    def Draw(self):
        #pygame.draw.rect(DISPLAYSURF, BLACK, (self.pos_x,self.pos_y,self.width,self.width))
        DISPLAYSURF.blit(self.sprite, (self.pos_x,self.pos_y))


class Maze:
    def __init__(self):
        self.maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1], #View this as a Transposed matrix
                     [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,1,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,1,1,1,0,0,0,0,1,1,1,1,1],
                     [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,1,0,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,1,1,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                     [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
                     ]
        self.maze = self._MakeMaze() #converts 1s and 0s into tiles and empty spaces respectively

    def _MakeMaze(self):
        for y in range(BLOCK_SIZE):
            for x in range(BLOCK_SIZE):
                if self.maze[x][y] == 1:
                    t = Tile(x*SCREEN_SIZE/BLOCK_SIZE,y*SCREEN_SIZE/BLOCK_SIZE)
                    Positions['WallTiles'].append(t)
                    self.maze[x][y] = t
                    
    def Draw(self):
        for row in self.maze:
            for block in row:
                block.Draw()
        

class Projectile:
    def __init__(self, pos_x, pos_y, angle, tank_origin):
        self.radius = 15 #size of image
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.angle = angle
        self.tank_origin = tank_origin
        self.speed_x = self.speed_y = 3
        self.sprite = ''
        if tank_origin == 1:
            self.sprite = pygame.image.load('Bullet.png')
        else:
            self.sprite = pygame.image.load('Bullet2.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.radius, self.radius) 

    def Draw(self):
        DISPLAYSURF.blit(self.sprite, (self.pos_x,self.pos_y))
        
    def Update(self): #changes the position of the projectile every second
        rad = math.radians(self.angle)
        self.pos_x += self.speed_x * math.sin(rad)
        self.pos_y -= self.speed_y * math.cos(rad)
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.radius, self.radius)
            
        

class Tank:
    def __init__(self, pos_x, pos_y, orientation, player_no = 1):
        self.pos_x = pos_x #center of tank
        self.pos_y = pos_y #center of tank
        self.orientation = orientation #in deg. 0 deg is the north line
        self.sprite = ''
        self.width = 64
        self.height = 64
        self.player_no = player_no
        self.speed = 1 #projectiles don't interract properly when speed > 1 ..?
        if self.player_no == 1: #i.e. player 1
            self.sprite = pygame.image.load('RedTank.png')
        else: #i.e. player 2
            self.sprite = pygame.image.load('GreenTank.png')
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def Draw(self):
        s = pygame.transform.rotozoom(self.sprite, -self.orientation, 1)
        DISPLAYSURF.blit(s, (self.pos_x, self.pos_y))
        #Updating rect for collision!
        self.rect = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)
    
    def TurnLeft(self):
        self.orientation -= 1

    def TurnRight(self):
        self.orientation += 1

    def MoveUp(self):
        rad = math.radians(self.orientation)
        self.pos_x += self.speed * math.sin(rad)
        self.pos_y -= self.speed * math.cos(rad)

    def MoveDown(self):
        rad = math.radians(self.orientation)
        self.pos_x -= self.speed * math.sin(rad)
        self.pos_y += self.speed * math.cos(rad)

    def Shoot(self): #get it to shoot projectiles out the front
        p = Projectile(self.pos_x, self.pos_y, self.orientation, self.player_no)
        Positions['Projectiles'].append(p)


#Main game's functions
def init(): #initalizing a loop
    pygame.init()
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('Tank trouble')

def fin(): #finishing off a loop
    CheckForCollisions()
    UpdateProjectiles()
    pygame.display.update()
    FPS_CLOCK.tick(FPS)

def MakeTank(x, y, angle, player = 1):
    t = Tank(x,y,angle,player)
    Positions['Tanks'].append(t)
    return t
    
def DrawEverything():
    for i in Positions['Projectiles']:
        i.Draw()
    for i in Positions['Tanks']:
        i.Draw()
    for i in Positions['WallTiles']:
        i.Draw()

def UpdateProjectiles():
    for i in Positions['Projectiles']:
        i.Update()

def CollisionProjectiles(): #Alters projectiles if they hit something
                            #Done in O(p) where p = num of projectiles
    for proj in Positions['Projectiles']:
        for wall in Positions['WallTiles']:
            if pygame.sprite.collide_rect(proj, wall):
                #checking if the ball collides with a wall and thus reflecting it
                if (proj.pos_y) <= (wall.pos_y + 40): #check if ball's hitting Vertically
                    proj.speed_y *= -1
                    proj.speed_x *= -1
                if (proj.pos_x) >= (wall.pos_x): #check if ball's hitting wall horizontally
                    proj.speed_x *= -1
        for tank in Positions['Tanks']: #checks if a projectile has destroyed a tank
            if pygame.sprite.collide_rect(proj, tank) and (proj.tank_origin != tank.player_no):
                tank.sprite = pygame.image.load('Boom.png')

def CollisionTanks(): #Handles collisions in tanks
                      #Check for collisions discretely as opposed to continously
    for tank in Positions['Tanks']:
        collision_list = pygame.sprite.spritecollide(tank, Positions['WallTiles'], False)
        if collision_list != []: #i.e. there's a collision
            #Don't move forward
            pass

def CheckForCollisions():
    CollisionProjectiles()
    CollisionTanks()

def PlayerMovement(keys_pressed): #Checks for player movement
    #controls for player 1
    temp1 = t1
    temp2 = t2
    if keys_pressed[K_LEFT]:
            t1.TurnLeft()
    elif keys_pressed[K_RIGHT]:
        t1.TurnRight()
    elif keys_pressed[K_UP]:
        t1.MoveUp()
    elif keys_pressed[K_DOWN]:
        t1.MoveDown()
    else:
        pass

    #controls for player 2
    if keys_pressed[K_e]:
        t2.MoveUp()
    elif keys_pressed[K_s]:
        t2.TurnLeft()
    elif keys_pressed[K_d]:
        t2.MoveDown()
    elif keys_pressed[K_f]:
        t2.TurnRight()
    

#Main game
if __name__ == '__main__':

    #Initialising the game
    t1 = MakeTank(100,50,0)
    t2 = MakeTank(100,300,0,2) #making player 2
    maze = Maze()
    init()

    #Main game logic loop
    while True:
        DISPLAYSURF.fill(WHITE)
        DrawEverything()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN: #No consecutive fire
                if event.key == pygame.K_m:
                    t1.Shoot()
                if event.key == pygame.K_q:
                    t2.Shoot()

        keys_pressed = pygame.key.get_pressed()

        PlayerMovement(keys_pressed)

        fin()

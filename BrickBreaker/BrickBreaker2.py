#Making my own brick breaker
import pygame, sys, random, math
from pygame.locals import *

#Constants needed
BRICK_LEN = 45
BRICK_WIDTH = 20
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 500
MAX_OBJ_HEIGHT = 50 #This is the maximum height the ball and bricks can reach (i.e. game border)

#Colours
WHITE  = (255, 255, 255)
BLACK  = (  0,   0,   0)
RED    = (128,   0,   0)
RED2   = (179,   0,   0)
RED3   = (255,   0,   0)
GREEN  = (  0, 255,   0)
BLUE   = (  0,   0, 255)
YELLOW = (244, 244,  66)
GREY   = (217, 217, 217)

#Define Screen
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

#Clock
FPS = 60
FPS_CLOCK = pygame.time.Clock()

#Game states
START     = 0
PLAYING   = 1
WON       = 2
GAME_OVER = 3

#Player stats
LIVES = 3
SCORE = 0


class Paddle:
    def __init__(self):
        self.length = 50
        self.width = 10
        self.pos_x = (SCREEN_WIDTH//2) - (self.length//2)
        self.pos_y = SCREEN_HEIGHT - self.width - 5
        self.speed = 3
        self.Rect = pygame.Rect(self.pos_x, self.pos_y, self.length, self.width) #Used for collision detection

    def Draw(self):
        pygame.draw.rect(SCREEN, BLUE, (self.pos_x, self.pos_y, self.length, self.width))
        self.Rect = pygame.Rect(self.pos_x, self.pos_y, self.length, self.width) #Need to update the rectangle
        
    def Move(self, key): #Moves the paddle until it collides with the wall
        if key == 'Right' and (self.pos_x+self.length < SCREEN_WIDTH):
            self.pos_x += self.speed
        elif key == 'Left' and (self.pos_x > 0):
            self.pos_x -= self.speed


class Ball:
    def __init__(self, radius = 5):
        self.radius = 5
        self.pos_x = self.left = int((SCREEN_WIDTH//2) - (self.radius//2) + 3)
        self.pos_y = self.top = int(SCREEN_HEIGHT - self.radius - 15)
        self.vel_x = 5
        self.vel_y = -5
        self.right = self.pos_x + self.radius
        self.bottom = self.pos_y + self.radius
        self.Rect = pygame.Rect(self.pos_x - self.radius,self.pos_y,2*int(self.radius),2*int(self.radius))

    def Draw(self):
        pygame.draw.circle(SCREEN, BLUE, (int(self.pos_x), int(self.pos_y)), int(self.radius))
        self.Rect = pygame.Rect(self.pos_x - self.radius,self.pos_y,2*self.radius,2*self.radius)

    def Update(self):
        #update velocity
        self.pos_x += self.vel_x
        self.pos_y += self.vel_y

        #Update it's coordinates
        self.Rect = pygame.Rect(self.pos_x - self.radius,self.pos_y,2*self.radius,2*self.radius)
        self.left = self.pos_x
        self.top = self.pos_y
        self.bottom = self.pos_y + self.radius
        self.right = self.pos_x + self.radius

    def SetVel(self, angle):
        speed = math.sqrt(5**2 + (-5)**2)
        self.vel_x = speed * math.sin(math.radians(angle))
        self.vel_y = -1 * speed * math.cos(math.radians(angle))


class Brick:
    def __init__(self, x, y, hits):
        self.pos_x = x
        self.pos_y = y
        self.length = BRICK_LEN
        self.width = 10
        self.colour = RED
        self.num_of_hits = hits #Determines the hardness of the brick. i.e. the number of hits needed to destroy the brick
        self.Rect = pygame.Rect(self.pos_x, self.pos_y, self.length, self.width)

    def Draw(self):
        if self.num_of_hits == 1:
            self.colour = RED
        elif self.num_of_hits == 2:
            self.colour = RED2
        else:
            self.colour = RED3
        pygame.draw.rect(SCREEN, self.colour, (self.pos_x, self.pos_y, self.length, self.width))
        self.Rect = pygame.Rect(self.pos_x, self.pos_y, self.length, self.width)


class AngleLine:
    def __init__(self, x1, y1):
        self.x1  = x1
        self.y1  = y1
        #self.direction = 1 #This increases/decreases the angle
        self.angle = 0
        self.line_len = 20 #The length of the line is 20px
        self.y2 = self.y1 - (self.line_len * math.cos(math.radians(self.angle))) - 10
        self.x2 = self.x1 + (self.line_len * math.sin(math.radians(self.angle)))

    def Draw(self):
        pygame.draw.line(SCREEN, WHITE, (self.x1, self.y1), (self.x2, self.y2))

    def Move(self, direction, ball):
        if direction == 1 and self.angle<90:
            self.angle += 1
        elif direction == -1 and self.angle > -90:
            self.angle -= 1
        self.y2 = int(ball.pos_y) - (self.line_len * math.cos(math.radians(self.angle))) - 10
        self.x2 = int(ball.pos_x)  + (self.line_len * math.sin(math.radians(self.angle)))

    def Reinitialize(self, paddle):
        self.x1 = paddle.pos_x + (paddle.length//2)
        self.y1 = paddle.pos_y - ball.radius
        self.angle = 0
        self.y2 = self.y1 - (self.line_len * math.cos(math.radians(self.angle))) - 10
        self.x2 = self.x1 + (self.line_len * math.sin(math.radians(self.angle)))
            

def MakeBricks():
    bricks = []
    y_ofs = MAX_OBJ_HEIGHT + 30
    bricks = []
    for row in range(random.randint(2,6)): #makes a random number of rows of bricks
        x_ofs = 50
        for column in range(8): #makes 8 columns of bricks
            bricks.append(Brick(x_ofs,y_ofs, random.randint(1,3)))
            x_ofs += BRICK_LEN + 15
        y_ofs += BRICK_WIDTH + 25
    return bricks

def CollisionDetection(ball, bricks, paddle, score, lives, state, line):
    #print('In func score: ' + str(score))
    for brick in bricks:
        if ball.Rect.colliderect(brick.Rect):
            score += 1
            ball.vel_y = -ball.vel_y #direction gets inverted
            brick.num_of_hits -= 1
            if brick.num_of_hits == 0:
                bricks.remove(brick)
            break #so this game logic only effects one brick at a time

    #Check if you've won
    if len(bricks) == 0:
        GAME_STATE = WON

    #If ball hits the wall
    if ball.right >= SCREEN_WIDTH:
        ball.vel_x = -ball.vel_x
    elif ball.left <= 0:
        ball.vel_x = -ball.vel_x
    if ball.Rect.top <= MAX_OBJ_HEIGHT:
        ball.vel_y = -ball.vel_y
        
    #If the ball hits the paddle
    if ball.Rect.colliderect(paddle.Rect):
        ball.Rect.top = paddle.Rect.top - (2*ball.radius)
        ball.vel_y = -ball.vel_y #ball goes up

    #If the ball misses the paddle
    elif ball.Rect.top > paddle.Rect.top: #i.e. the ball is lower than the paddle
        lives -= 1
        line.Reinitialize(paddle)
        if lives > 0:
            state = START
        else:
            state = GAME_OVER

    return score, lives, state


def DrawEverything(paddle, bricks, ball, score, num_of_lives_left):
    OutputOnScreen('Score: ' + str(score), (20,10))
    OutputOnScreen('Lives: ' + str(num_of_lives_left), (160,10))
    #Drawing screen border
    pygame.draw.rect(SCREEN, GREEN, (0, MAX_OBJ_HEIGHT, SCREEN_WIDTH-1, SCREEN_HEIGHT), 2)
    paddle.Draw()
    for brick in bricks:
        brick.Draw()
    ball.Draw()


def KeyboardInput():
    keys = pygame.key.get_pressed()
    if keys[K_RIGHT]:
        paddle.Move('Right')
    elif keys[K_LEFT]:
        paddle.Move('Left')


def OutputOnScreen(message, pos = (100,100), temp_font = 'Times New Roman'):
    font_size = 30
    my_font = pygame.font.SysFont(temp_font, font_size)
    my_message = my_font.render(message, 1, YELLOW)
    SCREEN.blit(my_message, pos)


if __name__ == '__main__':
    paddle = Paddle()
    bricks = MakeBricks()
    ball = Ball()
    line = AngleLine(ball.pos_x, ball.pos_y)
    GAME_STATE = START
    
    while True:
        
        #Initialising loop
        pygame.init()
        SCREEN.fill(BLACK)
        pygame.display.set_caption('Brick Breaker')
        
        for event in pygame.event.get():
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == K_SPACE and GAME_STATE == START:
                    GAME_STATE = PLAYING
                    ball.SetVel(line.angle)
                elif event.key == K_RETURN and (GAME_STATE == GAME_OVER or GAME_STATE == WON):
                    GAME_STATE = START
                    LIVES = 3
                    SCORE = 0
                    bricks = MakeBricks()
                    paddle.pos_x = (SCREEN_WIDTH//2) - (paddle.length//2)
                    paddle.pos_y = SCREEN_HEIGHT - paddle.width - 5
                    line = AngleLine(int((SCREEN_WIDTH//2) - 5//2 + 3),
                                     int(SCREEN_HEIGHT - 5 - 15))
                
        #Checking game states and responding accordingly
        if GAME_STATE == START:
            #Initialise ball
            ball.pos_x = paddle.pos_x + paddle.length/2 
            ball.pos_y = paddle.pos_y - ball.radius

            #initialise Line
            line.Draw()

            #Draw balls, bricks &
            DrawEverything(paddle, bricks, ball, SCORE, LIVES)

            #Update angle of projection and line
            keys = pygame.key.get_pressed()
            if keys[K_RIGHT]:
                line.Move(1, ball)
            elif keys[K_LEFT]:
                line.Move(-1, ball)
                
        elif GAME_STATE == PLAYING:
            #Move ball
            ball.Update()

            #Check for collision detection
            SCORE, LIVES, GAME_STATE = CollisionDetection(ball, bricks, paddle, SCORE, LIVES, GAME_STATE, line)

            #Drawing everything on the screen
            DrawEverything(paddle, bricks, ball, SCORE, LIVES)

            #Getting keyboard input for paddle
            KeyboardInput()
            
        elif GAME_STATE == GAME_OVER:
            #Output: score, a message that you've lost and that you need to hit Enter to play again
            OutputOnScreen("Score: " + str(SCORE), ((SCREEN_WIDTH/2 - 60,100)))
            OutputOnScreen("Awww. You didn't beat the game :'(", (95,170))
            OutputOnScreen("Hit the Enter/Return key to play again", (80,350))

        elif GAME_STATE == WON:
            #Output: score, a message that you've lost and that you need to hit Enter to play again
            OutputOnScreen("Score: " + str(SCORE), ((SCREEN_WIDTH/2 - 40,50)))
            #Sans == <3
            OutputOnScreen("You... won...", (SCREEN_WIDTH/2 - 60,100), 'Comic Sans MS')
            OutputOnScreen("Chances are, though...", (160,150), 'Comic Sans MS')
            OutputOnScreen("You're just a dirty hacker, aren't you?", (35, 200), 'Comic Sans MS')
            OutputOnScreen("Yeah, get outta here.", (165,250), 'Comic Sans MS')
            OutputOnScreen("Hit the Enter/Return key to play again", (80,400))

        #Finalising stuff in loop
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

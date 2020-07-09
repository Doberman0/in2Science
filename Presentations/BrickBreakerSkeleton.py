#Making my own brick breaker
import pygame, sys
from pygame.locals import *

#Constants needed

#Colours

#Define Screen

#Clock

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
        '''
        To do:
            - length of paddle
            - width of paddle
            - position tuple of paddle
            - speed that the paddle moves at
            - the paddle's rect (for collision detection)
        '''
        
    def Draw(self):
        '''
        To do:
            - Draw the paddle
            - Update the paddle's Rect
        '''
        
    def Move(self, key): #Moves the paddle until it collides with the wall
        '''
        To do:
            - Move the paddle (left or right) according to the key entered
            - Make sure that the paddle doesn't move past the edges of the screen!
        '''

class Ball:
    def __init__(self, radius = 5):
        '''
        To do:
            - Get the radius attribute
            - Set the horizontal velocity
            - Set the veritcal velocity
            - Set the attribute for the top, bottom, right and left of the ball (rest)
            - Set the Rect attribute for collision
        '''
        
    def Draw(self):
        '''
        To do:
            - Draw the ball
            - Update the Rect
        '''
       
    def Update(self):
        '''
        To do:
            - Update the position of the ball using the horizontal and vertical velocity
            - Update the top, bottom, right and left of the ball (rect)
        '''


class Brick:
    def __init__(self, x, y):
        '''
        To do:
            - Set the position of the brick
            - Set the length and width of the brick
            - Set the Rect attribute for the brick (for collision detection)
        '''

    def Draw(self):
        '''
        To do:
            - Draw the brick
            - Set the Rect for the brick
        '''
        

def MakeBricks():
    '''
    To do:
        - Store the bricks in a list
        - Make the brick using a nested for loop
        - Update position of the bricks to make rows
    '''

def CollisionDetection(ball, bricks, paddle, score, lives, state):
    '''
    To do:
        - Check if there's a collision with any of the bricks (can only handle 1 collision per frame)
        - Check if all the bricks have been eliminated
        - Check if the ball hits the wall
        - Check if the ball hits the paddle
        - Adjust all of the aforementioned collisions by changing their horizontal and vertical velocities
        - If the ball is lower than the paddle, reduce the number of lives by 1
            - If lives = 0, change the game state
    '''

def DrawEverything(paddle, bricks, ball, score, num_of_lives_left):
    '''
    To do:
        - Draw the Score & lives on the screen
        - Draw the border/walls
        - Draw the following by using their .Draw() methods
            - Paddle
            - Bricks
            - Ball
    '''

def OutputOnScreen(message, pos = (100,100), temp_font = 'Times New Roman'):
    '''
    Outputs any message on the screen.
    Normally used for when the game is over.
    '''

if __name__ == '__main__':
    '''
    To do:
        - Initialise the paddle
        - Initialise the bricks
        - Initialise the ball
        - Initialise the game state
    '''
    
    while True:
        
        #Initialising loop
        pygame.init()
        SCREEN.fill(BLACK)
        #Set caption
        
        for event in pygame.event.get():
            #exiting the game
            if event.type== pygame.QUIT:
                pygame.quit()
                sys.exit()
            #if a button is pressed discretely
                #Use certain keys to start the game depending on the game state
                
                #User certain keys to restart the game once you won or lost
                    '''
                    To do:
                        - Intialise the game state, lives, score
                        - Make new bricks to replace the old
                        - Initialise the ball and paddle
                    '''
                
        #Checking game states and responding accordingly
        if GAME_STATE == START:
            #Initialise ball
            #Draw balls, bricks, paddle, score and lives
                
        elif GAME_STATE == PLAYING:
            '''
            To do:
                - Move ball
                - Check for collision detection
                - Drawing everything on the screen
                - Getting keyboard input for paddle
            '''
            
        elif GAME_STATE == GAME_OVER: #i.e Player has lost
            #Output: score, a message that you've lost and that you need to hit Enter to play again


        elif GAME_STATE == WON:
            #Output: score, a message that you've lost and that you need to hit Enter to play again

        #Finalising stuff in loop
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

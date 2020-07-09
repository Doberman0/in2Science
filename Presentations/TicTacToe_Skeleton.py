import pygame, sys
from pygame.locals import * #This is for variable name convinience. E.g. QUIT

class Box:
    def __init__(self, pos_x, pos_y): #You'll want the x, y position of the box
        pass
    
    def Draw(self):
        pass
    
    def Val_Is_Set(self): #checks if box is x, o, or empty
        pass
    
    def _Draw_X(self):
        pass
    
    def _Draw_O(self): #Can't it just replace with a circle
        pass
    
    def Click_In_Range(self, PositionTuple):
        pass

class Board:
    def __init__(self, pos_x, pos_y, scale):
        pass
    
    def Init_Board(self,scale): #used to initalise the board
        pass
    
    def Update_Board(self, position_tuple, player_1 = True): #Adds naughts and crosses
        pass
    
    def Draw(self): #Draws all the boxes
        pass
    
    def Is_Full(self): #Checks if the board is full. i.e. no more moves can be made
        pass
    
    def Win(self): #Brute forces all possible way to achieve victory in 3x3 Tic-Tac-Toe
       pass
    
    def WinScreen(self, player_1):
        pass

#Global Parameters
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
RED    = (255,  0,  0)
SCREEN_SIZE = 500
BOX_LEN = 100
DISPLAYSURF = pygame.display.set_mode((SCREEN_SIZE,SCREEN_SIZE),0,32)
FPS = 30
FPS_CLOCK = pygame.time.Clock()

def init(): #Just a basic function used to make the program logic clearer
    pygame.init()
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('Tic-Tac-Toe')
     
if __name__ == "__main__":
    #intialising the game
    init()
    B = Board(SCREEN_SIZE/4,SCREEN_SIZE/4,BOX_LEN)
    font = pygame.font.Font(None, 25)
    label_2 = ''
    player = True #sets to player 1 by default
    running = True
    
    while running: #main game loop
        DISPLAYSURF.fill(WHITE)
        B.Draw() #Drawing the board on a blank canvas at every iteration of the clock
        win = B.Win() #check winning condition
        
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not win:
                pass
        
        if win: #takes you to a winning screen if you win
            B.WinScreen(player_1)
                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

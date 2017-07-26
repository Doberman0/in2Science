import pygame, sys
from pygame.locals import * #This is for variable name convinience. E.g. QUIT

class Box:
    def __init__(self,pos_x,pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.length = 50 #i.e. the boxes are length x length large

    def _Draw_Circ(self, color = WHITE): #private helper method meant to draw a circle in the "box"
        if color == WHITE:
            pygame.draw.circle(DISPLAYSURF, WHITE, (self.pos_x + int(self.length/2), self.pos_y + int(self.length/2)), int(self.length/2 - 3))
        elif color == RED:
            pygame.draw.circle(DISPLAYSURF, RED, (self.pos_x + int(self.length/2), self.pos_y + int(self.length/2)), int(self.length/2 - 3))
        else:
            pygame.draw.circle(DISPLAYSURF, YELLOW, (self.pos_x + int(self.length/2), self.pos_y + int(self.length/2)), int(self.length/2 - 3))
            
    def Draw(self,no_player=True): 
        pygame.draw.rect(DISPLAYSURF, BLUE, (self.pos_x,self.pos_y,self.length,self.length))
        if no_player:
            self._Draw_Circ()
        elif no_player == 1: #i.e. player 1 has slotted a checker in this specific box
            self._Draw_Circ(RED)
        else:
            self._Draw_Circ(YELLOW)

class Board:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.boxes = self.Init_Board() #stores the board and the checkers in a matrix/2D list

    def Init_Board(self):
        board = [[0, 0, 0, 0], #initial board
                 [0, 0, 0, 0],
                 [0, 0, 0, 0],
                 [0, 0, 0, 0]
                 ]
        
        for i in range(0, 4):
            for j in range(0,4):
                b = Box(i,j,100)
                board[i][j] = b

        return board

    def Add_Move(self, column, player_1 = True):
        
        
        
            
#Some constants I require
YELLOW = (255,255,  0)
RED    = (255,  0,  0)
BLUE   = (  0,  0,128) #Navy blue technically
WHITE  = (255,255,255)
DISPLAYSURF = pygame.display.set_mode((600,600),0,32)

def init():
    pygame.init()
    DISPLAYSURF.fill(WHITE)
    pygame.display.set_caption('Connect 4')
    
if __name__ == "__main__":
    init()
    while 1: #main game loop
        b1 = Box(200,200,50)
        b1.Draw()
        #This checks for you closing pygame
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()

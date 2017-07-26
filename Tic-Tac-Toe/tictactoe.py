import pygame, sys
from pygame.locals import * #This is for variable name convinience. E.g. QUIT

class Box:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.length = 100
        self.space_nicer = 10
        self.padding = 2
        self.line_width = 2
        self.val = None #denotes if the box has cross, naught or is empty ('o','x' or None respectively)
    
    def Draw(self):
        pygame.draw.rect(DISPLAYSURF, BLACK, (self.pos_x,self.pos_y,self.length,self.length), self.padding)
        if self.val == 'x':
            self._Draw_X()
        elif self.val == 'o':
            self._Draw_O()

    def Val_Is_Set(self):
        return self.val != None

    def _Draw_X(self):
        pygame.draw.line(DISPLAYSURF, BLACK, (self.pos_x+self.space_nicer, self.pos_y+self.space_nicer), (self.pos_x+self.length-self.space_nicer, self.pos_y+self.length-self.space_nicer),self.line_width)
        pygame.draw.line(DISPLAYSURF, BLACK, (self.pos_x+self.space_nicer, self.pos_y-self.space_nicer+self.length), (self.pos_x+self.length-self.space_nicer, self.pos_y+self.space_nicer),self.line_width)

    def _Draw_O(self):
        pygame.draw.circle(DISPLAYSURF, BLACK, (self.pos_x+int(self.length/2),self.pos_y+int(self.length/2)),int(self.length/2) - self.padding)
        pygame.draw.circle(DISPLAYSURF, WHITE, (self.pos_x+int(self.length/2),self.pos_y+int(self.length/2)),int(self.length/2) - 2*self.padding)

    def Click_In_Range(self, PositionTuple):
        if (PositionTuple[0] in range(self.pos_x, self.pos_x+self.length+1)) and (PositionTuple[1] in range(self.pos_y, self.pos_y+self.length+1)):
            return True
        else:
            return False
        

class Board:
    def __init__(self, pos_x, pos_y, scale):
        #Top left hand corner of board
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.boxes = self.Init_Board(scale) #stores the board and the checkers in a 3x3 matrix/2D list

    def Init_Board(self,scale):
        board = [[0, 0, 0],
                 [0, 0, 0],
                 [0, 0, 0]
                 ]
        
        for i in range(0, 3):
            for j in range(0,3):
                b = Box(scale*(i+1),scale*(j+1))
                board[i][j] = b

        return board

    def Update_Board(self, position_tuple, player_1 = True): #Adds naughts and crosses
        for i in self.boxes:
            for box in i:
                if box.Click_In_Range(position_tuple) and not box.Val_Is_Set():
                    if player_1:
                        box.val = 'x'
                    else:
                        box.val = 'o'
                    return True
        return False

    def Draw(self): #Draws all the boxes
        for i in self.boxes:
            for box in i:
                box.Draw()

    def Is_Full(self): #Checks if the board is full. i.e. no more moves can be made
        for i in self.boxes:
            for box in i:
                if box.val == None:
                    return False
        return True
        
    def Win(self): #Brute forces all possible way to achieve victory in 3x3 Tic-Tac-Toe
        x = self.boxes
        for i in range(0,3): #checks all horizontal rows
            if (x[i][0].val == x[i][1].val == x[i][2].val) and (x[i][0].val != None):
                return True
        for j in range(0,3): #checks all vertical rows
            if (x[0][j].val == x[1][j].val == x[2][j].val) and (x[0][j].val != None):
                return True
        if (x[0][0].val == x[1][1].val == x[2][2].val) and (x[0][0].val != None): #checks descending diagonal
            return True
        if (x[0][2].val == x[1][1].val == x[2][0].val) and (x[0][2].val != None): #checks ascending diagonal
            return True
        return False

    def WinScreen(self, player_1):
        font = pygame.font.Font(None, 75)
        label2 = ''

        if not player_1:
            label2 = font.render("Player 1 won!", 1, RED)
        else:
            label2 = font.render("Player 2 won!", 1, RED)

        #Outputting message
        DISPLAYSURF.blit(label2, (100,SCREEN_SIZE/2 - 50))

    

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
    player_1 = True
    running = True
    
    while running: #main game loop
        DISPLAYSURF.fill(WHITE)
        B.Draw() #Drawing the board on a blank canvas at every iteration of the clock
        win = B.Win()
        
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and not win:
                pos = (PosX, PosY) = pygame.mouse.get_pos()
                if B.Update_Board(pos, player_1):
                    player_1 = not player_1
        
        if win:
            B.WinScreen(player_1)
                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)

'''
Classes needed:
    - Stone
    - Board
    - Player
'''

import random, sys, pygame, time, copy, itertools
from pygame.locals import *

#Global Parameters
WHITE  = (255,255,255)
BLACK  = (  0,  0,  0)
SCREEN_SIZE_X = 800
SCREEN_SIZE_Y = 1000
BOX_LEN = 100
SCREEN = pygame.display.set_mode((SCREEN_SIZE_X,SCREEN_SIZE_Y),0,32)
FPS = 60
FPS_CLOCK = pygame.time.Clock()

BLACK_PLAYER = True
WHITE_PLAYER = False

BLACK_STONE = pygame.image.load('BlackStone.png')
WHITE_STONE = pygame.image.load('WhiteStone.png')

class StoneTile:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y
        self.parity = None #i.e. whether it's black (True) XOR white (False)
        self.sprite = pygame.image.load('StoneBackground.png')
        self.length = 100 #This is the size of the box in pixels

    def Draw(self):
        SCREEN.blit(self.sprite, (self.pos_x,self.pos_y))

    def Flip(self):
        self.parity = not self.parity
        if self.parity: #i.e. black
            self.sprite = BLACK_STONE
        else: #i.e. white
            self.sprite = WHITE_STONE

    def RemoveStone(self): #initialises the board again
        self.parity = None
        self.sprite = pygame.image.load('StoneBackground.png')

    def AddStone(self, player):
        if player == BLACK_PLAYER:
            self.parity = BLACK_PLAYER
            self.sprite = BLACK_STONE
        else:
            self.parity = WHITE_PLAYER
            self.sprite = WHITE_STONE

    def Flip(self):
        self.parity = not self.parity
        if self.parity == BLACK_PLAYER:
            self.sprite = BLACK_STONE
        else:
            self.sprite = WHITE_STONE

    def ClickInRange(self, pos_tuple):
        if (pos_tuple[0] in range(self.pos_x, self.pos_x+self.length+1)) and (pos_tuple[1] in range(self.pos_y, self.pos_y+self.length+1)):
            return True
        else:
            return False


class Board:
    def __init__(self):
        self.board = self._InitBoard()
        self.black_pieces = 0
        self.white_pieces = 0

    def Draw(self):
        for i in self.board:
            for tile in i:
                tile.Draw()

    def _InitBoard(self):
        #Filling the board with blank squares
        full_board = []
        temp_board = []
        for x in range(0,800, 100):
            for y in range(0, 800, 100):
                temp_board.append(StoneTile(x,y))
            full_board.append(temp_board)
            temp_board = []
        #Initialising the board with a white black pattern in the middle
        full_board[3][3].AddStone(WHITE_PLAYER)
        full_board[4][4].AddStone(WHITE_PLAYER)
        full_board[3][4].AddStone(BLACK_PLAYER)
        full_board[4][3].AddStone(BLACK_PLAYER)
        return full_board

    def Full(self): #Returns true if the board is full
        for i in self.board:
            for tile in i:
                if tile.parity == None:
                    return False
        return True

    def AllSameColour(self):
        initial_tile = None
        for i in self.board:
            for tile in i:
                if (initial_tile == None) and ((tile.parity == BLACK_PLAYER) or (tile.parity == WHITE_PLAYER)):
                    intial_tile = tile.parity
                if (tile.parity != None) and (tile.parity != intial_tile):
                    return False
        return True

    def _OnBoard(self, x,y): #This method checks if the x and y values are in the range()
        return (x in range(7)) and (y in range(7))

    def _TileAlreadyOnBoard(self, tile):
        for i in self.board:
            for stone in i:
                if stone == tile:
                    return True
        return False

    def AvailablePlaces(self, tile, player): #This method returns a list of the stones to flip
        if not self._TileAlreadyOnBoard(tile):
            return self.FlipStones(tile,player)
        return False

    def FlipStones(self, tile, player): #This method returns a list of the stones to flip
        #initially add the tile to the board for this to work
        tile.AddStone(player)
        
        tiles_to_flip = []
        x_initial, y_initial = self._Index2d(tile)
        for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
            x, y = x_initial, y_initial

            x += x_direction
            y += y_direction
            if self._OnBoard(x,y) and (self.board[x][y].parity == (not player)):  #i.e. traversing board so long as
                                                                                  #the opposite colour is present
                                                                                  #and you haven't fallen off the board
                x += x_direction
                y += y_direction

                if not self._OnBoard(x, y): #if you're off the board, then you can skip this iteration
                    continue
                
                while (self.board[x][y].parity != player):
                    x += x_direction
                    y += y_direction
                    if not self._OnBoard(x,y): #i.e. you run into a straight line of stones of the opposite parity
                        break

                if not self._OnBoard(x,y): #skips forward to the next iteration of the for loop
                    continue
                
                if (self.board[x][y].parity == player):
                    #Now we go backwards to the original stone appending the intermediate stones
                    #to the flip list
                    while True:
                        x -= x_direction
                        y -= y_direction
                        if ((x==x_initial) and (y == y_initial)):
                            break
                        tiles_to_flip.append(self.board[x][y])
        tile.RemoveStone()

        if len(tiles_to_flip)==0: #i.e. the move is invalid so you can't flip anything
            return False
        return tiles_to_flip
                    
        
    def Update(self, pos_tuple, player):
        for i in self.board:
            for tile in i:
                has_been_clicked = tile.ClickInRange(pos_tuple)
                if has_been_clicked:
                    if (tile.parity == None): #i.e. if the space is free
                        flip_tiles = self.FlipStones(tile, player) #Gets the stones to flip
                        if (flip_tiles != False): #if the move is actually valid
                            tile.AddStone(player)
                            if tile in flip_tiles:
                                flip_tiles.remove(tile)
                            #Flip the stones
                            for stone in flip_tiles:
                                stone.Flip()
                            #Updates score for AI and player
                            self._UpdateScore()
                            return True
                    else: #i.e you don't rotate the player
                        return False

    def _Index2d(self, tile): #returns the index of a tile in the form (row_num,column_num)
        for i, x in enumerate(self.board):
            if tile in x:
                return i, x.index(tile)

    def _UpdateScore(self):
        b = w = 0
        for row in self.board:
            for tile in row:
                if tile.parity == BLACK_PLAYER:
                    b += 1
                elif tile.parity == WHITE_PLAYER:
                    w += 1
        self.black_pieces = b
        self.white_pieces = w

def init(): #Just a basic function used to make the program logic clearer
    pygame.init()
    SCREEN.fill(WHITE)
    pygame.display.set_caption('Othello')
    
    
def OutputOnScreen(message, pos = (100,100), font_size = 30):
    temp_font = 'Times New Roman'
    my_font = pygame.font.SysFont(temp_font, font_size)
    my_message = my_font.render(message, 1, BLACK)
    SCREEN.blit(my_message, pos)
    
def Stats(black_pieces, white_pieces):
    #Outputting player's stats
    OutputOnScreen('Player ', (30,830))
    black = pygame.image.load('BlackStoneEmpty.png')
    SCREEN.blit(black,(115,820))
    OutputOnScreen('Pieces:' + str(black_pieces), (300,830))
    
    #Outputting the AI's stats
    OutputOnScreen('AI ', (70,920))
    white = pygame.image.load('WhiteStoneEmpty.png')
    SCREEN.blit(white,(115,910))
    OutputOnScreen('Pieces: ' + str(white_pieces), (300,920))

def AIGuess(board, player): #randomly returns a position unless a corner is available
    if board.Update((50,50),  player):
        return
    elif board.Update((50,750),  player):
        return
    elif board.Update((750,50),  player):
        return 
    elif board.Update((750,750),  player):
        return
    else: #Check all other positions
        for x in range(8):
            for y in range(8):
                if board.Update(((x*100)+50,(y*100)+50), player):
                    return #break out of the function

def GameOver(board, player):
    total_num_of_moves = 0
    for i in board.board:
        for tile in i:
            if tile.parity == None:
                x = board.AvailablePlaces(tile, player) #why is this returning false
                if isinstance(x, list):
                    total_num_of_moves += len(x)
    if total_num_of_moves == 0:
        OutputOnScreen('GAME OVER', (100,100), 75)
    
    
if __name__ == '__main__':
    #intialising the game
    init()
    B = Board()
    player = BLACK_PLAYER
    AI = WHITE_PLAYER
    player_turn = player
    running = True
    
    while running: #main game loop
        #GameOver(B, player_turn)
        SCREEN.fill(WHITE)
        B.Draw() #Drawing the board on a blank canvas at every iteration of the clock
        Stats(B.black_pieces, B.white_pieces)
        
        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if player_turn == AI:
                AIGuess(B, player_turn)
                player_turn = player

            elif (player_turn == player) and (event.type == pygame.MOUSEBUTTONDOWN):
                pos = (PosX, PosY) = pygame.mouse.get_pos()
                if B.Update(pos, player_turn):
                    player_turn = AI #i.e. if it was the black player, it's now the white player and vise-versa
                
        pygame.display.update()
        FPS_CLOCK.tick(FPS)
    
    





        

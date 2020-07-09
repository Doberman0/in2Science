import pygame, sys
from pygame.locals import *

pygame.init()

#Define some constants we'll need
WHITE = (255, 255, 255) #This is a tuple which contains RGB
                        #(Red,Green,Blue) values
RED   = ( 255 ,  0  ,   0)
GREEN = (   0 , 255 ,   0)
BLUE  = (   0 ,  0  , 255)
BLACK = (   0 ,  0  ,   0)

WIDTH, HEIGHT = 600, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption('First "Game"')

#position of text
top_left_x = top_left_y = 100

#Load font
font_size = 25
my_font = pygame.font.SysFont('Times New Roman', font_size)

#Render text
my_text = my_font.render('Hello World!', 1, BLACK)

while True:

    SCREEN.fill(WHITE) #At each iteration of the game loop,
                       #the screen is white washed

    '''
    Outputting the text onto the screen.
    The text will read, 'Hello World!' and will be in
    the font Times New Roman and size 25.
    It will read left-to-right starting from the position (100,100)
    '''
    SCREEN.blit(my_text, (top_left_x, top_left_y))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed() #This gets all the keys that have been pressed

    if keys[K_UP]:
        pass #Do something. Most likely movement upwards for player 1.
    if keys[K_w]:
        pass #Do something. Most likely movement upwards for player 2.

    pygame.display.update()

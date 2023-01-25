import sys
import pygame
from pygame.locals import *
import random
from array import *

pygame.init()
lost = False
won = False
##### VARIABLES #####

# colors
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
YELLOW = (255, 255, 0)
TEAL = (0, 255, 255)

colors = [BLUE, GREEN, RED, PURPLE, YELLOW, TEAL, BLACK, GRAY]

# sizes

width = 40
height = 40
margin = 10
window_size = [510, 510]

# arrays for game and mine values
grid = [[0 for x in range(10)] for y in range(10)]
values = [[0 for x in range(10)] for y in range(10)]
recursion = [[False for x in range(10)] for y in range(10)]



font = pygame.font.Font('freesansbold.ttf', 40)

# display surface
surface = pygame.display.set_mode(window_size)
pygame.display.set_caption("Minesweeper CSP Create Task")
clock = pygame.time.Clock()

# generate the mines and grid values
def generate(x, y):
    for i in range(20):
        intx = random.randint(0, 9)
        inty = random.randint(0, 9)

        while((intx == x or intx == x + 1 or intx == x - 1) and
              (inty == y or inty == y + 1 or inty == y - 1)):
            intx = random.randint(0, 9)
            inty = random.randint(0, 9)


        values[intx][inty] = 9

    for row in range(10):
        for column in range(10):
            count = 0
            if(column != 0 and values[row][column - 1] == 9):
                count += 1
            if(column != 9 and values[row][column + 1] == 9):
                count += 1
            if(row != 9 and values[row + 1][column] == 9):
               count += 1
            if(row != 0 and values[row - 1][column] == 9):
               count += 1
            if(row != 0 and column != 0 and values[row - 1][column - 1] == 9):
                count += 1
            if(row != 9 and column != 9 and values[row + 1][column + 1] == 9):
                count += 1
            if(row != 9 and column != 0 and values[row + 1][column - 1] == 9):
               count += 1
            if(row != 0 and column != 9 and values[row - 1][column + 1] == 9):
               count += 1

            if(values[row][column] != 9):
                values[row][column] = count
                        
##### FUNCTIONS #######

# create the grid
def drawGrid(grid):

    for row in range(10):
        for column in range(10):
            # create the game grid depending on where the user has clicked
            color = GRAY
            if(grid[row][column] == 1):
                color = RED
            if(grid[row][column] == 2):
                color = WHITE
                
            pygame.draw.rect(surface, color,
                             pygame.Rect(margin + column * (width + margin),
                                         margin + row * (height + margin),
                                         width, height))
            if(grid[row][column] == 2 and values[row][column] != 0 and values[row][column] != 9):
                # create the number grid based on where the mines are
                text = font.render(str(values[row][column]), True, colors[values[row][column]-1])
                textRect = text.get_rect()
                textRect.center = (margin + column * (width + margin) + (width // 2),
                                   margin + row * (height + margin) + (height // 2) + 2)
                surface.blit(text, textRect)


def openGrid(row, column):
    recursion[row][column] = True

    # open any surrounding 0s
    if(column != 0):
        grid[row][column - 1] = 2
    if(column != 9):
        grid[row][column + 1] = 2
    if(row != 9):
        grid[row + 1][column] = 2
    if(row != 0):
        grid[row - 1][column] = 2
    if(row != 0 and column != 0):
        grid[row - 1][column - 1] = 2
    if(row != 9 and column != 9):
        grid[row + 1][column + 1] = 2
    if(row != 9 and column != 0):
       grid[row + 1][column - 1] = 2
    if(row != 0 and column != 9 ):
       grid[row - 1][column + 1] = 2

    # keep opening spaces until all connected 0s are opened
    if(column != 0 and values[row][column - 1] == 0 and not(recursion[row][column-1])):
        openGrid(row, column - 1)
    if(column != 9 and values[row][column + 1] == 0 and not(recursion[row][column+1])):
        openGrid(row, column + 1)
    if(row != 9 and values[row + 1][column] == 0 and not(recursion[row+1][column])):
        openGrid(row + 1, column)
    if(row != 0 and values[row - 1][column] == 0 and not(recursion[row-1][column])):
        openGrid(row - 1, column)

def gameLost():
    for row in range(10):
        for column in range(10):
            if(values[row][column] == 9):
                text = font.render("X", True, BLACK)
                textRect = text.get_rect()
                textRect.center = (margin + column * (width + margin) + (width // 2),
                                   margin + row * (height + margin) + (height // 2) + 2)
                surface.blit(text, textRect)
    text = font.render("You Lost", True, RED, BLACK)
    textRect = text.get_rect()
    textRect.center = (510 // 2, 510 // 2)
    surface.blit(text, textRect)
                

def testWin():
    for row in range(10):
        for column in range(10):
            if(values[row][column] != 9 and grid[row][column] != 2):
                return False
    return True


###### GAME LOOP #########

first = True
        
while True:
    for event in pygame.event.get():
        # if the user closes the window, exit
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # if the user right clicks, place a flag at that location
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            column = pygame.mouse.get_pos()[0] // (width + margin)
            row = pygame.mouse.get_pos()[1] // (height + margin)
            # don't flag an open area, and unflag if already flagged
            if(grid[row][column] == 1 and not(lost)):
                grid[row][column] = 0
            elif(grid[row][column] != 2 and not(lost)):
                grid[row][column] = 1
            
        # if the user left clicks, open that location
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            column = pygame.mouse.get_pos()[0] // (width + margin)
            row = pygame.mouse.get_pos()[1] // (height + margin)
            if(first):
                first = False
                generate(row, column)
             # game over if mine selected
            if(values[row][column] == 9 and grid[row][column] != 1):
                lost = True
                gameLost()
            # don't open a flagged area, and chain open any 0s
            if(grid[row][column] != 1 and not(lost)):
                grid[row][column] = 2
                if(values[row][column] == 0):
                    openGrid(row, column)
            won = testWin()
            '''if(lost and row == 6 and (column == 3 or column == 4 or column == 5 or column == 6)):
                won = False
                lost = False
                grid = [[0 for x in range(10)] for y in range(10)]
                values = [[0 for x in range(10)] for y in range(10)]
                recursion = [[False for x in range(10)] for y in range(10)]'''
            

           
    if(won):
        lost = True
        text = font.render("YOU WON", True, GREEN, BLACK)
        textRect = text.get_rect()
        textRect.center = (510 // 2, 510 // 2)
        surface.blit(text, textRect)
        gameLost()


    if(not(lost) and not(won)):
        drawGrid(grid)
        
    clock.tick(60)
    pygame.display.update()


    
    

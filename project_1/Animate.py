import pygame
import time
import numpy as np

# open the file for reading
with open('nodePath.txt', 'r') as f:
    # read the content of the file
    content = f.read()

# split the content by blank line to get a list of matrix strings
strings = content.strip().split('\n')

# create a list of 3x3 matrices from the matrix strings
track = []
for string in strings:
    values = list(map(int, string.split()))
    state = np.array(values).reshape(3, 3)
#     print(state)
    track.append(state.T)
# track.reverse()
# initialize pygame
pygame.init()

# set the size of the game window
window_size = (300, 300)
screen = pygame.display.set_mode(window_size)

# set the title of the game window
pygame.display.set_caption("8 Puzzle Game")

# define colors
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)

# set the font
font = pygame.font.SysFont('Arial', 30)

# define the size of the puzzle grid
grid_size = 3
cell_size = 100

# define the position of the puzzle numbers
puzzle_positions = [(i % grid_size, i // grid_size) for i in range(grid_size ** 2)]

# define the position of the empty cell
empty_position = puzzle_positions[-1]



# define a function to draw the puzzle board
def draw_board():
    for i in range(grid_size):
        for j in range(grid_size):
            x = j * cell_size
            y = i * cell_size
            index = puzzle_positions.index((j, i))
            number = puzzle_numbers[index]
            if number != 0:
                pygame.draw.rect(screen, white, (x, y, cell_size, cell_size))
                text = font.render(str(number), True, black)
                text_rect = text.get_rect(center=(x+cell_size/2, y+cell_size/2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, grey, (x, y, cell_size, cell_size))

# define the main game loop
running = True

i=0
while running  :
    # handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # clear the screen
    screen.fill(grey)
    
#     update position
    if i<len(track):
        puzzle_numbers=track[i].flatten()
        i+=1
    # draw the puzzle board
    draw_board()
    time.sleep(1)
    # update the screen
    pygame.display.update()
    

# quit pygame
pygame.quit()

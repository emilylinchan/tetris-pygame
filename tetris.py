# Tetris Game
# By: Emily Chan

import pgzrun
import random

WIDTH = 875
HEIGHT = 660
game_top_x = 300
game_top_y = 85

class Tetromino:
    # Assume a 4x4 grid for each Tetromino shape with cell indices from 0 to 15
    # (indices increasing left to right and wrapping at the end of a row)
    #  0  1  2  3 
    #  4  5  6  7
    #  8  9 10 11
    # 12 13 14 15

    # Tetromino shapes
    # (top left location)
    z = [[0, 1, 5, 6], [1, 4, 5, 8]]
    l = [[0, 4, 8, 9], [2, 4, 5, 6], [0, 1, 5, 9], [0, 1, 2, 4]]
    o = [[0, 1, 4, 5]]
    s = [[1, 2, 4, 5], [0, 4, 5, 9]]
    i = [[0, 4, 8, 12], [0, 1, 2, 3]]
    j = [[0, 1, 4, 8], [0, 4, 5, 6], [1, 5, 8, 9], [0, 1, 2, 6]]
    t = [[1, 4, 5, 6], [1, 4, 5, 9], [0, 1, 2, 5], [0, 4, 5, 8]]

    shapes = [z, l, o, s, i, j, t]
        
    # x and y offsets for the first orientation of each shape
    z_offset = [1, 2]
    l_offset = [2, 1]
    o_offset = [2, 2]
    s_offset = [1, 2]
    i_offset = [3, 0]
    j_offset = [2, 1]
    t_offset = [1, 2]

    shape_offsets = [z_offset, l_offset, o_offset, s_offset, i_offset, j_offset, t_offset]

    # Tetromino colours
    red = (255, 0, 0) # Z shape
    orange = (255, 160, 0) # L shape
    yellow = (255, 255, 0) # O shape
    green = (0, 255, 0) # S shape
    cyan = (0, 255, 255) # I shape
    blue = (0, 0, 255) # J shape
    purple = (128, 0, 128) # T shape

    colours = [red, orange, yellow, green, cyan, blue, purple]
    
    def __init__(self, x, y):
        '''Constructor: creates the Tetromino object'''
        # get a random index value for the shapes and colours list
        rand_idx = random.randint(0, len(Tetromino.shapes) - 1)
        
        self.x = x
        self.y = y
        self.shape = Tetromino.shapes[rand_idx]
        self.colour = Tetromino.colours[rand_idx]
        self.rotation = 0 # integer represents the index value that corresponds to a particular orientation of the shape
        
        self.x_offset = Tetromino.shape_offsets[rand_idx][0]
        self.y_offset = Tetromino.shape_offsets[rand_idx][1]
        
    def rotate(self):
        '''Rotate orientation of shape by 90 degrees'''
        # increase the rotation attribute by 1 and wrap back to 0 if the length of the particular shape is exceeded
        self.rotation = (self.rotation + 1) % (len(self.shape))
        # swap offset values
        self.x_offset, self.y_offset = self.y_offset, self.x_offset
        
    def grid(self):
        '''Numerical representation of a shape's particular orientation
           Returns: list
        '''
        return self.shape[self.rotation]
    
    
class Tetris:
    def __init__(self, row, col):
        '''Constructor: creates the Tetris object'''
        self.state = "start"
        self.score = 0
        self.lines_cleared = 0
        self.until_next_level = 10
        self.level = 1
        self.speed = 30
        
        self.tetromino = None
        self.next = None
        
        self.block_size = 25
        self.row = row 
        self.col = col
        self.height = row * self.block_size
        self.width = col * self.block_size
        
        self.grid = []
        for i in range(row):
            line = []
            for j in range(col):
                line.append(0)
            self.grid.append(line)
    
    def new_tetromino(self):
        '''Assign new current and next tetrominoes'''
        # create 2 tetromino objects at the start of the game: 1st = current, 2nd = next
        if self.tetromino == None:
            self.tetromino = Tetromino(game_top_x + self.width // 2 - self.block_size, game_top_y)
            self.next = Tetromino(700, 150)
            
        # swap the current tetromino with the next and generate a new next tetromino
        else:
            self.tetromino = self.next
            self.tetromino.x = game_top_x + self.width // 2 - self.block_size
            self.tetromino.y = game_top_y
            self.next = Tetromino(700, 150)

    def collision(self):
        '''Check if the current tetromino makes a collision
           Returns: boolean
        '''
        collision = False
        for i in range(4): # row of 4x4 block
            for j in range(4): # col of 4x4 block
                cell = i * 4 + j # integer from 0 to 15
                if cell in self.tetromino.grid():
                    # location of block on game board
                    row = (self.tetromino.y - game_top_y) // self.block_size
                    col = (self.tetromino.x - game_top_x) // self.block_size
                    # check if the tetromino makes a collision with the sides or bottom of the game board
                    if self.tetromino.x < game_top_x or \
                       self.tetromino.x + (4 - self.tetromino.x_offset) * self.block_size > game_top_x + self.width or \
                       self.tetromino.y + (4 - self.tetromino.y_offset) * self.block_size > game_top_y + self.height:
                        collision = True
                    # check if the tetromino makes a collision with another block currently on the game board
                    elif self.grid[row + i][col + j] > 0:
                        collision = True

        return collision
    
    def lock(self):
        '''Lock the current tetromino into place after a collision'''
        for i in range(4): # row of 4x4 block
            for j in range(4): # col of 4x4 block
                cell = i * 4 + j # integer from 0 to 15
                if cell in self.tetromino.grid():
                    # location of block on game board
                    row = (self.tetromino.y - game_top_y + i * self.block_size )// self.block_size
                    col = (self.tetromino.x - game_top_x + j * self.block_size) // self.block_size
                    # add the location of the tetromino to the 2D game board list
                    self.grid[row][col] = Tetromino.colours.index(self.tetromino.colour) + 1           
        # check if a row was completed
        self.clear_lines()
        # spawn a new tetromino at the top of the game board
        self.new_tetromino()  
        
    def clear_lines(self):
        '''Clear any rows that are completed and update score accordingly'''
        cleared = 0
        for row in range(self.row):
            empty = 0
            for col in range(self.col):
                # check if the cell is empty
                if self.grid[row][col] == 0:
                    empty += 1
            # empty is zero if a row is completely filled    
            if empty == 0:
                cleared += 1
                # move all of the blocks above the cleared line down 1 row
                for row in range(row, 1, -1):
                    for col in range(self.col):
                        self.grid[row][col] = self.grid[row - 1][col]
        
        # update attributes according to how many lines were cleared
        self.lines_cleared += cleared
        self.until_next_level -= cleared
        self.score += (cleared ** 2) * 100
        
        # increase level every time 10 lines are cleared
        if self.until_next_level <= 0:
            self.level += 1
            self.until_next_level = 10
        
    def rotate(self):
        '''Rotate the orientation of the current tetromino by 90 degrees'''
        self.tetromino.rotate()
        # prevent the current tetromino from rotating if it creates an invalid move
        if self.collision():
            # rotate the tetromino 360 degrees back to its original orientation
            for i in range(1, len(self.tetromino.shape)):
                self.tetromino.rotate()

    def move_down(self):
        '''Move the current tetromino down a row'''
        old_y = self.tetromino.y
        self.tetromino.y += self.block_size
        # prevent tetrominoes from continuing to move down if they collide with the bottom of the game board or another tetromino
        if self.collision():
            # end game if tetrominoes reach the top of the game board
            if old_y == game_top_y:
                self.state = "gameover"
            # lock tetromino into place    
            self.tetromino.y = old_y
            self.lock()
    
    def move_lateral(self, direction):
        '''Move the current tetromino across to the column in the according direction
           Args:
               direction (int): absolute value of 1, positive = right, negative = left
        '''
        old_x = self.tetromino.x
        self.tetromino.x += self.block_size * direction
        # prevent the current tetromino from continuing to move laterally if it collides with anything
        if self.collision():
            self.tetromino.x = old_x
            
# buttons         
options = Rect((340, 440), (200, 100))
easy = Rect((250, 175), (375, 100))
medium = Rect((250, 325), (375, 100))
hard = Rect((250, 475), (375, 100))
back = Rect((30, 25), (100, 50))

mode = "EASY"

def draw():
    '''Game Loop: constantly redraws the game window'''
    # start screen
    if game.state == "start":
        screen.clear()
        screen.blit("tetris_title.png", (0, 0))
        screen.draw.text("Press 'SPACE' to start!", midtop = (WIDTH//2 + 23, HEIGHT//2 + 40), fontsize = 60, color = "black")
        screen.draw.text("Press 'SPACE' to start!", midtop = (WIDTH//2 + 20, HEIGHT//2 + 44), fontsize = 60, color = "white")
        
        # display options button
        screen.draw.filled_rect(options, color = "black")
        screen.draw.rect(Rect((345, 445), (190, 90)), color = "white")
        screen.draw.text("OPTIONS", midtop = (440, 475), fontsize = 35, color = "white")
        
        # display mode
        screen.draw.text(f"Mode: {mode}", bottomright = (WIDTH - 40, HEIGHT - 30), fontsize = 30, color = "white")
    
    # options screen
    elif game.state == "options":
        screen.clear()
        screen.draw.text("-=[ SELECT MODE ]=-", midtop = (WIDTH//2, 80), fontsize = 50, color = "white")
        
        # display different mode buttons
        screen.draw.filled_rect(easy, (0,179,0))
        screen.draw.filled_rect(medium, (255,181,0))
        screen.draw.filled_rect(hard, (188, 0, 0))
        screen.draw.rect(Rect((255, 180), (365, 90)), color = "white")
        screen.draw.rect(Rect((255, 330), (365, 90)), color = "white")
        screen.draw.rect(Rect((255, 480), (365, 90)), color = "white")
        screen.draw.text("EASY", center = (WIDTH//2, 225), fontsize = 45, color = "white")
        screen.draw.text("MEDIUM", center = (WIDTH//2, 375), fontsize = 45, color = "white")
        screen.draw.text("HARD", center = (WIDTH//2, 525), fontsize = 45, color = "white")
        
        # display back button
        screen.draw.filled_rect(back, color = "light gray")
        screen.draw.rect(Rect((33, 28), (94, 44)), color = "black")
        screen.draw.text("BACK", center = (80, 50), fontsize = 25, color = "black")
        
    # gameover screen
    elif game.state == "gameover":
        screen.draw.text("GAME OVER", midtop = (WIDTH//2 + 3, HEIGHT//2 - 77), fontsize = 90, color = "red")
        screen.draw.text("GAME OVER", midtop = (WIDTH//2 - 3, HEIGHT//2 - 83), fontsize = 90, color = "red")
        screen.draw.text("GAME OVER", midtop = (WIDTH//2, HEIGHT//2 - 80), fontsize = 90, color = "white")
        screen.draw.text("Press 'ESCAPE' to restart!", midtop = (WIDTH//2 + 3, HEIGHT//2 + 3), fontsize = 50, color = "red")
        screen.draw.text("Press 'ESCAPE' to restart!", midtop = (WIDTH//2 - 3, HEIGHT//2 - 3), fontsize = 50, color = "red")
        screen.draw.text("Press 'ESCAPE' to restart!", midtop = (WIDTH//2, HEIGHT//2), fontsize = 50, color = "white")
    
    # game is being played
    else:
        screen.clear()
        # display current game stats
        screen.draw.text("SCORE", (50, 75), fontsize = 25, color = "white")
        screen.draw.text(f"{game.score}", (50, 100), fontsize = 50, color = "light blue")
        screen.draw.text("LINES CLEARED", (50, 200), fontsize = 25, color = "white")
        screen.draw.text(f"{game.lines_cleared}", (50, 225), fontsize = 50, color = "light blue")
        screen.draw.text("LEVEL", (50, 325), fontsize = 25, color = "white")
        screen.draw.text(f"{game.level}", (50, 350), fontsize = 50, color = "light blue")
        
        # display next tetromino
        screen.draw.text("NEXT", (650, 75), fontsize=24, color="white")
        next_box = Rect((650, 100), (150, 180))
        screen.draw.rect(next_box, color = "light blue")
        
        # game board
        outline = Rect((game_top_x - 10, game_top_y - 10), (game.width + 20, game.height + 20))
        screen.draw.filled_rect(outline, (107, 107, 107))
        
        # draw locked tetrominoes on the game board
        for i in range(game.row):
            for j in range(game.col):
                cell_value = game.grid[i][j]
                cell_location = Rect((game_top_x + game.block_size * j, game_top_y + game.block_size * i),
                                     (game.block_size, game.block_size))
                # cell filled by a tetromino block
                if cell_value > 0:
                    screen.draw.filled_rect(cell_location, Tetromino.colours[cell_value-1])
                # cell not filled by a tetromino block
                else:
                    screen.draw.filled_rect(cell_location, (0,0,0))
        
        # draw current tetromino on the game board
        if game.tetromino != None:
            for row in range(4):
                for col in range(4):
                    # 4x4 grid for each Tetromino shape with cell indices from 0 to 15
                    cell = row * 4 + col
                    if cell in game.tetromino.grid():
                        rect = Rect((game.tetromino.x + game.block_size * col, game.tetromino.y + game.block_size * row),
                                    (game.block_size, game.block_size))
                        screen.draw.filled_rect(rect, game.tetromino.colour)
                        
        # draw next tetromino on the game board
        if game.next != None:
            for row in range(4):
                for col in range(4):
                    # 4x4 grid for each Tetromino shape with cell indices from 0 to 15
                    cell = row * 4 + col
                    if cell in game.next.grid():
                        rect = Rect((game.next.x + game.block_size * col, game.next.y + game.block_size * row),
                                    (game.block_size, game.block_size))
                        screen.draw.filled_rect(rect, game.next.colour)
      
        # draw vertical lines for game grid
        for col in range(1, game.col):
            x = game_top_x + (game.block_size * col)
            y = game_top_y
            screen.draw.line((x, y), (x, y + game.height), (255, 255, 255))
            
        # draw horizontal lines for game grid
        for row in range(1, game.row):
            x = game_top_x
            y = game_top_y + (game.block_size * row)
            screen.draw.line((x, y), (x + game.width, y), (255, 255, 255))


def update():
    '''Game Loop: updates program to deal with game logic (called 60 times/ second)'''
    global counter
    
    # game hasn't started yet
    if game.state == "start":
        counter = 0
    
    # game is currently being played
    elif game.state == "play":
        counter += 1
        # initiate the game
        if game.tetromino == None:
            game.new_tetromino()
        # the current tetromino descends at a constant rate according the the game level
        if counter % (game.speed // game.level) == 0:
            game.move_down()
        # speed up the rate at which the current tetromino descends    
        if keyboard.DOWN:
            game.move_down()
        
            
def on_key_down(key):
    '''Event Handler: called every time a key is pressed
       Args:
           key: indicates which key was pressed
    '''
    global game
    
    if game.state == "start":
        # press space to begin the game
        if key == keys.SPACE:
            game.state = "play"
    
    elif game.state == "gameover":
        # press escape to reset the game
        if key == keys.ESCAPE:
            game = Tetris(20, 10)
    
    elif game.state == "play":
        # key controls during the game
        if key == keys.UP:
            game.rotate()
        if key == keys.LEFT:
            game.move_lateral(-1)
        if key == keys.RIGHT:
            game.move_lateral(1)


def on_mouse_down(pos):
    '''Event Handler: called every time the mouse is clicked
       Args:
           pos (tuple): x and y coordinates of the mouse pointer
    '''
    global mode
    
    if game.state == "start":
        # check if the options button was clicked on the start screen
        if options.collidepoint(pos):
            game.state = "options"
            
    elif game.state == "options":
        # check if any of the buttons were clicked on the options screen and return to start screen if so
        if easy.collidepoint(pos):
            game.speed = 30
            mode = "EASY"
            game.state = "start"
        elif medium.collidepoint(pos):
            game.speed = 20
            mode = "MEDIUM"
            game.state = "start"
        elif hard.collidepoint(pos):
            game.speed = 10
            mode = "HARD"
            game.state = "start"
        elif back.collidepoint(pos):
            game.state = "start"


game = Tetris(20, 10)
counter = 0

pgzrun.go()


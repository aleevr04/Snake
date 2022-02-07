import pygame, sys, random
from pygame.math import Vector2

class Apple:
    def __init__(self):
        self.spawn()
    
    def draw(self):
        self.rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        
        pygame.draw.rect(screen, RED, self.rect)
    
    def spawn(self):
        self.x = random.randint(0, cell_num - 1)
        self.y = random.randint(0, cell_num - 1)
        self.pos = Vector2(self.x, self.y)


class Snake:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = RIGHT
        self.new_block = False
    
    def draw(self):
        for block in self.body:
            block_rect = pygame.Rect(block.x * cell_size, block.y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, BLUE, block_rect)
    
    def move(self):
        # If we are creating a new block
        # we do the same thing as moving normal
        # except we dont remove the last block
        if self.new_block:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            
            # We set this attribute back to False
            # so the snake doesn't add a new block in every frame
            self.new_block = False
        
        else:
            # We take the entire body of the snake
            # except of the last one, so we remove it
            body_copy = self.body[:-1]
            
            # We take the actual head and add to it the current direction
            # This will be the new head
            new_head = body_copy[0] + self.direction
            
            # We append the new head to the new body we are making
            body_copy.insert(0, new_head)
            
            # We assing the actual head to the new one we have created
            self.body = body_copy[:]
    

class Game:
    deaths = 0
    
    def __init__(self):
        self.snake = Snake()
        self.apple = Apple()
        
        self.score = 0
        
    def check_collisions(self):
        # We create a list of all the positions where there is no snake
        possible_spawns = []
        
        for x in range(0, cell_num - 1):
            for y in range(0, cell_num - 1):
                if Vector2(x, y) not in self.snake.body:
                    possible_spawns.append(Vector2(x, y))
                    
        # If the head of the snake is in the same position as the apple...
        if self.snake.body[0] == self.apple.pos:
            # We position the apple in a random pos of all the possible ones
            self.apple.pos = random.choice(possible_spawns)
            # We add a new block to the snake
            self.snake.new_block = True
            self.score += 1
                      
    def check_fail(self):
        # Checking X and Y Collision
        if not (0 <= self.snake.body[0].x < cell_num) or not(0 <= self.snake.body[0].y < cell_num):
            self.__init__()
            self.deaths += 1
        
        # Checking if the snake collide with itself
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.__init__()
                self.deaths += 1
    
    def draw_score(self):
        text = font.render(f'Score: {self.score}          Deaths: {self.deaths}', True, WHITE)
        text_rect = text.get_rect(center = (screen_size/2, 30))
        
        screen.blit(text, text_rect)
    
    def draw_elements(self):
        screen.fill(GREEN)
        self.apple.draw()
        self.snake.draw()
        self.draw_score()
    
    def update(self):
        self.snake.move()
        self.check_collisions()
        self.check_fail()
        
# General Setup
pygame.init()
clock = pygame.time.Clock()

# Colors
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GREEN = (50,205,50)
PINK = (255, 105, 180)
BLUE = (0, 0, 255)

# Font
font = pygame.font.Font('freesansbold.ttf', 24, bold = True)

# Directions
UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
RIGHT = Vector2(1, 0)
LEFT = Vector2(-1, 0)

# User Events
SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 120)

# Grid Settings
cell_size = 30
cell_num = 20

# Game Window
screen_size = cell_size * cell_num
screen = pygame.display.set_mode((screen_size, screen_size))
pygame.display.set_caption('Snake Game')

# Game Object
game = Game()

# Game Loop
while True:
    # Handling Events
    for event in pygame.event.get():
        # We close the window
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # The screen updates every 120 ms
        if event.type == SCREEN_UPDATE:
            game.update()
        # Controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game.snake.direction != DOWN:
                game.snake.direction = UP
            if event.key == pygame.K_DOWN and game.snake.direction != UP:
                game.snake.direction = DOWN
            if event.key == pygame.K_RIGHT and game.snake.direction != LEFT:
                game.snake.direction = RIGHT
            if event.key == pygame.K_LEFT and game.snake.direction != RIGHT:
                game.snake.direction = LEFT
    
    game.draw_elements()
    
    pygame.display.flip()
    clock.tick(60)
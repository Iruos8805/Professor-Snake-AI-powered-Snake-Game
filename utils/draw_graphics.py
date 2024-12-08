import pygame
import pygame_gui
import os
import random
from .config_constants import *
from .snake_algorithms import *

# Increase window size for more space
screen = pygame.display.set_mode((SCREEN_SIZE + 800, SCREEN_SIZE + 200))  # Increased width
Clock = pygame.time.Clock()
apple = pygame.image.load("assets/apple.png").convert_alpha()
stone = pygame.image.load("assets/stone.png").convert_alpha()

# Define constants
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
current_algorithm = None

# Try loading the background image with error handling
try:
    background_image = pygame.image.load("assets/back.png")  # Adjust this path
    background_image = pygame.transform.scale(background_image, (SCREEN_SIZE + 800, SCREEN_SIZE + 200))  # Scale to fit window size
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = pygame.Surface((SCREEN_SIZE + 800, SCREEN_SIZE + 200))  
    background_image.fill((0, 0, 0))  # Fallback

# Initialize Pygame and the GUI manager
pygame.init()
manager = pygame_gui.UIManager((SCREEN_SIZE + 800, SCREEN_SIZE + 200))  # Updated window size

# Font for the score display
font_path = "assets/PixelifySans-VariableFont_wght.ttf"
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 48)
else:
    print(f"Font file not found at {font_path}, using default font.")
    font = pygame.font.Font(None, 48)

# Button initialization for algorithms and control
button_labels = ['BFS', 'A*', 'DFS', 'Greedy BFS', 'Iterative Deepening DFS', 'Bidirectional Search', 'Quit', 'Restart', 'Toggle Auto/Manual']
button_functions = [bfs, a_star, dfs, greedy_bfs, iddfs, bidirectional_search, 'quit', 'restart', 'toggle_mode']

button_width = 180
button_height = 50
button_margin = 10
buttons_per_row = 2
start_x = SCREEN_SIZE + 220  # Padding from the right
start_y = 100
buttons = []

# Initialize game variables
score = 0
is_auto_mode = True  # Start with automatic mode
dragging = False
last_pos = None
food = None  # Initially, no food is placed
obstacles = set()

# Function to enumerate buttons
def enumerate_buttons():
    global buttons
    buttons.clear()  # Clear previous buttons to avoid duplicates
    for i, label in enumerate(button_labels):
        col = i % buttons_per_row
        row = i // buttons_per_row
        button_x = start_x + col * (button_width + button_margin)
        button_y = start_y + row * (button_height + button_margin)
        
        buttons.append(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (button_width, button_height)),
                text=label,
                manager=manager,
                object_id="#main_button"
            )
        )
        # buttons.append(button)

# Function to draw the grid
def draw_grid():
    grid_x = 160
    grid_y = (SCREEN_SIZE + 200 - GRID_HEIGHT) // 2
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (grid_x + x * CELL_SIZE, grid_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (grid_x + x * CELL_SIZE, grid_y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

body_br = pygame.image.load("assets/body_br.png").convert_alpha()
body_bl = pygame.image.load("assets/body_bl.png").convert_alpha()
body_tl = pygame.image.load("assets/body_tl.png").convert_alpha()
body_tr = pygame.image.load("assets/body_tr.png").convert_alpha()

body_horizontal = pygame.image.load("assets/body_horizontal.png").convert_alpha()
body_vertical = pygame.image.load("assets/body_vertical.png").convert_alpha()

head_down = pygame.image.load("assets/head_down.png").convert_alpha()
head_left = pygame.image.load("assets/head_left.png").convert_alpha()
head_right = pygame.image.load("assets/head_right.png").convert_alpha()
head_up = pygame.image.load("assets/head_up.png").convert_alpha()

tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()
tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()

def update_graphics(snake):
    if len(snake) < 2:
        return head_right, tail_right

    tail_relation = (snake[-1][0] - snake[-2][0], snake[-1][1] - snake[-2][1])
    
    if tail_relation == (0, 1): 
        tail = head_right
    elif tail_relation == (0, -1): 
        tail = head_left
    elif tail_relation == (1, 0): 
        tail = head_down
    elif tail_relation == (-1, 0): 
        tail = head_up
    else:
        tail = head_right

    head_relation = (snake[1][0] - snake[0][0], snake[1][1] - snake[0][1])

    if head_relation == (0, 1):
        head = tail_left
    elif head_relation == (0, -1):
        head = tail_right
    elif head_relation == (1, 0):
        head = tail_up
    elif head_relation == (-1, 0):
        head = tail_down
    else:
        head = tail_right

    return head, tail

def draw_snake(snake):
    if not snake:
        return
        
    head, tail = update_graphics(snake)
    
    grid_x = 160
    grid_y = (SCREEN_SIZE + 200 - GRID_HEIGHT) // 2
    
    for index, segment in enumerate(snake):
        # Calculate the position based on the segment
        x_pos = segment[1] * CELL_SIZE + grid_x
        y_pos = segment[0] * CELL_SIZE + grid_y  # Ensure the Y position is directly aligned
        
        block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        
        if index == 0:
            screen.blit(head, block_rect)  # Draw head
        elif index == len(snake) - 1:
            screen.blit(tail, block_rect)  # Draw tail
        elif len(snake) > 2:
            previous_block = snake[index + 1]
            next_block = snake[index - 1]
            prev_direction = (segment[0] - previous_block[0], segment[1] - previous_block[1])
            next_direction = (segment[0] - next_block[0], segment[1] - next_block[1])
            
            if prev_direction[1] == next_direction[1]:
                screen.blit(body_vertical, block_rect)  # Draw vertical body
            elif prev_direction[0] == next_direction[0]:
                screen.blit(body_horizontal, block_rect)  # Draw horizontal body
            else:
                if (prev_direction[1] == -1 and next_direction[0] == 1) or (prev_direction[0] == 1 and next_direction[1] == -1):
                    screen.blit(body_br, block_rect)  # Draw bottom-right corner body
                elif (prev_direction[1] == -1 and next_direction[0] == -1) or (prev_direction[0] == -1 and next_direction[1] == -1):
                    screen.blit(body_tr, block_rect)  # Draw top-right corner body
                elif (prev_direction[1] == 1 and next_direction[0] == 1) or (prev_direction[0] == 1 and next_direction[1] == 1):
                    screen.blit(body_bl, block_rect)  # Draw bottom-left corner body
                elif (prev_direction[1] == 1 and next_direction[0] == -1) or (prev_direction[0] == -1 and next_direction[1] == 1):
                    screen.blit(body_tl, block_rect)  # Draw top-left corner body


# Function to draw food
def draw_food(food):
    grid_x = 160
    grid_y = (SCREEN_SIZE + 200 - GRID_HEIGHT) // 2
    size = CELL_SIZE - 6 + (3 * (pygame.time.get_ticks() % 1000) // 500)
    x, y = food[1] * CELL_SIZE + grid_x + 1, food[0] * CELL_SIZE + grid_y + 1
    tup = (x, y, size, size)
    screen.blit(apple, tup)

# Function to draw obstacles
def draw_obstacles(obstacles):
    grid_x = 160
    grid_y = (SCREEN_SIZE + 200 - GRID_HEIGHT) // 2
    for obstacle in obstacles:
        x, y = obstacle[1] * CELL_SIZE + grid_x, obstacle[0] * CELL_SIZE + grid_y
        tup  =(x, y, CELL_SIZE, CELL_SIZE)
        screen.blit(stone, tup)
# Function to draw the path
def draw_path(path):
    grid_x = 160
    grid_y = (SCREEN_SIZE + 200 - GRID_HEIGHT) // 2
    if path:
        for step in path[:-1]:
            x, y = step[1] * CELL_SIZE + grid_x + 2, step[0] * CELL_SIZE + grid_y + 2
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)

# Function to draw the score
def draw_score():
    score_text = font.render(f"SCORE: {score:03d}", True, WHITE)
    screen.blit(score_text, (SCREEN_SIZE - 260, 20))

# Game over screen
def game_over_screen(message="Game Over!"):
    screen.fill((30, 30, 30))
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    game_loop(Clock)

# Function to automatically place food if none exists
def place_food_if_needed():
    global food
    if food is None:
        food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
        while food in obstacles:  # Ensure food doesn't spawn inside obstacles
            food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))

# Main game loop
def game_loop(clock):
    global dragging, last_pos, score, is_auto_mode, food  # Add 'food' to the global variables
    screen.blit(background_image, (0, 0))
    dragging = False
    running = True
    snake = [(10, 10)]
    obstacles = set()
    algorithm = bfs
    previous_path = []
    enumerate_buttons()

    while running:
        screen.blit(background_image, (0, 0))
        draw_grid()
        draw_snake(snake)
        if food:  # Make sure food exists before drawing it
            draw_food(food)
        draw_obstacles(obstacles)

        # Handle game logic for automatic mode
        if is_auto_mode:
            place_food_if_needed()  # Ensure food is placed in auto mode

            snake_body = set(snake[:-1])  # Exclude last segment (tail)
            path = algorithm(snake[-1], food, obstacles | snake_body)

            if path != previous_path:
                previous_path = path
                draw_path(path)

            # Move the snake along the path
            if path:
                next_move = path[1]
                if next_move in snake_body:
                    game_over_screen()
                    pygame.time.wait(1500)
                    continue

                snake.append(next_move)
                if next_move == food:
                    score += 10
                    food = None  # Remove the food once eaten
                else:
                    snake.pop(0)
            else:
                game_over_screen("Game Over: No path to food!")
                pygame.display.flip()
                pygame.time.wait(2000)

        # Handle manual mode
        else:
            if food:
                # Find the path manually if food is present
                snake_body = set(snake[:-1])  # Exclude last segment (tail)
                path = algorithm(snake[-1], food, obstacles | snake_body)

                if path:
                    next_move = path[1]
                    if next_move == food:
                        score += 10
                        food = None  # Remove the food once eaten
                    else:
                        snake.append(next_move)
                        snake.pop(0)
                else:
                    game_over_screen("Game Over: No path to food!")
                    pygame.display.flip()
                    pygame.time.wait(2000)

        # Draw the score
        draw_score()

        # Handle events and UI updates
        time_delta = clock.tick(30) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            manager.process_events(event)
            if event.type == pygame_gui.UI_BUTTON_PRESSED:
                button_index = buttons.index(event.ui_element)
                clicked_function = button_functions[button_index]

                if clicked_function == 'quit':
                    exit()
                elif clicked_function == 'restart':
                    score = 0
                    game_loop(clock)
                elif clicked_function == 'toggle_mode':
                    is_auto_mode = not is_auto_mode  # Toggle between auto and manual
                else:
                    algorithm = clicked_function
                    previous_path = []
                    path = algorithm(snake[-1], food, obstacles | set(snake[:-1]))  # Include snake body as obstacle
                    draw_path(path)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    x, y = pygame.mouse.get_pos()
                    grid_pos = (y // CELL_SIZE, x // CELL_SIZE)
                    if grid_pos not in snake and grid_pos != food:
                        if grid_pos[0] < GRID_SIZE and grid_pos[1] < GRID_SIZE:
                            obstacles.add(grid_pos)
                    last_pos = grid_pos
                elif event.button == 3 and not is_auto_mode:
                    # Right-click in manual mode to place food only if within grid bounds
                    x, y = pygame.mouse.get_pos()
                    grid_pos = (y // CELL_SIZE, x // CELL_SIZE)
                    if 0 <= grid_pos[0] < GRID_SIZE and 0 <= grid_pos[1] < GRID_SIZE:  # Ensure within grid
                        food = grid_pos

            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                grid_pos = (y // CELL_SIZE, x // CELL_SIZE)
                if grid_pos != last_pos:
                    if grid_pos not in snake and grid_pos != food:
                        if grid_pos[0] < GRID_SIZE and grid_pos[1] < GRID_SIZE:
                            obstacles.add(grid_pos)
                            last_pos = grid_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    last_pos = None

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()

    pygame.quit()



# Run the game loop
game_loop(Clock)

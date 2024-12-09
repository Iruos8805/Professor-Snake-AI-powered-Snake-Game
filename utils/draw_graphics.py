import pygame
import pygame_gui
from .config_constants import *
import random
from .snake_algorithms import *
import os

screen = pygame.display.set_mode((SCREEN_SIZE + 800, SCREEN_SIZE + 200))

Clock = pygame.time.Clock()
apple = pygame.image.load("assets/apple.png").convert_alpha()
stone = pygame.image.load("assets/stone.png").convert_alpha()

screen = pygame.display.set_mode((SCREEN_SIZE + 800, SCREEN_SIZE + 200))
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE
current_algorithm = None
score = 0
score_label = None

pygame.init()
manager = pygame_gui.UIManager((SCREEN_SIZE + 800, SCREEN_SIZE + 200), 'utils/theme.json')

try:
    background_image = pygame.image.load("assets/back.png")
    background_image = pygame.transform.scale(background_image, (SCREEN_SIZE + 800, SCREEN_SIZE + 200))
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_image = pygame.Surface((SCREEN_SIZE + 800, SCREEN_SIZE + 200))  
    background_image.fill((0, 0, 0))

font_path = "Pixelify_Sans/PixelifySans-VariableFont_wght.ttf"
if os.path.exists(font_path):
    font = pygame.font.Font(font_path, 48)
else:
    print(f"Font file not found at {font_path}, using default font.")
    font = pygame.font.Font(None, 48)

button_labels = ['BFS', 'A*', 'DFS', 'Greedy BFS', 'Iterative Deepening DFS', 'Bidirectional Search', 'Quit', 'Restart']
button_functions = [bfs, a_star, dfs, greedy_bfs, iddfs, bidirectional_search, 'quit', 'restart']
buttons = []

body_br = pygame.image.load("assets/body_br.png").convert_alpha()
body_bl = pygame.image.load("assets/body_bl.png").convert_alpha()
body_tl = pygame.image.load("assets/body_tl.png").convert_alpha()
body_tr = pygame.image.load("assets/body_tr.png").convert_alpha()

body_horizontal = pygame.image.load("assets/body_horizontal.png").convert_alpha()
body_vertical = pygame.image.load("assets/body_vertical.png").convert_alpha()

head_up = pygame.image.load("assets/head_down.png").convert_alpha()
head_right = pygame.image.load("assets/head_left.png").convert_alpha()
head_left = pygame.image.load("assets/head_right.png").convert_alpha()
head_down = pygame.image.load("assets/head_up.png").convert_alpha()

tail_down = pygame.image.load("assets/tail_down.png").convert_alpha()
tail_left = pygame.image.load("assets/tail_left.png").convert_alpha()
tail_right = pygame.image.load("assets/tail_right.png").convert_alpha()
tail_up = pygame.image.load("assets/tail_up.png").convert_alpha()

START_X = GRID_WIDTH + 270

def load_obstacles_from_file(file_path):
    global obstacles
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()

        obstacles = set()

        for row_idx, line in enumerate(lines):
            line = line.strip()
            for col_idx, char in enumerate(line):
                if char == '#':
                    if row_idx < GRID_SIZE and col_idx < GRID_SIZE:
                        obstacles.add((row_idx, col_idx))
                    else:
                        print(f"Obstacle invalid!!")
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except Exception as e:
        print(f"Error loading obstacles: {e}")

def highlight_current_algorithm():
    for button in buttons:
        if button.text == current_algorithm:
            button._set_active()
        else:
            button._set_inactive()

def enumerate_buttons():
    for i, label in enumerate(button_labels):
        col = i % BUTTONS_PER_ROW
        row = i // BUTTONS_PER_ROW
        button_x = START_X + col * (BUTTON_WIDTH + BUTTON_MARGIN)
        button_y = START_Y + row * (BUTTON_HEIGHT + BUTTON_MARGIN)

        button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((button_x, button_y), (BUTTON_WIDTH, BUTTON_HEIGHT)),
            text=label,
            manager=manager,
            object_id=f"#button"
        )
        buttons.append(button)

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (GRID_OFFSET_X + x * CELL_SIZE, GRID_OFFSET_Y + y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def update_graphics(snake):
    if len(snake) < 2:
        return head_right, tail_right

    tail_relation = (snake[-1][0] - snake[-2][0], snake[-1][1] - snake[-2][1])
    
    if tail_relation == (0, 1): 
        tail = head_left
    elif tail_relation == (0, -1): 
        tail = head_right
    elif tail_relation == (1, 0): 
        tail = head_up
    elif tail_relation == (-1, 0): 
        tail = head_down
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
    
    for index, segment in enumerate(snake):
        x_pos = int(segment[1] * CELL_SIZE)
        y_pos = int(segment[0] * CELL_SIZE)
        block_rect = pygame.Rect(GRID_OFFSET_X + x_pos, GRID_OFFSET_Y + y_pos, CELL_SIZE, CELL_SIZE)
        
        if index == 0:
            screen.blit(head, block_rect)
        elif index == len(snake) - 1:
            screen.blit(tail, block_rect)
        elif len(snake) > 2:
            previous_block = snake[index + 1]
            next_block = snake[index - 1]
            prev_direction = (segment[0] - previous_block[0], segment[1] - previous_block[1])
            next_direction = (segment[0] - next_block[0], segment[1] - next_block[1])
            
            if prev_direction[1] == next_direction[1]:
                screen.blit(body_vertical, block_rect)
            elif prev_direction[0] == next_direction[0]:
                screen.blit(body_horizontal, block_rect)
            else:
                if (prev_direction[1] == -1 and next_direction[0] == 1) or (prev_direction[0] == 1 and next_direction[1] == -1):
                    screen.blit(body_br, block_rect)
                elif (prev_direction[1] == -1 and next_direction[0] == -1) or (prev_direction[0] == -1 and next_direction[1] == -1):
                    screen.blit(body_tr, block_rect)
                elif (prev_direction[1] == 1 and next_direction[0] == 1) or (prev_direction[0] == 1 and next_direction[1] == 1):
                    screen.blit(body_bl, block_rect)
                elif (prev_direction[1] == 1 and next_direction[0] == -1) or (prev_direction[0] == -1 and next_direction[1] == 1):
                    screen.blit(body_tl, block_rect)

def draw_food(food):
    size = CELL_SIZE - 6 + (3 * (pygame.time.get_ticks() % 1000) // 500)
    x, y = food[1] * CELL_SIZE + 1, food[0] * CELL_SIZE + 1
    fruit_rect = (GRID_OFFSET_X + x, GRID_OFFSET_Y + y, size, size)
    screen.blit(apple, fruit_rect)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE
        stone_rect = (GRID_OFFSET_X + x, GRID_OFFSET_Y + y, CELL_SIZE, CELL_SIZE)
        screen.blit(stone, stone_rect)

def draw_path(path):
    if path:
        for step in path[1:-1]:
            x = GRID_OFFSET_X + step[1] * CELL_SIZE + 2
            y = GRID_OFFSET_Y + step[0] * CELL_SIZE + 2
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)

def game_over_screen(message="Game Over!"):
    screen.fill((30, 30, 30))
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(GRID_OFFSET_X + GRID_WIDTH // 2, GRID_OFFSET_Y + GRID_HEIGHT // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    game_loop(Clock)

def draw_score():
    score_text = font.render(f"SCORE: {score:03d}", True, WHITE)
    text_width, text_height = score_text.get_size()
    padding = 20
    score_rect = pygame.Rect(SCREEN_SIZE - text_width - padding, 20, text_width + 2 * padding, text_height + padding)
    border_radius = 15
    border_thickness = 3
    pygame.draw.rect(screen, (0, 0, 0), score_rect, border_radius=border_radius)
    pygame.draw.rect(screen, (255, 0, 0), score_rect, border_radius=border_radius, width=border_thickness)
    screen.blit(score_text, (SCREEN_SIZE - text_width - padding + padding, 20 + (padding // 2)))

def game_loop(clock, obstacle_file=None):
    global dragging, last_pos, current_algorithm, food, score, obstacles
    dragging = False
    running = True
    snake = [(10, 10)]
    food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
    obstacles = set()

    # Load obstacles from file if provided
    if obstacle_file:
        load_obstacles_from_file(obstacle_file)

    algorithm = bfs
    previous_path = []
    enumerate_buttons()

    while running:
        current_algorithm = button_labels[button_functions.index(algorithm)]
        screen.blit(background_image, (0, 0))
        highlight_current_algorithm()
        draw_grid()
        draw_snake(snake)
        draw_food(food)
        draw_obstacles(obstacles)

        snake_body = set(snake[:-1])
        path = algorithm(snake[-1], food, obstacles | snake_body)

        if path != previous_path:
            previous_path = path
            draw_path(path)

        if path:
            next_move = path[1]
            if next_move in snake_body:
                game_over_screen()
                pygame.time.wait(1500)
                continue

            snake.append(next_move)
            if next_move == food:
                score += 10
                food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
                while food in obstacles or food in snake:
                    food = (random.randint(0, GRID_SIZE - 1), random.randint(0, GRID_SIZE - 1))
            else:
                snake.pop(0)
        else:
            game_over_screen("Game Over: No path to food!")
            pygame.display.flip()
            pygame.time.wait(2000)

        draw_score()

        time_delta = clock.tick(60) / 1000.0

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
                    return game_loop(clock, obstacle_file)
                else:
                    algorithm = clicked_function
                    previous_path = []
                    path = algorithm(snake[-1], food, obstacles | set(snake[:-1]))
                    draw_path(path)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    dragging = True
                    x, y = pygame.mouse.get_pos()
                    grid_pos = ((y - GRID_OFFSET_Y) // CELL_SIZE, (x - GRID_OFFSET_X) // CELL_SIZE)
                    if grid_pos not in snake and grid_pos != food:
                        if 0 <= grid_pos[0] < GRID_SIZE and 0 <= grid_pos[1] < GRID_SIZE:
                            obstacles.add(grid_pos)
                    last_pos = grid_pos

            elif event.type == pygame.MOUSEMOTION and dragging:
                x, y = pygame.mouse.get_pos()
                grid_pos = ((y - GRID_OFFSET_Y) // CELL_SIZE, (x - GRID_OFFSET_X) // CELL_SIZE)
                if grid_pos != last_pos:
                    if grid_pos not in snake and grid_pos != food:
                        if 0 <= grid_pos[0] < GRID_SIZE and 0 <= grid_pos[1] < GRID_SIZE:
                            obstacles.add(grid_pos)
                            last_pos = grid_pos

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    dragging = False
                    last_pos = None

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

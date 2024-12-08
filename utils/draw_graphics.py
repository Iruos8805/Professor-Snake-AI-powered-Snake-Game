import pygame
from .config_constants import *
import random
from .snake_algorithms import *

screen = pygame.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE + 200))

Clock = pygame.time.Clock()
apple = pygame.image.load("assets/apple.png").convert_alpha()
stone = pygame.image.load("assets/stone.png").convert_alpha()

button_labels = ['BFS', 'A*', 'DFS', 'Greedy BFS', 'Iterative Deepening DFS', 'Bidirectional Search' 'Quit', 'Restart',]
button_functions = ['bfs', 'a_star', 'dfs', 'g_bfs', 'i_d_dfs', 'bi_search', 'quit', 'restart']

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

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
        block_rect = pygame.Rect(x_pos, y_pos, CELL_SIZE, CELL_SIZE)
        
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
    fruit_rect = (x, y, size, size)
    screen.blit(apple, fruit_rect)

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE
        stone_rect = (x, y, CELL_SIZE, CELL_SIZE)
        screen.blit(stone, stone_rect)


def draw_path(path):
    if path:
        for step in path[:-1]:
            x, y = step[1] * CELL_SIZE + 2, step[0] * CELL_SIZE + 2
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)

def game_over_screen(message="Game Over!"):
    screen.fill((30, 30, 30))
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    game_loop(Clock)
    

def draw_buttons():
    font = pygame.font.Font(None, 24)
    button_y = SCREEN_SIZE + BUTTON_MARGIN
    for i, label in enumerate(button_labels):
        button_x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        # Draw button
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)

        # Wrap text if it's too wide
        wrapped_lines = []
        words = label.split()
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if font.size(test_line)[0] <= BUTTON_WIDTH - 10:  # Account for padding
                current_line = test_line
            else:
                wrapped_lines.append(current_line)
                current_line = word
        if current_line:
            wrapped_lines.append(current_line)

        # Render each line of text
        for j, line in enumerate(wrapped_lines[:2]):  # Show at most 2 lines
            text = font.render(line, True, BUTTON_TEXT_COLOR)
            text_x = button_x + BUTTON_WIDTH // 2 - text.get_width() // 2
            text_y = button_y + BUTTON_HEIGHT // 2 - text.get_height() * len(wrapped_lines) // 2 + j * text.get_height()
            screen.blit(text, (text_x, text_y))

def handle_button_click(mouse_pos):
    button_y = SCREEN_SIZE + BUTTON_MARGIN
    for i, function_name in enumerate(button_functions):
        button_x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        if button_rect.collidepoint(mouse_pos):
            return function_name
    return None



def game_loop(clock):
    global dragging, last_pos

    dragging = False
    running = True
    snake = [(10, 10)]
    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    obstacles = set()
    algorithm = bfs
    previous_path = []

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_buttons()
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
                food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                while food in obstacles or food in snake:
                    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            else:
                snake.pop(0)
        else:
            game_over_screen("Game Over: No path to food!")
            pygame.display.flip()
            pygame.time.wait(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    clicked_function = handle_button_click(event.pos)
                    if clicked_function == 'bfs':
                        algorithm = bfs
                    elif clicked_function == 'a_star':
                        algorithm = a_star
                    elif clicked_function == 'dfs':
                        algorithm = dfs
                    elif clicked_function == 'g_bfs':
                        algorithm = greedy_bfs
                    elif clicked_function == 'i_d_bfs':
                        algorithm = iddfs
                    elif clicked_function == 'bi_search':
                        algorithm = bidirectional_search
                    elif clicked_function == 'quit':
                        running = False
                    elif clicked_function == 'restart':
                        game_loop(Clock)
                    else:
                        dragging = True
                        x, y = pygame.mouse.get_pos()
                        grid_pos = (y // CELL_SIZE, x // CELL_SIZE)
                        if grid_pos not in snake and grid_pos != food:
                            if grid_pos[0] < GRID_SIZE and grid_pos[1] < GRID_SIZE:
                                obstacles.add(grid_pos)
                        last_pos = grid_pos

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

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()
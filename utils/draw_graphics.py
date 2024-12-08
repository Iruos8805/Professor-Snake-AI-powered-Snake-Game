import pygame
from .config_constants import *
import random
from .snake_algorithms import *

screen = pygame.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE + 200))

Clock = pygame.time.Clock()

button_labels = ['BFS', 'A*', 'DFS', 'Quit', 'Restart']
button_functions = ['bfs', 'a_star', 'dfs', 'quit', 'restart']

def draw_grid():
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = SNAKE_COLOR if i != len(snake) - 1 else (0, 100, 0)
        pygame.draw.rect(screen, color, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, LINE_COLOR, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_food(food):
    size = CELL_SIZE - 6 + (3 * (pygame.time.get_ticks() % 1000) // 500)
    x, y = food[1] * CELL_SIZE + 3, food[0] * CELL_SIZE + 3
    pygame.draw.ellipse(screen, RED, (x, y, size, size))

def draw_obstacles(obstacles):
    for obstacle in obstacles:
        x, y = obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE
        pygame.draw.rect(screen, OBSTACLE_TEXTURE, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y + CELL_SIZE), 2)
        pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x, y + CELL_SIZE), 2)

def draw_path(path):
    if path:
        for step in path[:-1]:
            x, y = step[1] * CELL_SIZE + 2, step[0] * CELL_SIZE + 2
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)

def draw_instructions():
    font = pygame.font.Font(pygame.font.match_font('comicsansms'), 18)
    instructions = [
        "Press 'B' for BFS, 'A' for A*, 'D' for DFS.",
        "Click to place obstacles.",
        "Press 'Q' to quit or 'R' to restart after game over."
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (SCREEN_SIZE + 20, 30 + i * 30))

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
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        text = font.render(label, True, BUTTON_TEXT_COLOR)
        screen.blit(text, (button_x + BUTTON_WIDTH // 2 - text.get_width() // 2, button_y + BUTTON_HEIGHT // 2 - text.get_height() // 2))

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
        draw_instructions()

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
                    elif clicked_function == 'quit':
                        running = False
                    elif clicked_function == 'restart':
                        game_loop()
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
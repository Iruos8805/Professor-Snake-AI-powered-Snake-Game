import pygame
import pygame_gui
from .config_constants import *
import random
from .snake_algorithms import *

screen = pygame.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE + 200))

Clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE + 200))
GRID_WIDTH = GRID_SIZE * CELL_SIZE
GRID_HEIGHT = GRID_SIZE * CELL_SIZE

pygame.init()
manager = pygame_gui.UIManager((SCREEN_SIZE + 400, SCREEN_SIZE + 200))

button_labels = ['BFS', 'A*', 'DFS', 'Greedy BFS', 'Iterative Deepening DFS', 'Bidirectional Search', 'Quit', 'Restart']
button_functions = [bfs, a_star, dfs, greedy_bfs, iddfs, bidirectional_search, 'quit', 'restart']

button_width = 180
button_height = 50
button_margin = 10
buttons_per_row = 3
start_x = GRID_WIDTH + 20
start_y = 20  
buttons = []
buttons_per_row = 2

def enumerate_buttons():
    for i, label in enumerate(button_labels):
        col = i % buttons_per_row
        row = i // buttons_per_row
        button_x = start_x + col * (button_width + button_margin)
        button_y = start_y + row * (button_height + button_margin)

        buttons.append(
            pygame_gui.elements.UIButton(
                relative_rect=pygame.Rect((button_x, button_y), (button_width, button_height)),
                text=label,
                manager=manager
            )
        )

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

def game_over_screen(message="Game Over!"):
    screen.fill((30, 30, 30))
    font = pygame.font.Font(None, 50)
    text = font.render(message, True, RED)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(1500)
    game_loop(Clock)
    
def game_loop(clock):
    global dragging, last_pos

    dragging = False
    running = True
    snake = [(10, 10)]
    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    obstacles = set()
    algorithm = bfs
    previous_path = []
    enumerate_buttons()

    while running:
        screen.fill(BLACK)
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
                food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                while food in obstacles or food in snake:
                    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            else:
                snake.pop(0)
        else:
            game_over_screen("Game Over: No path to food!")
            pygame.display.flip()
            pygame.time.wait(2000)

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
                    game_loop(clock)
                else:
                    algorithm = clicked_function
                    previous_path = []  
                    path = algorithm(snake[-1], food, obstacles | set(snake[:-1]))
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
        clock.tick(10)

    pygame.quit()
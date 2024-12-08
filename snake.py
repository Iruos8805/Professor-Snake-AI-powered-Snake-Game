import pygame
import random
from collections import deque
import heapq

# Constants
GRID_SIZE = 30
CELL_SIZE = 20
SCREEN_SIZE = GRID_SIZE * CELL_SIZE
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
# Constants for Snake and Grid Appearance
SNAKE_COLOR = (0, 128, 0)  # Dark green for the snake
GRID_COLOR = (144, 238, 144)  # Light green grid color
LINE_COLOR = (0, 128, 0)  # Dark green grid line color
YELLOW = (255, 255, 0)  # Path highlight color
# Constants for Appearance Enhancements
GRID_COLOR_1 = (220, 220, 220)  # Light grid color
GRID_COLOR_2 = (200, 200, 200)  # Dark grid color
SNAKE_HEAD_COLOR = (0, 128, 0)  # Darker green for snake head
BACKGROUND_COLOR = (240, 248, 255)  # Subtle light blue
OBSTACLE_TEXTURE = (100, 100, 255)  # Textured blue for obstacles


# Constants for Button Dimensions and Colors
BUTTON_WIDTH = 80
BUTTON_HEIGHT = 40
BUTTON_MARGIN = 10
BUTTON_COLOR = (0, 0, 0)  # Black
BUTTON_BORDER_COLOR = (255, 0, 0)  # Red
BUTTON_TEXT_COLOR = (255, 255, 255)  # White

# Button Labels
button_labels = ['BFS', 'A*', 'DFS', 'Quit', 'Restart']
button_functions = ['bfs', 'a_star', 'dfs', 'quit', 'restart']


# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE + 400, SCREEN_SIZE + 200))  # Extra space for instructions
pygame.display.set_caption("AI Snake Game")

clock = pygame.time.Clock()

# Assuming these exist based on your original game setup
GRID = [(x, y) for x in range(GRID_SIZE) for y in range(GRID_SIZE)]
ADJACENCY_DICT = {}  # This should be filled based on grid adjacency

def bfs(start, goal, obstacles):
    """Breadth-First Search for pathfinding."""
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start: None}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path to get it from start to goal

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return None  # No path found

def dfs(start, goal, obstacles):
    """Depth-First Search for pathfinding."""
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {start: None}

    while stack:
        current = stack.pop()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path to get it from start to goal

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    return None  # No path found

def a_star(start, goal, obstacles):
    """A* Search for pathfinding."""
    def heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])  # Manhattan distance

    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {start: None}
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]  # Reverse the path to get it from start to goal

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in obstacles:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    priority = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    parent[neighbor] = current
    return None  # No path found

# Modified draw_grid function to apply new colors for squares and lines
def draw_grid():
    """Draws a grid with light green squares and dark green lines."""
    for y in range(GRID_SIZE):
        for x in range(GRID_SIZE):
            pygame.draw.rect(screen, GRID_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, LINE_COLOR, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


# Modified draw_snake to make the snake appear as a snake with dark green color for the head
def draw_snake(snake):
    """Draws the snake with a highlighted dark green head."""
    for i, segment in enumerate(snake):
        color = SNAKE_COLOR if i != len(snake) - 1 else (0, 100, 0)  # Dark green for the head
        pygame.draw.rect(screen, color, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, LINE_COLOR, (segment[1] * CELL_SIZE, segment[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)

def draw_food(food):
    """Draws the food with a pulsing effect."""
    size = CELL_SIZE - 6 + (3 * (pygame.time.get_ticks() % 1000) // 500)  # Pulse effect
    x, y = food[1] * CELL_SIZE + 3, food[0] * CELL_SIZE + 3
    pygame.draw.ellipse(screen, RED, (x, y, size, size))

def draw_obstacles(obstacles):
    """Draws textured obstacles."""
    for obstacle in obstacles:
        x, y = obstacle[1] * CELL_SIZE, obstacle[0] * CELL_SIZE
        pygame.draw.rect(screen, OBSTACLE_TEXTURE, (x, y, CELL_SIZE, CELL_SIZE))
        pygame.draw.line(screen, WHITE, (x, y), (x + CELL_SIZE, y + CELL_SIZE), 2)  # Diagonal texture
        pygame.draw.line(screen, WHITE, (x + CELL_SIZE, y), (x, y + CELL_SIZE), 2)

# Ensure that the DFS path is drawn correctly (you might need to check the pathfinding logic as well)
def draw_path(path):
    """Draws a glowing path to the food (check DFS path)."""
    if path:
        for step in path[:-1]:  # Exclude the goal
            x, y = step[1] * CELL_SIZE + 2, step[0] * CELL_SIZE + 2
            pygame.draw.rect(screen, YELLOW, (x, y, CELL_SIZE - 4, CELL_SIZE - 4), border_radius=4)
# Modified draw_instructions to place instructions below the grid
def draw_instructions():
    """Displays instructions with better font and styling below the grid."""
    font = pygame.font.Font(pygame.font.match_font('comicsansms'), 18)
    instructions = [
        "Press 'B' for BFS, 'A' for A*, 'D' for DFS.",
        "Click to place obstacles.",
        "Press 'Q' to quit or 'R' to restart after game over."
    ]
    for i, instruction in enumerate(instructions):
        text = font.render(instruction, True, WHITE)
        screen.blit(text, (SCREEN_SIZE + 20, 30 + i * 30))


def game_over_screen():
    """Displays a game over screen with animations."""
    screen.fill((30, 30, 30))  # Dark background
    font = pygame.font.Font(None, 70)
    text = font.render("Game Over!", True, RED)
    text_rect = text.get_rect(center=(SCREEN_SIZE // 2, SCREEN_SIZE // 2))
    screen.blit(text, text_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

# Helper to Draw Buttons
def draw_buttons():
    font = pygame.font.Font(None, 24)
    button_y = SCREEN_SIZE + BUTTON_MARGIN
    for i, label in enumerate(button_labels):
        button_x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        
        text = font.render(label, True, BUTTON_TEXT_COLOR)
        text_rect = text.get_rect(center=(button_x + BUTTON_WIDTH // 2, button_y + BUTTON_HEIGHT // 2))
        screen.blit(text, text_rect)

# Detect Button Clicks
def handle_button_click(mouse_pos):
    button_y = SCREEN_SIZE + BUTTON_MARGIN
    for i, function_name in enumerate(button_functions):
        button_x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        button_rect = pygame.Rect(button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT)
        if button_rect.collidepoint(mouse_pos):
            return function_name
    return None


# Helper to Draw Buttons
def draw_buttons():
    font = pygame.font.Font(None, 24)
    button_y = SCREEN_SIZE + BUTTON_MARGIN
    for i, label in enumerate(button_labels):
        button_x = BUTTON_MARGIN + i * (BUTTON_WIDTH + BUTTON_MARGIN)
        pygame.draw.rect(screen, BUTTON_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT))
        pygame.draw.rect(screen, BUTTON_BORDER_COLOR, (button_x, button_y, BUTTON_WIDTH, BUTTON_HEIGHT), 2)
        text = font.render(label, True, BUTTON_TEXT_COLOR)
        screen.blit(text, (button_x + BUTTON_WIDTH // 2 - text.get_width() // 2, button_y + BUTTON_HEIGHT // 2 - text.get_height() // 2))

# Main loop


def main():
    running = True
    snake = [(10, 10)]
    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
    obstacles = set()
    algorithm = bfs  # Default algorithm
    previous_path = []  # Keeps track of the last path drawn

    while running:
        screen.fill(BLACK)
        draw_grid()
        draw_buttons() 
        draw_snake(snake)
        draw_food(food)
        draw_obstacles(obstacles)
        draw_instructions()

        # Pathfinding and Snake Movement
        snake_body = set(snake[:-1])
        path = algorithm(snake[-1], food, obstacles | snake_body)
        
        # If path changes, update the previous path and draw the new path
        if path != previous_path:
            previous_path = path
            # Highlight the path up to the food (excluding the food itself)
            draw_path(path)

        if path:
            next_move = path[1]  # Move to the next step in the path
            if next_move in snake_body:
                game_over_screen()
                pygame.time.wait(3000)  # Wait before restarting or quitting
                continue

            snake.append(next_move)
            if next_move == food:
                food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
                while food in obstacles or food in snake:
                    food = (random.randint(0, GRID_SIZE-1), random.randint(0, GRID_SIZE-1))
            else:
                snake.pop(0)
        else:
            display_message("Game Over: No path to food!")
            pygame.display.flip()
            pygame.time.wait(2000)

        # Main Game Loop Modification
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
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
                        main()
                    else:
                        # Handling obstacle placement
                        x, y = pygame.mouse.get_pos()
                        grid_pos = (y // CELL_SIZE, x // CELL_SIZE)
                        if grid_pos not in snake and grid_pos != food:  # Avoid placing obstacles where the snake or food is
                            obstacles.add(grid_pos)

            # Drawing Buttons Below the Game Area
            draw_buttons()

        pygame.display.flip()
        clock.tick(10)  # Slower snake speed

    pygame.quit()

if __name__ == "__main__":
    main()

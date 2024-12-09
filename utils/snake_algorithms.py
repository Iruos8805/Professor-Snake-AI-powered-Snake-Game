from collections import deque
import heapq
from .config_constants import GRID_SIZE

def bfs(start, goal, obstacles):
    queue = deque([start])
    visited = set()
    visited.add(start)
    parent = {start:None}

    while queue:
        current = queue.popleft()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
    return None


def dfs(start, goal, obstacles):
    stack = [start]
    visited = set()
    visited.add(start)
    parent = {start:None}

    while stack:
        current = stack.pop()
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
    return None

def a_star(start, goal, obstacles):
    def heuristic(cell, goal):
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1]) 

    open_set = []
    heapq.heappush(open_set, (0, start))
    parent = {start:None}
    g_score = {start:0}

    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in obstacles:
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    priority = tentative_g_score + heuristic(neighbor, goal)
                    heapq.heappush(open_set, (priority, neighbor))
                    parent[neighbor] = current
    return None 

def greedy_bfs(start, goal, obstacles):
    def heuristic(cell, goal):
        # Manhattan distance as heuristic (you can modify based on needs)
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    open_set = []
    # Initially push the start node with its heuristic value
    heapq.heappush(open_set, (heuristic(start, goal), start))
    visited = set()
    parent = {start: None}

    while open_set:
        # Pop the node with the smallest heuristic value
        _, current = heapq.heappop(open_set)

        # Check if we have reached the goal
        if current == goal:
            # Reconstruct the path
            path = []
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]

        # Mark the current node as visited
        visited.add(current)

        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current[0] + dx, current[1] + dy)

            # Check if the neighbor is within bounds, not visited, and not an obstacle
            if (
                0 <= neighbor[0] < GRID_SIZE and
                0 <= neighbor[1] < GRID_SIZE and
                neighbor not in visited and
                neighbor not in obstacles
            ):
                visited.add(neighbor)  # Add neighbor to visited to prevent re-processing
                parent[neighbor] = current
                # Add the neighbor to the open set with its heuristic value
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))

    # Return None if there is no path to the goal
    return None


def iddfs(start, goal, obstacles):
    def dls(node, goal, limit, visited, parent):
        if node == goal:
            return True
        if limit <= 0:
            return False

        visited.add(node)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (node[0] + dx, node[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited and neighbor not in obstacles:
                parent[neighbor] = node
                if dls(neighbor, goal, limit - 1, visited, parent):
                    return True
        return False

    depth = 0
    while True:
        visited = set()
        parent = {start: None}
        if dls(start, goal, depth, visited, parent):
            path = []
            current = goal
            while current:
                path.append(current)
                current = parent[current]
            return path[::-1]
        depth += 1


def bidirectional_search(start, goal, obstacles):
    if start == goal:
        return [start]

    frontier_start = {start}
    frontier_goal = {goal}
    parent_start = {start: None}
    parent_goal = {goal: None}
    visited_start = set()
    visited_goal = set()

    while frontier_start and frontier_goal:
        
        current_start = frontier_start.pop()
        visited_start.add(current_start)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current_start[0] + dx, current_start[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited_start and neighbor not in obstacles:
                parent_start[neighbor] = current_start
                if neighbor in visited_goal:
                    
                    path_start = []
                    path_goal = []
                    current = neighbor
                    while current:
                        path_start.append(current)
                        current = parent_start[current]
                    current = neighbor
                    while current:
                        path_goal.append(current)
                        current = parent_goal[current]
                    return path_start[::-1] + path_goal[1:]

                frontier_start.add(neighbor)

        
        current_goal = frontier_goal.pop()
        visited_goal.add(current_goal)
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            neighbor = (current_goal[0] + dx, current_goal[1] + dy)
            if 0 <= neighbor[0] < GRID_SIZE and 0 <= neighbor[1] < GRID_SIZE and neighbor not in visited_goal and neighbor not in obstacles:
                parent_goal[neighbor] = current_goal
                if neighbor in visited_start:
                    
                    path_start = []
                    path_goal = []
                    current = neighbor
                    while current:
                        path_start.append(current)
                        current = parent_start[current]
                    current = neighbor
                    while current:
                        path_goal.append(current)
                        current = parent_goal[current]
                    return path_start[::-1] + path_goal[1:]

                frontier_goal.add(neighbor)
    return None



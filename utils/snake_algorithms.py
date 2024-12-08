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
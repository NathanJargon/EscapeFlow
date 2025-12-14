import random
from collections import deque
from prolog_solver import PrologPathfinder
from lisp_solver import LispPathfinder

DIRS = [(0, -1), (1, 0), (0, 1), (-1, 0)]

class Maze:
    def __init__(self, width, height, difficulty=1, algorithm="bfs"):
        self.width = width
        self.height = height
        self.difficulty = difficulty
        self.algorithm = algorithm
        self.prolog_solver = PrologPathfinder() if algorithm == "prolog" else None
        self.lisp_solver = LispPathfinder() if algorithm == "lisp" else None
        self.maze = self.generate_maze()

    def generate_maze(self):
        maze = [[0 for _ in range(self.width)] for _ in range(self.height)]
        for x in range(self.width):
            maze[0][x] = maze[self.height-1][x] = 1
        for y in range(self.height):
            maze[y][0] = maze[y][self.width-1] = 1
        start = (1, 1)
        end = (self.width-2, self.height-2)
        path = self._guaranteed_path(start, end)
        playable_area = (self.width - 2) * (self.height - 2)
        max_walls = playable_area - len(path) - 5
        wall_count = min((self.width * self.height // 4) * self.difficulty, max_walls)
        placed = 0
        attempts = 0
        max_attempts = wall_count * 100
        while placed < wall_count and attempts < max_attempts:
            x = random.randint(1, self.width-2)
            y = random.randint(1, self.height-2)
            if maze[y][x] == 0 and (x, y) not in path:
                maze[y][x] = 1
                placed += 1
            attempts += 1
        return maze

    def _guaranteed_path(self, start, end):
        # Simple straight path with random turns
        path = [start]
        x, y = start
        while (x, y) != end:
            if x < end[0]:
                x += 1
            elif x > end[0]:
                x -= 1
            elif y < end[1]:
                y += 1
            elif y > end[1]:
                y -= 1
            path.append((x, y))
        return set(path)

    def move_walls(self):
        from_pos = None
        to_pos = None
        wall_positions = [(y, x) for y in range(1, self.height-1) for x in range(1, self.width-1) if self.maze[y][x] == 1]
        empty_positions = [(y, x) for y in range(1, self.height-1) for x in range(1, self.width-1) if self.maze[y][x] == 0]
        # Only move if it doesn't block the only path; use Python BFS for reliability
        for _ in range(20):
            if not wall_positions or not empty_positions:
                break
            wy, wx = random.choice(wall_positions)
            ey, ex = random.choice(empty_positions)
            self.maze[wy][wx] = 0
            self.maze[ey][ex] = 1
            start = (1, 1)
            end = (self.width-2, self.height-2)
            if self._bfs_plain(start, end):
                from_pos = (wy, wx)
                to_pos = (ey, ex)
                break
            else:
                self.maze[wy][wx] = 1
                self.maze[ey][ex] = 0
        # If no valid move found, do nothing

    def _bfs_plain(self, start, goal):
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for dx, dy in DIRS:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 0 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited[(nx, ny)] = current
        path = []
        node = goal
        while node and node in visited:
            path.append(node)
            node = visited[node]
        path.reverse()
        return path if path and path[0] == start else []

    def bfs_path(self, start, goal):
        if self.algorithm == "prolog" and self.prolog_solver:
            return self.prolog_solver.find_path(self.maze, start, goal, self.width, self.height)
        elif self.algorithm == "lisp" and self.lisp_solver:
            return self.lisp_solver.find_path(self.maze, start, goal, self.width, self.height)
        
        queue = deque([start])
        visited = {start: None}
        while queue:
            current = queue.popleft()
            if current == goal:
                break
            for dx, dy in DIRS:
                nx, ny = current[0] + dx, current[1] + dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    if self.maze[ny][nx] == 0 and (nx, ny) not in visited:
                        queue.append((nx, ny))
                        visited[(nx, ny)] = current
        path = []
        node = goal
        while node and node in visited:
            path.append(node)
            node = visited[node]
        path.reverse()
        return path if path and path[0] == start else []
        path.reverse()
        return path if path and path[0] == start else []

from collections import deque

class LispPathfinder:
    def __init__(self):
        pass

    def find_path(self, maze, start, goal, width, height):
        return self._lisp_bfs(
            [(start, [start])],
            goal,
            maze,
            width,
            height,
            set()
        )

    def _lisp_bfs(self, queue, goal, maze, width, height, visited):
        if not queue:
            return []

        (current, path), *rest = queue
        if current == goal:
            return path

        if current in visited:
            return self._lisp_bfs(rest, goal, maze, width, height, visited)

        visited.add(current)
        neighbors = self._lisp_neighbors(current, maze, width, height, visited)
        new_queue = rest + [(n, path + [n]) for n in neighbors]

        return self._lisp_bfs(new_queue, goal, maze, width, height, visited)

    def _lisp_neighbors(self, pos, maze, width, height, visited):
        x, y = pos
        directions = [(0, -1), (1, 0), (0, 1), (-1, 0)]
        return list(filter(
            lambda p: self._is_walkable(p, maze, width, height, visited),
            map(lambda d: (x + d[0], y + d[1]), directions)
        ))

    def _is_walkable(self, pos, maze, width, height, visited):
        x, y = pos
        return (
            0 <= x < width and
            0 <= y < height and
            maze[y][x] == 0 and
            pos not in visited
        )

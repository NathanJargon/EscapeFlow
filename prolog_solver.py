import os

try:
    from pyswip import Prolog
    PROLOG_AVAILABLE = True
except ImportError:
    PROLOG_AVAILABLE = False

class PrologPathfinder:
    def __init__(self):
        if not PROLOG_AVAILABLE:
            self.prolog = None
            return
        self.prolog = Prolog()
        prolog_file = os.path.join(os.path.dirname(__file__), 'pathfinding.pl')
        try:
            self.prolog.consult(prolog_file)
        except:
            self.prolog = None

    def find_path(self, maze, start, goal, width, height):
        if not self.prolog:
            return []

        maze_term = self._convert_maze_to_term(maze)
        start_x, start_y = start
        goal_x, goal_y = goal

        try:
            result_list = list(self.prolog.query(
                f'solve_maze({start_x}, {start_y}, {goal_x}, {goal_y}, {maze_term}, {width}, {height}, Path)',
                catcherrors=True
            ))

            if result_list:
                path_result = result_list[0].get('Path', [])
                return self._parse_path(path_result)
            return []
        except Exception:
            return []

    def _convert_maze_to_term(self, maze):
        rows = []
        for row in maze:
            row_term = '[' + ','.join(str(cell) for cell in row) + ']'
            rows.append(row_term)
        return '[' + ','.join(rows) + ']'

    def _parse_path(self, path_term):
        path = []

        # When pyswip returns a Python list of tuples
        if isinstance(path_term, list):
            for item in path_term:
                if isinstance(item, tuple) and len(item) == 2:
                    try:
                        path.append((int(item[0]), int(item[1])))
                    except Exception:
                        continue
            if path:
                return path

        # Fallback: parse from string representation
        path_str = str(path_term).strip('[]')
        if not path_str:
            return path

        parts = [p.strip() for p in path_str.split('),')]
        for coord in parts:
            coord = coord.replace('(', '').replace(')', '').strip()
            if not coord:
                continue
            comps = coord.split(',')
            if len(comps) != 2:
                continue
            try:
                x = int(comps[0].strip())
                y = int(comps[1].strip())
                path.append((x, y))
            except Exception:
                continue
        return path

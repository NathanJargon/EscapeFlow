import ctypes
import os
import sys

class CppPathfinder:
    def __init__(self):
        self.dll = None
        self._load_dll()

    def _load_dll(self):
        try:
            dll_path = os.path.join(os.path.dirname(__file__), 'pathfinding.dll')
            if os.path.exists(dll_path):
                self.dll = ctypes.CDLL(dll_path)
                self.dll.find_path_cpp.argtypes = [
                    ctypes.POINTER(ctypes.c_int),
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int,
                    ctypes.c_int
                ]
                self.dll.find_path_cpp.restype = ctypes.c_void_p
                self.dll.free_path.argtypes = [ctypes.c_void_p]
                self.dll.free_path.restype = None
        except Exception:
            self.dll = None

    def find_path(self, maze, start, goal, width, height):
        if not self.dll:
            return []

        try:
            maze_flat = []
            for row in maze:
                maze_flat.extend(row)
            
            maze_array = (ctypes.c_int * len(maze_flat))(*maze_flat)
            start_x, start_y = start
            goal_x, goal_y = goal

            result_ptr = self.dll.find_path_cpp(
                maze_array,
                width,
                height,
                start_x,
                start_y,
                goal_x,
                goal_y
            )

            if not result_ptr:
                return []

            class Path(ctypes.Structure):
                pass
            Path._fields_ = [("points", ctypes.POINTER(ctypes.c_int * 2)), ("length", ctypes.c_int)]

            path_obj = ctypes.cast(result_ptr, ctypes.POINTER(Path)).contents
            
            if path_obj.length == 0:
                self.dll.free_path(result_ptr)
                return []

            path = []
            for i in range(path_obj.length):
                x = path_obj.points[i][0]
                y = path_obj.points[i][1]
                path.append((x, y))

            self.dll.free_path(result_ptr)
            return path
        except Exception:
            return []

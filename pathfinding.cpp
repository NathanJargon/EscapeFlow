#include <queue>
#include <vector>
#include <cstring>

using namespace std;

typedef struct {
    int x, y;
} Point;

typedef struct {
    Point* points;
    int length;
} Path;

extern "C" {
    Path* find_path_cpp(int* maze, int width, int height, int start_x, int start_y, int goal_x, int goal_y) {
        queue<pair<Point, vector<Point>>> q;
        vector<vector<bool>> visited(height, vector<bool>(width, false));
        
        Point start = {start_x, start_y};
        vector<Point> start_path = {start};
        q.push({start, start_path});
        visited[start_y][start_x] = true;
        
        int dirs[4][2] = {{0, -1}, {1, 0}, {0, 1}, {-1, 0}};
        
        while (!q.empty()) {
            Point current = q.front().first;
            vector<Point> path = q.front().second;
            q.pop();
            
            if (current.x == goal_x && current.y == goal_y) {
                Path* result = new Path();
                result->length = path.size();
                result->points = new Point[path.size()];
                for (int i = 0; i < path.size(); i++) {
                    result->points[i] = path[i];
                }
                return result;
            }
            
            for (int i = 0; i < 4; i++) {
                int nx = current.x + dirs[i][0];
                int ny = current.y + dirs[i][1];
                
                if (nx >= 0 && nx < width && ny >= 0 && ny < height && 
                    !visited[ny][nx] && maze[ny * width + nx] == 0) {
                    visited[ny][nx] = true;
                    Point next = {nx, ny};
                    vector<Point> new_path = path;
                    new_path.push_back(next);
                    q.push({next, new_path});
                }
            }
        }
        
        Path* result = new Path();
        result->length = 0;
        result->points = nullptr;
        return result;
    }
    
    void free_path(Path* path) {
        if (path) {
            if (path->points) {
                delete[] path->points;
            }
            delete path;
        }
    }
}

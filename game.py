import pygame
import sys
from maze_algorithm import Maze
from sprites import PlayerSprite, ExitSprite

CELL_SIZE = 48
MAZE_WIDTH = 15
MAZE_HEIGHT = 10
FPS = 10
MOVE_WALL_INTERVAL = 60

# Palette
BG = (17, 24, 39)
PANEL = (24, 33, 53)
FLOOR = (232, 236, 243)
WALL = (42, 55, 78)
GRID = (90, 110, 140)
PATH = (80, 180, 255)
EXIT = (0, 200, 120)

HUD_TEXT = (220, 230, 245)
HUD_ACCENT = (120, 200, 255)

class Game:
    def __init__(self, control_scheme="arrows", difficulty=1, guide=False, algorithm="bfs"):
        self.control_scheme = control_scheme
        self.difficulty = difficulty
        self.guide = guide
        self.algorithm = algorithm
        self.maze = Maze(MAZE_WIDTH, MAZE_HEIGHT, difficulty, algorithm)
        self.player = (1, 1)
        self.exit_pos = (MAZE_WIDTH-2, MAZE_HEIGHT-2)
        self.frame_count = 0
        self.screen = pygame.display.set_mode((CELL_SIZE * MAZE_WIDTH, CELL_SIZE * MAZE_HEIGHT))
        pygame.display.set_caption("Game")
        self.clock = pygame.time.Clock()
        self.player_sprite = PlayerSprite(self.player)
        self.exit_sprite = ExitSprite(self.exit_pos)
        self.sprites = pygame.sprite.Group(self.player_sprite, self.exit_sprite)

    def get_move(self, event):
        if self.control_scheme == "arrows":
            if event.key == pygame.K_UP:
                return (0, -1)
            elif event.key == pygame.K_DOWN:
                return (0, 1)
            elif event.key == pygame.K_LEFT:
                return (-1, 0)
            elif event.key == pygame.K_RIGHT:
                return (1, 0)
        elif self.control_scheme == "wasd":
            if event.key == pygame.K_w:
                return (0, -1)
            elif event.key == pygame.K_s:
                return (0, 1)
            elif event.key == pygame.K_a:
                return (-1, 0)
            elif event.key == pygame.K_d:
                return (1, 0)
        return None

    def draw_maze(self, path):
        board_rect = pygame.Rect(0, 0, CELL_SIZE * MAZE_WIDTH, CELL_SIZE * MAZE_HEIGHT)
        pygame.draw.rect(self.screen, PANEL, board_rect, border_radius=12)

        for y in range(MAZE_HEIGHT):
            for x in range(MAZE_WIDTH):
                rect = pygame.Rect(x*CELL_SIZE, y*CELL_SIZE, CELL_SIZE, CELL_SIZE)
                if self.maze.maze[y][x] == 1:
                    pygame.draw.rect(self.screen, WALL, rect, border_radius=10)
                else:
                    pygame.draw.rect(self.screen, FLOOR, rect, border_radius=10)
                pygame.draw.rect(self.screen, GRID, rect, 1)

        if path:
            overlay = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            overlay.fill((*PATH, 90))
            for px, py in path:
                self.screen.blit(overlay, (px*CELL_SIZE, py*CELL_SIZE))

        self.exit_sprite.update(self.exit_pos)
        self.player_sprite.update(self.player)
        self.sprites.draw(self.screen)

    def draw_hud(self):
        hud_font = pygame.font.SysFont(None, 24)
        bar_rect = pygame.Rect(0, 0, CELL_SIZE * MAZE_WIDTH, 32)
        pygame.draw.rect(self.screen, PANEL, bar_rect)
        info = [
            f"Controls: {self.control_scheme.upper()}",
            f"Difficulty: {self.difficulty}",
            f"Guide: {'ON' if self.guide else 'OFF'}",
            f"Algo: {self.algorithm.upper()}"
        ]
        text = "  |  ".join(info)
        label = hud_font.render(text, True, HUD_TEXT)
        self.screen.blit(label, (12, 6))

    def run(self):
        running = True
        move_triggered = False
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                elif event.type == pygame.KEYDOWN:
                    move = self.get_move(event)
                    if move:
                        dx, dy = move
                        nx, ny = self.player[0] + dx, self.player[1] + dy
                        if 0 <= nx < MAZE_WIDTH and 0 <= ny < MAZE_HEIGHT and self.maze.maze[ny][nx] == 0:
                            self.player = (nx, ny)
                            move_triggered = True
            if move_triggered:
                self.maze.move_walls()
                move_triggered = False
            path = self.maze.bfs_path(self.player, self.exit_pos) if self.guide else []
            self.screen.fill(BG)
            self.draw_maze(path)
            self.draw_hud()
            pygame.display.flip()
            self.clock.tick(FPS)
            if self.player == self.exit_pos:
                self.show_win_screen()
                return "menu"

    def show_win_screen(self):
        font = pygame.font.SysFont(None, 64)
        sub_font = pygame.font.SysFont(None, 32)
        self.screen.fill((24, 120, 90))
        text = font.render("You Escaped!", True, (255,255,255))
        sub = sub_font.render("Returning to menu...", True, (230, 240, 240))
        self.screen.blit(text, (CELL_SIZE*4, CELL_SIZE*4))
        self.screen.blit(sub, (CELL_SIZE*4, CELL_SIZE*4 + 48))
        pygame.display.flip()
        pygame.time.wait(1600)

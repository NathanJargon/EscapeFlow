import pygame
import sys
from game import Game

CELL_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

class MainMenu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((CELL_SIZE * MAZE_WIDTH, CELL_SIZE * MAZE_HEIGHT))
        pygame.display.set_caption("Main Menu")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont(None, 48)
        self.control_scheme = "arrows"
        self.difficulty = 1
        self.guide = False

    def draw(self):
        self.screen.fill((30, 40, 60))
        title = self.font.render("EscapeFlow", True, (80, 180, 255))
        self.screen.blit(title, (CELL_SIZE * 3, CELL_SIZE * 1))
        menu_font = pygame.font.SysFont(None, 36)
        control_text = menu_font.render(f"Controls: {self.control_scheme.upper()} (Tab to toggle)", True, (255, 255, 255))
        self.screen.blit(control_text, (CELL_SIZE * 2, CELL_SIZE * 3))
        diff_text = menu_font.render(f"Difficulty: {self.difficulty} (Up/Down)", True, (255, 255, 255))
        self.screen.blit(diff_text, (CELL_SIZE * 2, CELL_SIZE * 5))
        guide_text = menu_font.render(f"Guide: {'ON' if self.guide else 'OFF'} (G to toggle)", True, (255, 255, 255))
        self.screen.blit(guide_text, (CELL_SIZE * 2, CELL_SIZE * 6))
        start_text = menu_font.render("Press Enter to Start", True, (40, 200, 80))
        start_rect = pygame.Rect(CELL_SIZE * 2, CELL_SIZE * 7, CELL_SIZE * 11, CELL_SIZE)
        pygame.draw.rect(self.screen, (80, 180, 255), start_rect, border_radius=12)
        self.screen.blit(start_text, (CELL_SIZE * 2 + 20, CELL_SIZE * 7 + 4))
        info_font = pygame.font.SysFont(None, 24)
        info_text = info_font.render("Tab: Controls | Up/Down: Difficulty | G: Guide", True, (200, 200, 200))
        self.screen.blit(info_text, (CELL_SIZE * 2, CELL_SIZE * 9))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_TAB:
                        self.control_scheme = "wasd" if self.control_scheme == "arrows" else "arrows"
                    elif event.key == pygame.K_UP:
                        self.difficulty = min(self.difficulty + 1, 3)
                    elif event.key == pygame.K_DOWN:
                        self.difficulty = max(self.difficulty - 1, 1)
                    elif event.key == pygame.K_g:
                        self.guide = not self.guide
                    elif event.key == pygame.K_RETURN:
                        running = False
        return self.control_scheme, self.difficulty, self.guide

def main():
    while True:
        menu = MainMenu()
        control_scheme, difficulty, guide = menu.run()
        game = Game(control_scheme, difficulty, guide)
        result = game.run()
        if result == "quit":
            break

if __name__ == "__main__":
    main()

import pygame
import sys
from game import Game

CELL_SIZE = 48
MAZE_WIDTH = 15
MAZE_HEIGHT = 10

# Palette
BG = (17, 24, 39)
PANEL = (26, 36, 56)
ACCENT = (86, 190, 255)
TEXT_MAIN = (230, 236, 245)
TEXT_MUTED = (170, 180, 195)
BUTTON = (80, 180, 255)
BUTTON_TEXT = (20, 30, 45)

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
        from prolog_solver import PROLOG_AVAILABLE
        self.prolog_available = PROLOG_AVAILABLE
        self.algorithm = "bfs"
        self.algorithm_list = ["bfs", "prolog", "lisp"]
        self.algorithm_idx = 0
    def draw(self):
        self.screen.fill(BG)

        card_rect = pygame.Rect(CELL_SIZE, CELL_SIZE, CELL_SIZE * 13, CELL_SIZE * 8)
        pygame.draw.rect(self.screen, PANEL, card_rect, border_radius=18)

        title = self.font.render("EscapeFlow", True, ACCENT)
        self.screen.blit(title, (CELL_SIZE * 3, CELL_SIZE * 1.4))

        menu_font = pygame.font.SysFont(None, 34)
        y_base = CELL_SIZE * 3
        line_gap = CELL_SIZE * 1.2
        control_text = menu_font.render(f"Controls: {self.control_scheme.upper()}  (Tab)", True, TEXT_MAIN)
        diff_text = menu_font.render(f"Difficulty: {self.difficulty}  (Up/Down)", True, TEXT_MAIN)
        guide_text = menu_font.render(f"Guide: {'ON' if self.guide else 'OFF'}  (G)", True, TEXT_MAIN)
        algo_display = self.algorithm.upper()
        algo_color = TEXT_MAIN
        algo_text = menu_font.render(f"Algorithm: {algo_display}  (A)", True, algo_color)

        self.screen.blit(control_text, (CELL_SIZE * 2, y_base))
        self.screen.blit(diff_text, (CELL_SIZE * 2, y_base + line_gap))
        self.screen.blit(guide_text, (CELL_SIZE * 2, y_base + line_gap * 2))
        self.screen.blit(algo_text, (CELL_SIZE * 2, y_base + line_gap * 3))

        start_rect = pygame.Rect(0, 0, CELL_SIZE * 9, CELL_SIZE * 1.2)
        start_rect.centerx = card_rect.centerx
        start_rect.y = y_base + line_gap * 4.0
        pygame.draw.rect(self.screen, BUTTON, start_rect, border_radius=14)
        start_text = menu_font.render("Press Enter to Start", True, TEXT_MAIN)
        text_rect = start_text.get_rect(center=start_rect.center)
        self.screen.blit(start_text, text_rect)

        info_font = pygame.font.SysFont(None, 24)
        info_text = info_font.render("Tab: Controls | Up/Down: Difficulty | G: Guide | A: Algorithm", True, TEXT_MUTED)
        info_rect = info_text.get_rect()
        info_rect.centerx = card_rect.centerx
        info_rect.y = card_rect.bottom + CELL_SIZE * 0.2
        self.screen.blit(info_text, info_rect)
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
                    elif event.key == pygame.K_a:
                        self.algorithm_idx = (self.algorithm_idx + 1) % len(self.algorithm_list)
                        self.algorithm = self.algorithm_list[self.algorithm_idx]
                    elif event.key == pygame.K_RETURN:
                        running = False
        return self.control_scheme, self.difficulty, self.guide, self.algorithm

def main():
    while True:
        menu = MainMenu()
        control_scheme, difficulty, guide, algorithm = menu.run()
        game = Game(control_scheme, difficulty, guide, algorithm)
        result = game.run()
        if result == "quit":
            break

if __name__ == "__main__":
    main()

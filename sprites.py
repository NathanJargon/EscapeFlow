import pygame
import math

CELL_SIZE = 40
MAZE_WIDTH = 15
MAZE_HEIGHT = 10

class PlayerSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2 - 4)
        pygame.draw.circle(self.image, (255, 255, 255), (CELL_SIZE//2, CELL_SIZE//2), CELL_SIZE//2 - 12)
        pygame.draw.circle(self.image, (0, 0, 0), (CELL_SIZE//2, CELL_SIZE//2), 4)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE)
    def update(self, pos):
        self.rect.topleft = (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE)

class ExitSprite(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.rect(self.image, (0, 200, 0), (4, 4, CELL_SIZE-8, CELL_SIZE-8), border_radius=8)
        pygame.draw.rect(self.image, (255, 255, 255), (12, 12, CELL_SIZE-24, CELL_SIZE-24), border_radius=4)
        self.rect = self.image.get_rect()
        self.rect.topleft = (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE)
    def update(self, pos):
        self.rect.topleft = (pos[0]*CELL_SIZE, pos[1]*CELL_SIZE)

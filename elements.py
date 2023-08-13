
import pygame
from settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PLAYER_WIDTH, PLAYER_HEIGHT))
        self.image.fill(PLAYER_COLOR)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.bottom = HEIGHT // 2
        self.velocity = 0
        self.score = 0  # Pontuação do jogador
    
    def update(self):
        self.rect.y += self.velocity
        
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            self.velocity = 0

    def increase_score(self, num_obstaculos):
        if num_obstaculos >= 3:
            self.score += 1

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, y_pos, height):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, height))
        self.image.fill(OBSTACLE_COLOR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH
        self.rect.y = y_pos
    
    def update(self):
        self.rect.x += OBSTACLE_VELOCITY
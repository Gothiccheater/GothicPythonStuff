import pygame
# Klasse für Spieler

class Player:
    def __init__(self, x, y, width, height, speed, max_height, spritePath):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.max_height = max_height
        self.image = pygame.image.load(spritePath)
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def move_up(self):
        self.y -= self.speed
        if self.y < 0:
            self.y = 0

    def move_down(self):
        self.y += self.speed
        if self.y > self.max_height:
            self.y = self.max_height

    def draw(self, window):
        window.blit(self.image, (self.x, self.y))
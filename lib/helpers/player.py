from hashlib import new
import pygame


class Player(object):

    def __init__(self, position: pygame.Vector2, size: tuple, display_width: int) -> None:

        self.position = position
        self.size = size
        self.display_width = display_width

        self.hitbox = pygame.Rect(position.x, position.y, size[0], size[1])

        self.color = (255, 255, 255)
        self.speed = 10

    def move(self, keys) -> None:

        if keys[pygame.K_LEFT]:
            if self.position.x - self.speed > 0:
                self.position.x -= self.speed
                self.hitbox.x -= self.speed
        if keys[pygame.K_RIGHT]:
            if self.position.x + self.size[0] + self.speed < self.display_width:
                self.position.x += self.speed
                self.hitbox.x += self.speed
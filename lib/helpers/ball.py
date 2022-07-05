import pygame


class Ball(object):

    def __init__(self, position: pygame.Vector2, size: int, display_width: int, display_height: int) -> None:

        self.size = size
        self.display_width = display_width
        self.display_height = display_height

        self.hitbox = pygame.Rect(position.x, position.y, size, size)

        self.color = (255, 255, 255)

        self.xvelocity = 0
        self.yvelocity = 0

        self.working = True

    def move(self) -> int:

        self.hitbox.x += self.xvelocity
        self.hitbox.y += self.yvelocity

        if self.hitbox.x < 0:
            self.xvelocity *= -1
            self.hitbox.x += self.xvelocity

        elif self.hitbox.x > self.display_width - self.size / 2:
            self.xvelocity *= -1
            self.hitbox.x += self.xvelocity

        if self.hitbox.y < 0:
            self.yvelocity *= -1
            self.hitbox.y += self.yvelocity

        if self.hitbox.y > self.display_height:
            return 1

        return 0

        
from lib.helpers.ball import Ball

import pygame
import random


class Field(object):

    def __init__(self, config: dict, display: pygame.Surface) -> None:
        
        self.config = config
        self.field = self.generate_new_field()

        self.display = display

        self.balls = []

    def generate_new_field(self) -> list:

        new_field = []

        for x in range(self.config['field_size_x']):
            for y in range(self.config['field_size_y']):
                new_field.append(Block((x * self.config['block_size'] + x * self.config['between_blocks'] + 1, y * self.config['block_size'] + y * self.config['between_blocks'] + 1), (self.config['block_size'], self.config['block_size'])))

        return new_field

    def add_ball(self, position: pygame.Vector2, velocity: pygame.Vector2) -> None:

        ball = Ball(
            position,
            int(self.config['block_size'] / 2),
            self.display.get_width(), 
            self.display.get_height() - self.config['video_height']
        )

        ball.xvelocity = velocity.x
        ball.yvelocity = velocity.y

        self.balls.append(ball)

    def update_balls(self) -> bool:

        touched_block = False

        for ball in self.balls:

            remove_ball = ball.move()
            if remove_ball == 1:
                self.balls.remove(ball)

            for block in self.field:
                if pygame.Rect.colliderect(ball.hitbox, block.hitbox):
                    self.field.remove(block)
                    touched_block = True
                    ball.xvelocity *= -1
                    ball.yvelocity *= -1

                    if len(self.balls) <= 15:

                        if random.randint(1, 10) == 1:

                            new_ball = Ball(
                                pygame.Vector2(ball.hitbox.x, ball.hitbox.y),
                                ball.size,
                                ball.display_width,
                                ball.display_height
                            )

                            new_ball.xvelocity = ball.xvelocity + random.randint(-1, 1)
                            new_ball.yvelocity = ball.yvelocity + random.randint(-1, 1)

                            self.balls.append(new_ball)

        return touched_block

    def touched_player(self, player_hitbox):

        for ball in self.balls:
            if pygame.Rect.colliderect(ball.hitbox, player_hitbox):
                ball.xvelocity = random.randint(-3, 3)
                ball.yvelocity *= -1
                ball.hitbox.y += ball.yvelocity * 2
                ball.hitbox.x += ball.xvelocity * 2
                

class Block(object):

    def __init__(self, position: tuple, size: tuple) -> None:

        self.size = size
        self.color = (
            random.randint(180, 255),
            random.randint(180, 255),
            random.randint(180, 255)
        )

        self.hitbox = pygame.Rect(position[0], position[1], size[0], size[1])



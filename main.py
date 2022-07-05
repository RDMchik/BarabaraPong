from lib.video_pygame.video import VideoSurface

from lib.helpers.player import Player
from lib.helpers.field import Field
from lib.helpers.ball import Ball

from lib.utils.json_load import JsonLoader

import pygame


pygame.init()
pygame.mixer.init()

config = JsonLoader.load('config.json')

clock = pygame.time.Clock()
display = pygame.display.set_mode(
    (
        config['field_size_x'] * config['block_size'] + config['field_size_x'] * config['between_blocks'],
        config['field_size_y'] * config['block_size'] + config['field_size_y'] * config['between_blocks'] + config['video_height'] + config['field_down_goes'] * config['block_size']
    )
)

happy_time_amount = 0

field = Field(config, display)

for i in range(5):
    field.add_ball(
        pygame.Vector2(
            display.get_width() / 2,
            config['field_size_y'] * config['block_size'] + int(config['field_down_goes'] / 2 * config['block_size'] / 2) +  + config['field_size_x'] * config['between_blocks']
        ),
        pygame.Vector2(0, -3) 
    )

player = Player(
    pygame.Vector2(
        int(display.get_width() / 2 - 25),
        config['field_size_y'] * config['block_size'] + int(config['field_down_goes'] * config['block_size'] / 2) +  + config['field_size_x'] * config['between_blocks']
    ),
    (80, 15),
    display.get_width()
)

sadvideo = VideoSurface(
    'static\\sad.mp4',
    pygame.Vector2(0, config['field_size_y'] * config['block_size'] + config['field_down_goes'] * config['block_size'] + config['field_size_x'] * config['between_blocks']),
    (config['field_size_x'] * config['block_size'] + config['field_size_x'] * config['between_blocks'], config['video_height'])
)
happyvideo = VideoSurface(
    'static\\happy.mp4',
    pygame.Vector2(0, config['field_size_y'] * config['block_size'] + config['field_down_goes'] * config['block_size'] + config['field_size_x'] * config['between_blocks']),
    (config['field_size_x'] * config['block_size'] + config['field_size_x'] * config['between_blocks'], config['video_height'])
)

losevideo = VideoSurface(
    'static\\lose.mp4',
    pygame.Vector2(0, config['field_size_y'] * config['block_size'] + config['field_down_goes'] * config['block_size'] + config['field_size_x'] * config['between_blocks']),
    (config['field_size_x'] * config['block_size'] + config['field_size_x'] * config['between_blocks'], config['video_height'])
)

sadvideo.sound.set_volume(0.05)
happyvideo.sound.set_volume(0.05)
losevideo.sound.set_volume(0.05)

sadvideo.play()

while True:

    display.fill((0, 120, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    happy_time_amount -= 0.1
    if happy_time_amount <= 0:
        happy_time_amount = 0

    keys = pygame.key.get_pressed()

    player.move(keys)
    if field.update_balls():
        happy_time_amount += 1

    for block in field.field:
        pygame.draw.rect(display, block.color, (block.hitbox.x, block.hitbox.y, block.size[0], block.size[1]))

    for ball in field.balls:
        field.touched_player(player.hitbox)
        pygame.draw.circle(display, ball.color, (ball.hitbox.x, ball.hitbox.y), ball.size)

    if happy_time_amount > 0:

        if not happyvideo.playing:
            happyvideo.play()
            display.blit(happyvideo(), happyvideo.get_position())
        else:
            display.blit(happyvideo(), happyvideo.get_position())

        if sadvideo.playing:
            sadvideo.stop()
    
    else:

        if not sadvideo.playing:
            sadvideo.play()
            display.blit(sadvideo(), sadvideo.get_position())
        else:
            display.blit(sadvideo(), sadvideo.get_position())

        if happyvideo.playing:
            happyvideo.stop()

    if len(field.balls) == 0:
        
        if sadvideo.playing:
            sadvideo.stop()
        if happyvideo.playing:
            happyvideo.stop()

        if not losevideo.playing:
            losevideo.play()

        display.blit(losevideo(), losevideo.get_position())

    pygame.draw.rect(display, player.color, (player.position.x , player.position.y, player.size[0], player.size[1]))
    
    pygame.display.flip()
    clock.tick(60)

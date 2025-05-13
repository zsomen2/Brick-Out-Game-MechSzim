# Mechatronikai szimuláció - BMEGEMINMMZ
# Ménes Zsombor - QTU3QF
# Brick Out Game

import pygame
import sys
import config
import random
from ball import Ball
from paddle import Paddle
from bricks import Bricks
from drops import Powerup

# States
STATE_INIT = "init"
STATE_RUNNING = "running"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
STATE_WIN = "win"
state = STATE_INIT

# Load configuration
if not config.load_config():
    print("Failed to load configuration.")
    sys.exit()

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("rogfonts", config.FONT_SIZE)
falling_powerups = []
active_powerups = []


# GAME LOOP
while True:
    text = None

    # State machine
    match state:
        case "init":
            # Initialize game objects
            ball = Ball(config.SCREEN_WIDTH/2,
                        config.SCREEN_HEIGHT - config.PADDLE_HEIGHT - 20 - config.BALL_RADIUS/2,
                        config.BALL_RADIUS,
                        0, 0,
                        config.COLORS['WHITE'])

            paddle = Paddle(config.SCREEN_WIDTH/2 - config.PADDLE_WIDTH/2,
                            config.SCREEN_HEIGHT - config.PADDLE_HEIGHT - 20,
                            config.PADDLE_WIDTH,
                            config.PADDLE_HEIGHT,
                            config.PADDLE_SPEED)

            bricks = Bricks(config.BRICK_ROWS,
                            config.BRICK_COLUMNS,
                            config.BRICK_SIZE,
                            config.COLORS['RED'])
            
            falling_powerups.clear()
            active_powerups.clear()
            
            text = "Press SPACE to start"

        case "running":
            ball.move(config.LEFT_BORDER, config.RIGHT_BORDER, config.TOP_BORDER)
            paddle.move(keys, config.LEFT_BORDER, config.RIGHT_BORDER)

            # Check for collisions
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1
                ball.dx += paddle.dx * 0.1

                # Ensure the ball doesn't get stuck in the paddle
                if ball.rect.bottom >= paddle.rect.top:
                    ball.rect.bottom = paddle.rect.top

            if bricks.check_collision(ball.rect):
                if not any(buff.type == 'fireball' for buff in active_powerups):
                    ball.dy *= -1

                if random.random() < config.DROP_RATE:
                    falling_powerups.append(Powerup.spawn_powerup(ball.rect.x,
                                                          ball.rect.y,
                                                          config.DROP_FALL_SPEED))

            for drop in falling_powerups[:]:
                drop.fall()
                
                if drop.rect.colliderect(paddle.rect):
                    drop.apply(ball, paddle)
                    active_powerups.append(drop)
                    falling_powerups.remove(drop)
                elif drop.rect.top > config.SCREEN_HEIGHT:
                    falling_powerups.remove(drop)

            # Clean expired powerups
            for buff in active_powerups[:]:
                buff.duration -= 1
                if buff.duration <= 0:
                    active_powerups.remove(buff)
                    Powerup.clean(buff.type, ball, paddle, active_powerups)

            # Check for game over condition
            if ball.rect.bottom >= config.BOTTOM_BORDER:
                state = STATE_GAME_OVER

            # Check for win condition
            if not bricks.grid:
                state = STATE_WIN

        case "paused":
            text = "PAUSED"

        case "game_over":
            text = "GAME OVER"

        case "win":
            text = "LEVEL COMPLETE"

    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if state == STATE_INIT:
                ball.dx = config.BALL_SPEED
                ball.dy = -config.BALL_SPEED
                state = STATE_RUNNING

            elif state == STATE_RUNNING:
                saved_dx = ball.dx
                saved_dy = ball.dy
                ball.dx = 0
                ball.dy = 0
                state = STATE_PAUSED

            elif state == STATE_PAUSED:
                ball.dx = saved_dx
                ball.dy = saved_dy
                state = STATE_RUNNING

            elif state == STATE_GAME_OVER or state == STATE_WIN:
                state = STATE_INIT

    # Render display objects
    screen.fill(config.COLORS['BLACK'])
    ball.draw(screen)
    paddle.draw(screen, config.COLORS['GRAY'])
    bricks.draw(screen)
    for drop in falling_powerups[:]:
        drop.draw(screen)
    if text:
        text = font.render(text, True, config.COLORS['WHITE'])
        screen.blit(text, (config.SCREEN_WIDTH // 2 - text.get_width() // 2,
                           config.SCREEN_HEIGHT // 2 - text.get_height() // 2))

    pygame.display.flip()
    clock.tick(config.FRAME_RATE)

# Mechatronikai szimuláció - BMEGEMINMMZ
# Ménes Zsombor - QTU3QF
# Brick Out Game

import pygame
import sys
from ball import Ball
from paddle import Paddle
from bricks import Bricks

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # standard HD resolution
LEFT_BORDER, RIGHT_BORDER = 0, SCREEN_WIDTH
TOP_BORDER, BOTTOM_BORDER = 0, SCREEN_HEIGHT
FONT_SIZE = 36
BALL_RADIUS = 20
BALL_SPEED = 5
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 16
PADDLE_SPEED = 8
BRICK_SIZE = 30
BRICK_ROWS = 4
BRICK_COLUMNS = 36

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (113, 121, 126)
RED = (255, 0, 0)

# States
STATE_INIT = "init"
STATE_RUNNING = "running"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"
state = STATE_INIT

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont("rogfonts", FONT_SIZE)

# GAME LOOP
while True:
    screen.fill(BLACK)

    # State machine
    match state:
        case "init":
            # Initialize game objects
            ball = Ball(SCREEN_WIDTH/2,
                        SCREEN_HEIGHT - PADDLE_HEIGHT - 20 - BALL_RADIUS/2,
                        BALL_RADIUS,
                        0, 0)

            paddle = Paddle(SCREEN_WIDTH/2 - PADDLE_WIDTH/2,
                            SCREEN_HEIGHT - PADDLE_HEIGHT - 20,
                            PADDLE_WIDTH,
                            PADDLE_HEIGHT,
                            PADDLE_SPEED)

            bricks = Bricks(BRICK_ROWS, BRICK_COLUMNS, BRICK_SIZE, RED)
            
            text = font.render("Press SPACE to start", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))

        case "running":
            ball.move(LEFT_BORDER, RIGHT_BORDER, TOP_BORDER)
            paddle.move(keys, LEFT_BORDER, RIGHT_BORDER)

            # Check for collisions
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1
                ball.dx += paddle.dx * 0.125

                # ensure the ball doesn't get stuck in the paddle
                if ball.rect.bottom >= paddle.rect.top:
                    ball.rect.bottom = paddle.rect.top

            if bricks.check_collision(ball.rect):
                ball.dy *= -1

            # Check for game over condition
            if ball.rect.bottom >= BOTTOM_BORDER:
                state = STATE_GAME_OVER

        case "paused":
            text = font.render("PAUSED", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))

        case "game_over":
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2,
                               SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if state == STATE_INIT:
                ball.dx = 0
                ball.dy = -BALL_SPEED
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

            elif state == STATE_GAME_OVER:
                state = STATE_INIT

    # Render game objects
    ball.draw(screen, WHITE)
    paddle.draw(screen, GRAY)
    bricks.draw(screen)

    pygame.display.flip()
    clock.tick(60)

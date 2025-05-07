# Mechatronikai szimuláció - BMEGEMINMMZ
# Ménes Zsombor - QTU3QF
# Brick Out Game

import pygame
import sys
from ball import Ball
from paddle import Paddle
from bricks import create_bricks, draw_bricks

# Define constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720  # standard HD resolution
LEFT_BORDER, RIGHT_BORDER = 0, SCREEN_WIDTH
TOP_BORDER, BOTTOM_BORDER = 0, SCREEN_HEIGHT
BALL_RADIUS = 20
PADDLE_WIDTH = 150
PADDLE_HEIGHT = 16
PADDLE_SPEED = 8

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (113, 121, 126)

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
font = pygame.font.SysFont("rogfonts", 36)

# GAME LOOP
while True:
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

            bricks = create_bricks(4, 30)
            
            text = font.render("Press SPACE to start", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        case "running":
            ball.move(LEFT_BORDER, RIGHT_BORDER, TOP_BORDER)
            paddle.move(keys, LEFT_BORDER, RIGHT_BORDER)

            # Check for collisions
            if ball.rect.colliderect(paddle.rect):
                ball.dy *= -1

            for brick in bricks:
                if ball.rect.colliderect(brick):
                    ball.dy *= -1
                    bricks.remove(brick)
                    break

            # Check for game over condition
            if ball.rect.bottom >= BOTTOM_BORDER:
                state = STATE_GAME_OVER

        case "paused":
            text = font.render("PAUSED", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        case "game_over":
            text = font.render("GAME OVER", True, WHITE)
            screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

    # Handle events
    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            if state == STATE_INIT:
                ball.dx = 5
                ball.dy = -5
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
    screen.fill(BLACK)
    ball.draw(screen, WHITE)
    paddle.draw(screen, GRAY)
    draw_bricks(screen, bricks)

    pygame.display.flip()
    clock.tick(60)

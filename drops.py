import pygame
import random

class Powerup:
    """
    Powerup drops

    Types of powerups:
        ball_speed_up: Increases the speed of the ball.
        ball_slow_down: Decreases the speed of the ball.
        paddle_speed_up: Increases the speed of the paddle.
        paddle_slow_down: Decreases the speed of the paddle.
        paddle_wide: Increases the width of the paddle.
        paddle_narrow: Decreases the width of the paddle.

    Attributes:
        x (int): x-coordinate of the drop's top-left corner
        y (int): y-coordinate of the drop's top-left corner
        type (str): type of powerup
        v (int): fall speed

    Methods:
        apply(ball, paddle): Applies the powerup effect.
        spawn_powerup(x, y, v): Spawns a drop with a random type.
        fall(): Moves the drop downwards.
        draw(screen): Renders the drop as a circle.
    """
    def __init__(self, x, y, v, type):
        self.speed = v
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        match type:
            case 'ball_speed_up':
                self.color = (255, 0, 0)
            case 'ball_slow_down':
                self.color = (0, 255, 0)
            case 'paddle_speed_up':
                self.color = (0, 0, 255)
            case 'paddle_slow_down':
                self.color = (255, 255, 0)
            case 'paddle_wide':
                self.color = (255, 0, 255)
            case 'paddle_narrow':
                self.color = (0, 255, 255)

    def apply(self, ball, paddle):
        # apply the powerup
        match self.type:
            case 'ball_speed_up':
                ball.dx *= 1.5
                ball.dy *= 1.5

            case 'ball_slow_down':
                ball.dx *= 0.5
                ball.dy *= 0.5

            case 'paddle_speed_up':
                paddle.speed *= 1.5

            case 'paddle_slow_down':
                paddle.speed *= 0.5

            case 'paddle_wide':
                paddle.rect.w += 50
                paddle.rect.x -= 25

            case 'paddle_narrow':
                paddle.rect.w -= 50
                paddle.rect.x += 25

    @staticmethod
    def spawn_powerup(x, y, v):
        # spawn a drop with a random type
        powerup_types = ['ball_speed_up',
                         'ball_slow_down',
                         'paddle_speed_up',
                         'paddle_slow_down',
                         'paddle_wide',
                         'paddle_narrow']

        type = random.choice(powerup_types)

        return Powerup(x, y, v, type)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

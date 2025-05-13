import pygame
import random
import config

class Powerup:
    """
    Powerup drops

    Types of powerups:
        ball_speed_up: Increases the speed of the ball.
        ball_slow_down: Decreases the speed of the ball.
        paddle_speed_up: Increases the speed of the paddle.
        paddle_slow_down: Decreases the speed of the paddle.
        paddle_grow: Increases the width of the paddle.
        paddle_shrink: Decreases the width of the paddle.
        fireball: Makes the ball pass through bricks.

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
    def __init__(self, x, y, v, type, duration):
        self.speed = v
        self.rect = pygame.Rect(x, y, 20, 20)
        self.type = type
        self.duration = duration * config.FRAME_RATE
        match type:
            case 'ball_speed_up':
                self.color = config.COLORS['GREEN']
            case 'ball_slow_down':
                self.color = config.COLORS['RED']
            case 'paddle_speed_up':
                self.color = config.COLORS['CYAN']
            case 'paddle_slow_down':
                self.color = config.COLORS['BLUE']
            case 'paddle_grow':
                self.color = config.COLORS['MAGENTA']
            case 'paddle_shrink':
                self.color = config.COLORS['YELLOW']
            case 'fireball':
                self.color = config.COLORS['ORANGE']

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

            case 'paddle_grow':
                paddle.rect.w += 50
                paddle.rect.x -= 25

            case 'paddle_shrink':
                paddle.rect.w -= 50
                paddle.rect.x += 25

            case 'fireball':
                ball.color = config.COLORS['ORANGE']
    
    @staticmethod
    def clean(type, ball, paddle, active_powerups):
        # remove the powerup
        match type:
            case 'ball_speed_up':
                ball.dx /= 1.5
                ball.dy /= 1.5
            
            case 'ball_slow_down':
                ball.dx /= 0.5
                ball.dy /= 0.5
            
            case 'paddle_speed_up':
                paddle.speed /= 1.5
            
            case 'paddle_slow_down':
                paddle.speed /= 0.5
            
            case 'fireball':
                Powerup.fireball_mode(active_powerups, ball)
            
            case _:
                pass

    @staticmethod
    def fireball_mode(active_powerups, ball):
        # if any fireball powerup is active the ball color doesn't change
        if not any(buff.type == 'fireball' for buff in active_powerups):
            ball.color = config.COLORS['WHITE']

    @staticmethod
    def spawn_powerup(x, y, v):
        # spawn a drop with a random type
        powerup_types = ['ball_speed_up',
                         'ball_slow_down',
                         'paddle_speed_up',
                         'paddle_slow_down',
                         'paddle_grow',
                         'paddle_shrink',
                         'fireball']
        
        type = random.choice(powerup_types)
        duration = config.POWERUP_DURATION

        return Powerup(x, y, v, type, duration)

    def fall(self):
        self.rect.y += self.speed

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

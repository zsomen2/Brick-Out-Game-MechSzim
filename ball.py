import pygame

class Ball:
    """
    Bouncing ball
    
    Attributes:
        x (int): x-coordinate of the ball's center
        y (int): y-coordinate of the ball's center
        r (int): radius of the ball
        dx (int): horizontal velocity of the ball
        dy (int): vertical velocity of the ball (positive = down, negative = up)
        color (tuple): RGB color of the ball
    
    Methods:
        move(screen_width): Updates the ball's position and handles bouncing off walls.
        draw(screen, color): Renders the ball as a circle.
    """

    def __init__(self, x, y, r, dx, dy, color):
        # tracking the ball's position with a rectangle
        # to simplify collision detection
        self.rect = pygame.Rect(x - r/2, y - r/2, r, r) 
        self.dx = dx
        self.dy = dy
        self.color = color
        self.fireball_mode = False

    def move(self, LEFT_BORDER, RIGHT_BORDER, TOP_BORDER):
        self.rect.x += self.dx
        self.rect.y += self.dy

        # bouncing off left, right and top walls
        if self.rect.left <= LEFT_BORDER or self.rect.right >= RIGHT_BORDER:
            self.dx *= -1
        if self.rect.top <= TOP_BORDER:
            self.dy *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, self.color, self.rect)

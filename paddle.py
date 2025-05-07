import pygame

class Paddle:
    """
    Paddle moved by the player

    Attributes:
        x (int): x-coordinate of the paddle's top-left corner
        y (int): y-coordinate of the paddle's top-left corner
        w (int): width of the paddle
        h (int): height of the paddle
        v (int): speed of the paddle

    Methods:
        move(keys, screen_width): Updates the paddle's position based on key presses.
        draw(screen): Renders the paddle as a rectangle.
    """

    def __init__(self, x, y, w, h, v):
        self.rect = pygame.Rect(x, y, w, h)
        self.speed = v
        self.dx = 0

    def move(self, keys, LEFT_BORDER, RIGHT_BORDER):
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.rect.left > LEFT_BORDER:
            self.rect.x -= self.speed
            self.dx = -self.speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.rect.right < RIGHT_BORDER:
            self.rect.x += self.speed
            self.dx = self.speed

    def draw(self, screen, color):
        pygame.draw.rect(screen, color, self.rect)

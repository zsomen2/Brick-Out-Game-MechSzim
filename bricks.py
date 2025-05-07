import pygame

class Bricks:
    """
    Grid of bricks

    Attributes:
        rows (int): number of rows
        cols (int): number of columns
        size (int): size of each brick
        color (tuple): brick color
        padding (int): padding between bricks
        x_offset (int): x offset for positioning the first brick
        y_offset (int): y offset for positioning the first brick

    Methods:
        create_grid(): Creates a grid of bricks based on the specified attributes.
        check_collision(ball): Checks if the ball collides with any of the bricks and removes it.
        draw(screen): Renders the grid of rectangles.
    """

    def __init__(self, rows, cols, size, color, padding=5, x_offset=13, y_offset=30):
        self.rows = rows
        self.cols = cols
        self.size = size
        self.color = color
        self.padding = padding
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.grid = self.create_grid()

    def create_grid(self):
        # creates a grid of rectangles
        bricks = []
        for row in range(self.rows):
            for col in range(self.cols):
                x = col * (self.size + self.padding) + self.x_offset
                y = row * (self.size + self.padding) + self.y_offset
                brick = pygame.Rect(x, y, self.size, self.size)
                bricks.append(brick)
        return bricks

    def check_collision(self, ball):
        # remove brick if the ball hits it
        for brick in self.grid:
            if ball.colliderect(brick):
                self.grid.remove(brick)
                return True
        return False

    def draw(self, screen):
        for brick in self.grid:
            pygame.draw.rect(screen, self.color, brick)

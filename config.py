import json
import sys
import os

# Config file path
if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    app_path = os.path.dirname(sys.executable)
    CONFIG_PATH = os.path.join(app_path, 'config.json')
    if not os.path.exists(CONFIG_PATH):
        CONFIG_PATH = os.path.join(sys._MEIPASS, 'config.json')
else:
    # Running as script
    CONFIG_PATH = "./config.json"

def load_config():
    """
    Load configuration from a JSON file.

    The configuration file includes screen dimensions,
    game constants & RGB color codes.
    """

    global SCREEN_WIDTH, SCREEN_HEIGHT
    global LEFT_BORDER, RIGHT_BORDER
    global TOP_BORDER, BOTTOM_BORDER
    global FRAME_RATE
    global FONT_SIZE
    global BALL_RADIUS, BALL_SPEED
    global PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
    global BRICK_SIZE, BRICK_ROWS, BRICK_COLUMNS
    global DROP_RATE, DROP_FALL_SPEED
    global POWERUP_DURATION
    global COLORS

    try:
        with open(CONFIG_PATH, 'r') as config_file:
            config = json.load(config_file)
    except (FileNotFoundError, json.JSONDecodeError, Exception):
        return False

    # Define borders
    SCREEN_WIDTH = config['SCREEN_WIDTH']
    SCREEN_HEIGHT = config['SCREEN_HEIGHT']
    LEFT_BORDER, RIGHT_BORDER = 0, SCREEN_WIDTH
    TOP_BORDER, BOTTOM_BORDER = 0, SCREEN_HEIGHT

    # Obtain frame rate
    FRAME_RATE = config['FRAME_RATE']

    # Load constants
    FONT_SIZE = config['FONT_SIZE']
    BALL_RADIUS = config['BALL_RADIUS']
    BALL_SPEED = config['BALL_SPEED']
    PADDLE_WIDTH = config['PADDLE_WIDTH']
    PADDLE_HEIGHT = config['PADDLE_HEIGHT']
    PADDLE_SPEED = config['PADDLE_SPEED']
    BRICK_SIZE = config['BRICK_SIZE']
    BRICK_ROWS = config['BRICK_ROWS']
    BRICK_COLUMNS = config['BRICK_COLUMNS']
    DROP_RATE = config['DROP_RATE']
    DROP_FALL_SPEED = config['DROP_FALL_SPEED']
    POWERUP_DURATION = config['POWERUP_DURATION']

    # Assign colors
    COLORS = {k: tuple(v) for k, v in config['COLORS'].items()}

    return True

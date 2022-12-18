from dataclasses import dataclass


@dataclass
class ConfigsStorage:

    # Screen configs:
    screen_width: int = 1600
    screen_height: int = 900
    FPS: int = 60

    # Bird configs:
    bird_speed: int = 0
    bird_acceleration: int = 0
    bird_Y_start_position: int = screen_height // 2
    bird_X_start_position: int = screen_width // 3

    # Pipes configs:
    pipe_distance_from_screen_border: int = 100
    pipe_start_width: int = screen_width - pipe_distance_from_screen_border
    pipe_width: int = 52  # Пиксели изображения трубы
    pipe_height: int = 320  # Пиксели изображения трубы
    top_pipe_start_height: int = 0
    bottom_pipe_start_height: int = screen_height - pipe_height
    pipe_speed: int = 3
    pipe_distance: int = pipe_distance_from_screen_border * 3

    # State configs:
    state: str = 'start'

    # Lives configs:
    lives: int = 3
    lives_bird_X_position: int = screen_width - 34
    lives_bird_Y_position: int = 15
    lives_X_position: int = lives_bird_X_position - 24
    lives_Y_position: int = 10

    # Scores configs:
    scores: int = 0
    scores_color: str = 'white'
    scores_X_position: int = 10
    scores_Y_position: int = 10
    scores_font_size: int = 50

    # Other configs
    background_speed: int = 1


class Configs(ConfigsStorage):

    def __init__(self):
        super(ConfigsStorage)

    def reset_speed_and_acceleration(self):
        self.bird_acceleration = ConfigsStorage.bird_acceleration
        self.bird_speed = ConfigsStorage.bird_speed

    def reset_start_position(self, bird):
        self.bird_Y_start_position += (self.screen_height // 2 - self.bird_Y_start_position) * 0.1
        bird.y = self.bird_Y_start_position

    def reset_lives_and_scores(self):
        self.lives = ConfigsStorage.lives
        self.scores = ConfigsStorage.scores

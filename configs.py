from dataclasses import dataclass


@dataclass
class ConfigsStorage:

    # Screen configs:
    screen_width: int = 1600
    screen_height: int = 900
    FPS: int = 60
    screen_fill_color: str = 'black'

    # Bird configs:
    bird_speed: int = 0
    bird_acceleration: int = 0
    bird_Y_start_position: int = screen_height // 2
    bird_X_start_position: int = screen_width // 3

    # Pipes configs:
    pipe_distance_from_screen_border: int = 100
    pipe_start_width: int = screen_width - pipe_distance_from_screen_border
    pipe_width: int = 52  # Пиксели изображения трубы
    top_pipe_start_height: int = 0
    pipe_speed: int = 3
    distance_between_pipes: int = pipe_distance_from_screen_border * 3
    pipe_speed_multiplier: float = 1.025
    pipes_gate_size: int = screen_height // 4
    pipes_gate_pos = int = screen_height // 2

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
    scores_base_points: int = 5
    scores_multiplier: int = 1

    # Start message image:
    start_message_image_width = 184
    start_message_image_height = 267
    start_message_X_position = screen_width / 2 - start_message_image_width / 2
    start_message_Y_position = screen_height / 2 - start_message_image_height / 2

    # Game over message:
    game_over_message_image_width = 192
    game_over_message_image_height = 42
    game_over_message_X_position = screen_width / 2 - game_over_message_image_width / 2
    game_over_message_Y_position = screen_height / 2 - game_over_message_image_height / 2

    # Record config:
    record_X_position = screen_width / 2 - 100
    record_Y_position = 10
    record_font_size: int = 50
    record_color: str = 'white'

    # Other configs
    background_speed: int = 1
    background_speed_multiplier: int = 2
    game_over_time: int = FPS * 4  # FPS * number of seconds before reboot
    state: str = 'start'


class Configs(ConfigsStorage):

    def __init__(self):
        super(ConfigsStorage)

    def reset_bird_speed_and_acceleration(self):
        self.bird_acceleration = ConfigsStorage.bird_acceleration
        self.bird_speed = ConfigsStorage.bird_speed

    def reset_bird_start_position(self, bird):
        if self.lives > 0:
            self.bird_Y_start_position += (self.screen_height // 2 - self.bird_Y_start_position) * 0.1
        else:
            self.bird_Y_start_position = ConfigsStorage.bird_Y_start_position
        bird.y = self.bird_Y_start_position

    def reset_lives_and_scores(self):
        self.lives = ConfigsStorage.lives
        self.scores = ConfigsStorage.scores
        self.scores_multiplier = ConfigsStorage.scores_multiplier

    def reset_pipes_and_background_speed(self):
        self.pipe_speed = ConfigsStorage.pipe_speed
        self.background_speed = ConfigsStorage.background_speed

    def reset_pipes_gate_pos(self):
        self.pipes_gate_pos = ConfigsStorage.pipes_gate_pos

from dataclasses import dataclass


@dataclass
class ConfigsStorage:

    # Screen configs:
    screen_width: int = 1920
    screen_height: int = 1080
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

    # Music:
    fly_sound_timer: int = 2
    main_theme_volume: float = 0.1

    # Paths:
    path_to_icon_picture: str = 'images/favicon.ico'
    path_to_background_picture: str = 'images/background-day.png'
    path_to_bird_picture: str = 'images/new_yellow.png'
    path_to_lives_bird_picture: str = 'images/yellow_bird.png'
    path_to_start_message_picture: str = 'images/start_message.png'
    path_to_game_over_message_picture: str = 'images/gameover.png'
    path_to_top_pipe_picture: str = 'images/rotated_green_pipe.png'
    path_to_bottom_pipe_picture: str = 'images/pipe-green.png'
    path_to_music: str = 'audio/main_theme.mp3'
    path_to_fall_sound: str = 'audio/swoosh.ogg'
    path_to_game_over_sound: str = 'audio/die.ogg'
    path_to_hit_sound: str = 'audio/hit.ogg'
    path_to_fly_sound: str = 'audio/wing.ogg'

    # GUI:
    gui_precondition_screen_width: int = 1200
    gui_precondition_screen_height: int = 800
    gui_precondition_screen_title: str = 'FlappyBird preconditions'

    gui_precondition_text_font: str = 'Times 20'
    gui_precondition_text_color: str = 'black'

    gui_precondition_label_X_start_position: int = 20
    gui_precondition_label_Y_start_position: int = 20
    gui_precondition_label_Y_distance_from_each_other: int = 60

    gui_precondition_entry_X_distance_from_label: int = (gui_precondition_label_X_start_position + 200)
    gui_precondition_entry_width: int = 10
    gui_precondition_entry_height: int = 40
    gui_precondition_entry_border_width: int = 4
    gui_precondition_entry_border_mode: str = 'outside'

    gui_precondition_default_button_distance_from_entry: int = 40
    gui_precondition_default_button_width: int = 20
    gui_precondition_default_button_border_width: int = 4
    gui_precondition_default_button_background_color: str = 'green'

    gui_precondition_lives_minimum: int = 1
    gui_precondition_lives_maximum: int = 9
    gui_precondition_lives_scale_width: int = 400

    gui_precondition_distance_between_radio_buttons: int = 20
    gui_precondition_radio_buttons_font: str = 'Times 15'

    gui_precondition_play_button_width: int = 10
    gui_precondition_play_button_height: int = 2
    gui_precondition_play_button_font: str = 'Times 40'
    gui_precondition_play_button_border_width: int = 4
    gui_precondition_play_button_background_color: str = 'red'

    gui_background_filetypes: tuple[tuple[str]] = (('PNG files', '*.png'), ('All files', '*'))
    gui_music_filetypes: tuple[tuple[str]] = (('MP3 files', '*.mp3'), ('All files', '*'))


class Configs(ConfigsStorage):

    def __init__(self):
        super(ConfigsStorage)

        self.lives_to_reset = None
        self._screen_resolutions_dict = {1: (1920, 1080), 2: (1600, 900), 3: (1536, 864), 4: (1440, 900),
                                         5: (1366, 768), 6: (1280, 720)}
        self._bird_colors_dict = {1: 'yellow', 2: 'red', 3: 'blue'}
        self._pipes_colors_dict = {1: 'green', 2: 'red'}
        self._game_difficulties_dict = {1: 'easy', 2: 'medium', 3: 'hard'}

    def update_configs_after_gui(self, difficulty_index: int, lives: int, bird_color_index: int, pipes_color_index: int,
                                 screen_resolution_index: int):

        # Сохраняем кол-во изначальных жизней птицы для корректного обновления при конце игры:
        self.lives_to_reset = lives

        self.lives = lives
        self.path_to_bird_picture = f'images/new_{self._bird_colors_dict[bird_color_index]}.png'
        self.path_to_lives_bird_picture = f'images/{self._bird_colors_dict[bird_color_index]}_bird.png'
        self.path_to_top_pipe_picture = f'images/rotated_{self._pipes_colors_dict[pipes_color_index]}_pipe.png'
        self.path_to_bottom_pipe_picture = f'images/pipe-{self._pipes_colors_dict[pipes_color_index]}.png'
        self.screen_width = self._screen_resolutions_dict[screen_resolution_index][0]
        self.screen_height = self._screen_resolutions_dict[screen_resolution_index][1]

        # Связанные с разрешением экрана конфиги, которые тоже необходимо обновить:
        self.bird_Y_start_position = self.screen_height // 2
        self.bird_X_start_position = self.screen_width // 3
        self.pipe_start_width = self.screen_width - self.pipe_distance_from_screen_border
        self.pipes_gate_size = self.screen_height // 4
        self.pipes_gate_pos = self.screen_height // 2
        self.lives_bird_X_position = self.screen_width - 34
        self.lives_X_position = self.lives_bird_X_position - 24
        self.start_message_X_position = self.screen_width / 2 - self.start_message_image_width / 2
        self.start_message_Y_position = self.screen_height / 2 - self.start_message_image_height / 2
        self.game_over_message_X_position = self.screen_width / 2 - self.game_over_message_image_width / 2
        self.game_over_message_Y_position = self.screen_height / 2 - self.game_over_message_image_height / 2

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
        self.lives = self.lives_to_reset
        self.scores = ConfigsStorage.scores
        self.scores_multiplier = ConfigsStorage.scores_multiplier

    def reset_pipes_and_background_speed(self):
        self.pipe_speed = ConfigsStorage.pipe_speed
        self.background_speed = ConfigsStorage.background_speed

    def reset_pipes_gate_pos(self):
        self.pipes_gate_pos = ConfigsStorage.pipes_gate_pos

    def reset_configs_after_exit(self):
        self.reset_pipes_gate_pos()
        self.reset_pipes_and_background_speed()
        self.reset_lives_and_scores()
        self.reset_bird_speed_and_acceleration()

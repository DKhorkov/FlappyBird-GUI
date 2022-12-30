import pygame
from PIL import Image
import os
import shutil
import random


class FlappyBirdGame:

    def __init__(self, configs, database):
        pygame.init()

        self._database = database
        self._configs = configs

        # Screen:
        self._screen = pygame.display.set_mode((self._configs.screen_width, self._configs.screen_height))
        pygame.display.set_caption('Flappy Bird')
        pygame.display.set_icon(pygame.image.load(self._configs.path_to_icon_picture))

        # Background:
        self._background_image = pygame.image.load(
            self._change_picture_size(self._configs.path_to_background_picture,
                                      necessary_height=self._configs.screen_height))
        self._background_image_width = self._background_image.get_width()
        self._background_image_height = self._background_image.get_height()
        self._backgrounds = []

        # Pipes:
        self._pipes = []
        self._counted_pipes_for_scores = []
        self._create_pipes_images()

        # Bird:
        self._bird = pygame.Rect(self._configs.bird_X_start_position, self._configs.bird_Y_start_position, 34, 24)
        self._bird_image = pygame.image.load(self._configs.path_to_bird_picture)
        self._frame = 0

        # Lives:
        self._lives = pygame.Rect(self._configs.lives_X_position, self._configs.lives_Y_position, 24, 34)
        self._lives_bird_rect = pygame.Rect(self._configs.lives_bird_X_position, self._configs.lives_bird_Y_position,
                                            34, 24)
        self._lives_bird_image = pygame.image.load(self._configs.path_to_lives_bird_picture)
        self._lives_image = None

        # Scores:
        self._scores_font = pygame.font.Font(None, self._configs.scores_font_size)

        # Start game:
        self._start_message_rect = pygame.Rect(self._configs.start_message_X_position,
                                               self._configs.start_message_Y_position,
                                               self._configs.start_message_image_width,
                                               self._configs.start_message_image_height)
        self._start_message_image = pygame.image.load(self._configs.path_to_start_message_picture)
        self._game_started = False

        # Game over:
        self._game_over_message_rect = pygame.Rect(self._configs.game_over_message_X_position,
                                                   self._configs.game_over_message_Y_position,
                                                   self._configs.game_over_message_image_width,
                                                   self._configs.game_over_message_image_height)
        self._game_over_message_image = pygame.image.load(self._configs.path_to_game_over_message_picture)

        # Record:
        self._record = self._configs.record
        self._record_font = pygame.font.Font(None, self._configs.scores_font_size)

        # Other:
        self._game_active = True
        self._timer = 0
        self._clock = pygame.time.Clock()

        # Music:
        pygame.mixer.music.load(self._configs.path_to_music)
        pygame.mixer.music.set_volume(self._configs.main_theme_volume)
        pygame.mixer.music.play(-1)  # -1, чтобы музыка играла бесконечно.

        # Sounds:
        self._fall_sound = pygame.mixer.Sound(self._configs.path_to_fall_sound)
        self._game_over_sound = pygame.mixer.Sound(self._configs.path_to_game_over_sound)
        self._hit_pipes_sounds = pygame.mixer.Sound(self._configs.path_to_hit_sound)
        self._fly_sound = pygame.mixer.Sound(self._configs.path_to_fly_sound)

    @staticmethod
    def _change_picture_size(path_to_picture, necessary_width=None, necessary_height=None):
        picture_name = path_to_picture.split('/')[-1]
        image = Image.open(path_to_picture)
        default_width, default_height = image.size
        if necessary_width is None and necessary_height is None:
            return path_to_picture

        if not os.path.exists('images/temporary_images'):
            os.mkdir('images/temporary_images')
        path_to_rendered_picture = rf'images/temporary_images/{picture_name}'
        if necessary_width is None:
            rendered_bg = image.resize((default_width, necessary_height))
            rendered_bg.save(path_to_rendered_picture)
        elif necessary_height is None:
            rendered_bg = image.resize((necessary_width, default_height))
            rendered_bg.save(path_to_rendered_picture)
        return path_to_rendered_picture

    def _create_pipes_images(self):
        """Метод загружает изображения для верхней и нижней трубы и проверяет его размеры. Если длина экрана за вычетом
        длины прохода между трубами больше, чем длина трубы, то изменяем длину труб, чтобы они красиво выглядели на
        экране и не было пробелов между краем экрана и началом картинки трубы."""

        self._top_pipe = pygame.image.load(self._configs.path_to_top_pipe_picture)
        self._bottom_pipe = pygame.image.load(self._configs.path_to_bottom_pipe_picture)
        pipe_height = self._top_pipe.get_height()
        if pipe_height - self._configs.pipes_gate_size < self._configs.screen_height:
            necessary_height = self._configs.screen_height - self._configs.pipes_gate_size
            self._top_pipe = pygame.image.load(self._change_picture_size(self._configs.path_to_top_pipe_picture,
                                                                         necessary_height=necessary_height))
            self._bottom_pipe = pygame.image.load(self._change_picture_size(self._configs.path_to_bottom_pipe_picture,
                                                                            necessary_height=necessary_height))

    def _create_pipes(self):
        """Трубы создаются если список труб пустой, либо если последние трубы в списке прошли больше дистанции на
        экране, чем расстояние между трубами.

        Также трубы рандомно смещаются относительно предыдущей пары труб."""

        if len(self._pipes) == 0 or \
                self._pipes[len(self._pipes) - 1].x < self._configs.screen_width - self._configs.distance_between_pipes:

            self._pipes.append(pygame.Rect(self._configs.pipe_start_width,
                                           self._configs.top_pipe_start_height,
                                           self._configs.pipe_width,
                                           self._configs.pipes_gate_pos - self._configs.pipes_gate_size // 2))
            self._pipes.append(pygame.Rect(self._configs.pipe_start_width,
                                           self._configs.pipes_gate_pos + self._configs.pipes_gate_size // 2,
                                           self._configs.pipe_width,
                                           self._configs.screen_height -
                                           (self._configs.pipes_gate_pos + self._configs.pipes_gate_size // 2)))
            self._configs.pipes_gate_pos += \
                random.choice((-self._configs.pipes_gate_size // 2, self._configs.pipes_gate_size // 2))

            # Меняем расположение прохода между трубами так, чтобы при этом сверху и снизу всегда была труба.
            if self._configs.pipes_gate_pos < self._configs.pipes_gate_size:
                self._configs.pipes_gate_pos = self._configs.pipes_gate_size
            elif self._configs.pipes_gate_pos > self._configs.screen_height - self._configs.pipes_gate_size:
                self._configs.pipes_gate_pos = self._configs.screen_height - self._configs.pipes_gate_size

    def _start_state_algorithm(self, pressed):
        if pressed and len(self._pipes) == 0:
            self._configs.state = 'play'
        self._configs.reset_bird_start_position(self._bird)

    def _fall_state_algorithm(self):
        self._configs.lives -= 1
        self._configs.reset_pipes_gate_pos()
        if self._configs.lives <= 0:
            self._configs.state = 'game_over'
            self._game_over_sound.play()
            self._timer = self._configs.game_over_time
        else:
            self._configs.state = 'start'
            self._configs.reset_bird_speed_and_acceleration()

    def _game_over_state_algorithm(self):
        self._move_bird()
        if self._timer == 0:
            self._configs.state = 'start'
            self._game_started = False
            self._pipes.clear()
            self._configs.reset_bird_start_position(self._bird)
            self._configs.reset_pipes_and_background_speed()
            self._configs.reset_lives_and_scores()
            self._configs.reset_bird_speed_and_acceleration()

    def _play_state_algorithm(self, pressed):
        if pressed:
            self._configs.bird_acceleration -= self._configs.bird_acceleration_factor
            if self._configs.fly_sound_timer == 0:
                self._fly_sound.play()
                self._configs.fly_sound_timer = 2
            else:
                self._configs.fly_sound_timer -= 1
        else:
            self._configs.bird_acceleration = 0

        self._move_bird()
        self._create_pipes()
        self._check_screen_border()
        self._check_collisions_and_update_scores()

    def _check_collisions_and_update_scores(self):
        """Проверка столкновений птицы с трубами и начисление очков."""

        for pipe in self._pipes:
            if self._bird.colliderect(pipe):
                self._configs.state = 'fall'
                self._hit_pipes_sounds.play()

            if pipe.right < self._bird.left and pipe not in self._counted_pipes_for_scores:
                self._counted_pipes_for_scores.append(pipe)

                # Экспоненциальное увеличение скорости движения труб и начисления очков:
                if self._pipes.index(pipe) % 2 == 0 and self._pipes.index(pipe) != 0:
                    self._configs.pipe_speed *= self._configs.pipe_speed_multiplier
                    self._configs.background_speed = \
                        self._configs.pipe_speed // self._configs.background_speed_multiplier
                    self._configs.scores_multiplier += 1

                self._configs.scores += self._configs.scores_base_points * self._configs.scores_multiplier
                self._check_record()

    def _check_screen_border(self):
        """Проверка достижения границы экрана."""

        if self._bird.top < 0 or self._bird.bottom > self._configs.screen_height:
            self._configs.state = 'fall'
            self._fall_sound.play()

    def _check_state(self, pressed):
        """Метод проверяет состояние игры. В зависимости от состояния определенные действия игрока будут менять данное
        состояние."""

        if self._configs.state == 'start':
            self._start_state_algorithm(pressed)

        elif self._configs.state == 'play':
            self._play_state_algorithm(pressed)

        elif self._configs.state == 'fall':
            self._fall_state_algorithm()

        elif self._configs.state == 'game_over':
            self._game_over_state_algorithm()

    def _check_record(self):
        if self._configs.scores > self._record:
            self._record = self._configs.scores

    @staticmethod
    def _get_pressed():
        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        pressed = keys[pygame.K_SPACE] or mouse[0]  # Нажатие пробела или ЛКМ
        return pressed

    def _check_fly(self):
        """Если кнопка нажата или держится зажатой, то производится действие."""

        pressed = self._get_pressed()
        self._check_state(pressed)

    def _check_exit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._game_active = False
                self._configs.reset_configs_after_exit()

        if event.type == pygame.QUIT:
            self._game_active = False
            self._configs.reset_configs_after_exit()

    def _check_events(self):
        """Метод проверяет события, влияющие на игру. Также метод обновляет таймер, относящийся к задержке перед началом
        игры или после смерти."""

        for event in pygame.event.get():
            self._check_exit(event)

        if not self._game_started:
            if self._get_pressed():
                self._game_started = True
        else:
            if self._timer > 0:
                self._timer -= 1

            """Меняем фрейм для создания анимации полета птицы. Деление с количеством ФПС сделано для плавности движения
            крыльев, иначе слишком быстрая анимация"""
            self._frame = (self._frame + 1 / (self._configs.FPS / 15)) % 4

            self._move_background()
            self._move_pipes()
            self._check_fly()

    def _move_background(self):
        """Данный метод двигает фон так, чтобы весь экран был покрыт изображением фона."""

        for i in range(len(self._backgrounds) - 1, -1, -1):
            background = self._backgrounds[i]
            background.x -= self._configs.background_speed

            if background.right < 0:
                self._backgrounds.remove(background)

            # Добавление картинок на фон так, чтобы весь экран был покрыт фоном.
            if self._backgrounds[len(self._backgrounds) - 1].right <= self._configs.screen_width:
                self._backgrounds.append(pygame.Rect(self._backgrounds[len(self._backgrounds) - 1].right, 0,
                                                     self._background_image_width, self._background_image_height))

    def _move_pipes(self):
        """Данный метод выполняет движение труб на экране. Движение труб происходит с конца по индексу в списке труб:"""

        for i in range(len(self._pipes) - 1, -1, -1):
            pipe = self._pipes[i]
            pipe.x -= self._configs.pipe_speed

            if pipe.right < 0:
                self._pipes.remove(pipe)

                if pipe in self._counted_pipes_for_scores:
                    self._counted_pipes_for_scores.remove(pipe)

    def _move_bird(self):
        """Метод изменяет положение птицы, создавая эффект падения/гравитации.

        Координата оси Y увеличивается на скорость полета.

        Скорость равна прежнему значению скорости + ускорению + 1,
        если ускорение равно 0, а также умножается на 0.9 для плавности игры."""

        self._configs.bird_Y_start_position += self._configs.bird_speed
        self._configs.bird_speed = (self._configs.bird_speed + self._configs.bird_acceleration + 1) * 0.9
        self._bird.y = self._configs.bird_Y_start_position

    def _draw_scores(self):
        scores_text = self._scores_font.render(f'Scores: {self._configs.scores}', True,
                                               pygame.Color(self._configs.scores_color))
        self._screen.blit(scores_text, (self._configs.scores_X_position, self._configs.scores_Y_position))

    def _draw_lives(self):
        self._lives_image = pygame.image.load(f'images/{self._configs.lives}.png')
        self._screen.blit(self._lives_image, self._lives)
        self._screen.blit(self._lives_bird_image, self._lives_bird_rect)

    def _draw_record(self):
        record_text = self._record_font.render(f'Record: {self._record}', True,
                                               pygame.Color(self._configs.record_color))
        self._screen.blit(record_text, (self._configs.record_X_position, self._configs.record_Y_position))

    def _draw_pipes(self):
        for pipe in self._pipes:
            if pipe.y == 0:
                pipe_image = self._top_pipe.get_rect(bottomleft=pipe.bottomleft)
                self._screen.blit(self._top_pipe, pipe_image)
            else:
                pipe_image = self._bottom_pipe.get_rect(topleft=pipe.topleft)
                self._screen.blit(self._bottom_pipe, pipe_image)

    def _draw_background(self):
        for background in self._backgrounds:
            self._screen.blit(self._background_image, background)

    def _update(self):
        """Метод обновляет экран и объекты, которые должны быть отрисованы на нем."""

        self._draw_background()
        self._draw_pipes()

        """Делим большое изображение 4 фреймов птицы так, чтобы получить одно маленькое. Также создаем вращение 
        изображения, когда птица летит вверх или падает вниз."""
        bird_image = self._bird_image.subsurface(34 * int(self._frame), 0, 34, 24)
        bird_image = pygame.transform.rotate(bird_image, -self._configs.bird_speed * 2)
        self._screen.blit(bird_image, self._bird)

        self._draw_lives()
        self._draw_scores()
        self._draw_record()

        if self._configs.state == 'game_over':
            self._screen.blit(self._game_over_message_image, self._game_over_message_rect)

        pygame.display.update()

    @staticmethod
    def _clear_temporary_images():
        if os.path.exists('images/temporary_images'):
            shutil.rmtree('images/temporary_images')

    def main(self):

        """Необходимо добавить первый рисунок фона в список фоновых рисунков, чтобы не было ошибки с индексированием в
        рамках движения фона в методе _check_events"""
        self._backgrounds.append(pygame.Rect(0, 0, self._background_image_width,
                                             self._background_image_height))
        while self._game_active:
            if not self._game_started:
                self._screen.fill(self._configs.screen_fill_color)
                self._screen.blit(self._start_message_image, self._start_message_rect)
                self._check_events()
                pygame.display.update()
            else:
                self._check_events()
                self._update()

            self._clock.tick(self._configs.FPS)

        self._clear_temporary_images()

        if self._record >= self._configs.record_from_database:
            self._database.upload_record(self._record)

        self._database.close_connection()

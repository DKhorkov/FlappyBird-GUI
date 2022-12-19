import pygame
from PIL import Image
import os
import shutil
import random

from configs import Configs


class FlappyBirdGame:

    def __init__(self):
        pygame.init()

        self._configs = Configs()

        self._frame = 0
        self._screen = pygame.display.set_mode((self._configs.screen_width, self._configs.screen_height))
        pygame.display.set_caption('Flappy Bird')

        self._background_image = pygame.image.load(
            self._change_picture_size('images/background-day.png', necessary_height=self._configs.screen_height))
        self._background_image_width = self._background_image.get_width()
        self._background_image_height = self._background_image.get_height()

        self._bird_image = pygame.image.load('images/new_yellow.png')
        self._create_pipes_images()

        self._clock = pygame.time.Clock()

        self._pipes = []
        self._counted_pipes_for_scores = []
        self._backgrounds = []

        self._game_active = True
        self._timer = self._configs.FPS  # Задержка в управлении перед началом игры или после смерти
        self._lives_image = None

        self._bird = pygame.Rect(self._configs.bird_X_start_position, self._configs.bird_Y_start_position, 34, 24)
        self._lives = pygame.Rect(self._configs.lives_X_position, self._configs.lives_Y_position, 24, 34)

        self._scores_font = pygame.font.Font(None, self._configs.scores_font_size)
        self._scores_bird_rect = pygame.Rect(self._configs.lives_bird_X_position, self._configs.lives_bird_Y_position,
                                             34, 24)
        self._scores_bird_image = pygame.image.load('images/yellow_bird.png')

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

        self._top_pipe = pygame.image.load('images/rotated_green_pipe.png')
        self._bottom_pipe = pygame.image.load('images/pipe-green.png')
        pipe_height = self._top_pipe.get_height()
        if pipe_height - self._configs.pipes_gate_size < self._configs.screen_height:
            necessary_height = self._configs.screen_height - self._configs.pipes_gate_size
            self._top_pipe = pygame.image.load(self._change_picture_size('images/rotated_green_pipe.png',
                                                                         necessary_height=necessary_height))
            self._bottom_pipe = pygame.image.load(self._change_picture_size('images/pipe-green.png',
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

    def _check_state(self, pressed):
        """Метод проверяет состояние игры. В зависимости от состояния определенные действия игрока будут менять данное
        состояние."""

        if self._configs.state == 'start':
            if pressed and self._timer == 0 and len(self._pipes) == 0:
                self._configs.state = 'play'
            self._configs.reset_start_position(self._bird)

        elif self._configs.state == 'play':
            if pressed:
                self._configs.bird_acceleration -= 2
            else:
                self._configs.bird_acceleration = 0

            self._move_bird()
            self._create_pipes()

            # Проверка достижения границы экрана:
            if self._bird.top < 0 or self._bird.bottom > self._configs.screen_height:
                self._configs.state = 'fall'

            # Проверка столкновений птицы с трубами и начисление очков:
            for pipe in self._pipes:
                if self._bird.colliderect(pipe):
                    self._configs.state = 'fall'

                if pipe.right < self._bird.left and pipe not in self._counted_pipes_for_scores:
                    self._counted_pipes_for_scores.append(pipe)

                    # Экспоненциальное увеличение скорости движения труб и начисления очков:
                    if self._pipes.index(pipe) % 2 == 0 and self._pipes.index(pipe) != 0:
                        self._configs.pipe_speed *= self._configs.pipe_speed_multiplier
                        self._configs.background_speed = \
                            self._configs.pipe_speed // self._configs.background_speed_multiplier
                        self._configs.scores_multiplier += 1

                    self._configs.scores += self._configs.scores_base_points * self._configs.scores_multiplier

        elif self._configs.state == 'fall':
            self._configs.lives -= 1
            self._configs.reset_pipes_gate_pos()
            if self._configs.lives <= 0:
                self._configs.state = 'game_over'
                self._timer = self._configs.game_over_time
            else:
                self._configs.state = 'start'
                self._configs.reset_speed_and_acceleration()

                # Обновляем таймер:
                self._timer = self._configs.FPS

        elif self._configs.state == 'game_over':
            self._move_bird()
            if self._timer == 0:
                self._game_active = False
                self._configs.reset_pipes_and_background_speed()
                self._configs.reset_lives_and_scores()

    def _check_fly(self):
        """Если кнопка нажата или держится зажатой, то производится действие."""

        mouse = pygame.mouse.get_pressed()
        keys = pygame.key.get_pressed()
        pressed = keys[pygame.K_SPACE] or mouse[0]  # Нажатие пробела или ЛКМ
        self._check_state(pressed)

    def _check_exit(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._game_active = False

    def _check_events(self):
        """Метод проверяет события, влияющие на игру. Также метод обновляет таймер, относящийся к задержке перед началом
        игры или после смерти."""

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._game_active = False

            self._check_exit(event)

        if self._timer > 0:
            self._timer -= 1

        """Меняем фрейм для создания анимации полета птицы. Деление с количеством ФПС сделано для плавности движения
        крыльев, иначе слишком быстрая анимация"""
        self._frame = (self._frame + 1 / (self._configs.FPS / 15)) % 4

        # Движение фона:
        for i in range(len(self._backgrounds) - 1, -1, -1):
            background = self._backgrounds[i]
            background.x -= self._configs.background_speed

            if background.right < 0:
                self._backgrounds.remove(background)

            """Добавление картинок на фон так, чтобы весь экран был покрыт фоном."""
            if self._backgrounds[len(self._backgrounds) - 1].right <= self._configs.screen_width:
                self._backgrounds.append(pygame.Rect(self._backgrounds[len(self._backgrounds) - 1].right, 0,
                                                     self._background_image_width, self._background_image_height))

        # Движение труб с конца по индексу в списке труб:
        for i in range(len(self._pipes) - 1, -1, -1):
            pipe = self._pipes[i]
            pipe.x -= self._configs.pipe_speed

            if pipe.right < 0:
                self._pipes.remove(pipe)

                if pipe in self._counted_pipes_for_scores:
                    self._counted_pipes_for_scores.remove(pipe)

        self._check_fly()

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
        self._screen.blit(self._scores_bird_image, self._scores_bird_rect)

    def _draw_lives(self):
        self._lives_image = pygame.image.load(f'images/{self._configs.lives}.png')
        self._screen.blit(self._lives_image, self._lives)

    def _update(self):
        """Метод обновляет экран и объекты, которые должны быть отрисованы на нем."""

        # Отрисовка фона:
        for background in self._backgrounds:
            self._screen.blit(self._background_image, background)

        # Отрисовка труб:
        for pipe in self._pipes:
            if pipe.y == 0:
                pipe_image = self._top_pipe.get_rect(bottomleft=pipe.bottomleft)
                self._screen.blit(self._top_pipe, pipe_image)
            else:
                pipe_image = self._bottom_pipe.get_rect(topleft=pipe.topleft)
                self._screen.blit(self._bottom_pipe, pipe_image)

        """Делим большое изображение 4 фреймов птицы так, чтобы получить одно маленькое. Также создаем вращение 
        изображения, когда птица летит вверх или падает вниз."""
        bird_image = self._bird_image.subsurface(34 * int(self._frame), 0, 34, 24)
        bird_image = pygame.transform.rotate(bird_image, -self._configs.bird_speed * 2)
        self._screen.blit(bird_image, self._bird)

        self._draw_lives()
        self._draw_scores()

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
            self._check_events()

            self._update()
            self._clock.tick(self._configs.FPS)

        self._clear_temporary_images()


if __name__ == '__main__':
    game = FlappyBirdGame()
    game.main()

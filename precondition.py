import tkinter
from tkinter import filedialog
import pickle

from game import FlappyBirdGame


class PreconditionsGUI:

    def __init__(self, database, configs):
        self._database = database
        self._configs = configs
        self._last_configs = {}

        self._precondition_window = tkinter.Tk()

        # Для целей работы на Windows:
        try:
            self._precondition_window.attributes('-zoomed', True)  # Full screen
        except tkinter.TclError:
            self._precondition_window.attributes('-fullscreen', True)  # Full screen

        self._precondition_window_width, self._precondition_window_height = self._precondition_window.wm_maxsize()
        self._precondition_window.title(self._configs.gui_precondition_screen_title)
        self._precondition_window.geometry(f'{self._configs.gui_precondition_screen_width}x'
                                           f'{self._configs.gui_precondition_screen_height}')

        self._difficulty = tkinter.IntVar()
        self._difficulty.set(1)
        self._bird_color = tkinter.IntVar()
        self._bird_color.set(1)
        self._pipes_color = tkinter.IntVar()
        self._pipes_color.set(1)
        self._screen_resolution = tkinter.IntVar()
        self._screen_resolution.set(1)

    def _create_and_place_labels(self):
        self._create_labels()
        self._place_labels()

    def _create_and_place_entries(self):
        self._create_entries()
        self._place_entries()

    def _create_and_place_buttons(self):
        self._create_buttons()
        self._place_buttons()

    def _create_labels(self):
        self._difficulty_label = tkinter.Label(self._precondition_window, text='Difficulty: ',
                                               font=self._configs.gui_precondition_text_font,
                                               fg=self._configs.gui_precondition_text_color)
        self._lives_label = tkinter.Label(self._precondition_window, text='Number of lives: ',
                                          font=self._configs.gui_precondition_text_font,
                                          fg=self._configs.gui_precondition_text_color)
        self._bird_color_label = tkinter.Label(self._precondition_window, text='Bird color: ',
                                               font=self._configs.gui_precondition_text_font,
                                               fg=self._configs.gui_precondition_text_color)
        self._pipes_color_label = tkinter.Label(self._precondition_window, text='Pipes color: ',
                                                font=self._configs.gui_precondition_text_font,
                                                fg=self._configs.gui_precondition_text_color)
        self._background_label = tkinter.Label(self._precondition_window, text='Background: ',
                                               font=self._configs.gui_precondition_text_font,
                                               fg=self._configs.gui_precondition_text_color)
        self._background_picture_label = tkinter.Label(self._precondition_window,
                                                       text=f'{self._configs.path_to_background_picture}',
                                                       font=self._configs.gui_precondition_text_font,
                                                       fg=self._configs.gui_precondition_text_color)
        self._music_label = tkinter.Label(self._precondition_window, text='Music: ',
                                          font=self._configs.gui_precondition_text_font,
                                          fg=self._configs.gui_precondition_text_color)
        self._music_chosen_label = tkinter.Label(self._precondition_window,
                                                 text=f'{self._configs.path_to_music}',
                                                 font=self._configs.gui_precondition_text_font,
                                                 fg=self._configs.gui_precondition_text_color)
        self._screen_resolution_label = tkinter.Label(self._precondition_window, text='Screen resolution: ',
                                                      font=self._configs.gui_precondition_text_font,
                                                      fg=self._configs.gui_precondition_text_color)

        self._labels = [self._difficulty_label, self._lives_label, self._bird_color_label, self._pipes_color_label,
                        self._background_label, self._background_picture_label, self._music_label,
                        self._music_chosen_label, self._screen_resolution_label]

    def _place_labels(self):
        self._difficulty_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                     y=self._configs.gui_precondition_label_Y_start_position)
        self._lives_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                y=int(self._difficulty_label.place_info()['y']) +
                                  self._configs.gui_precondition_label_Y_distance_from_each_other)
        self._bird_color_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                     y=int(self._lives_label.place_info()['y']) +
                                       self._configs.gui_precondition_label_Y_distance_from_each_other)
        self._pipes_color_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                      y=int(self._bird_color_label.place_info()['y']) +
                                        self._configs.gui_precondition_label_Y_distance_from_each_other)
        self._background_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                     y=int(self._pipes_color_label.place_info()['y']) +
                                       self._configs.gui_precondition_label_Y_distance_from_each_other)
        self._background_picture_label.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                             y=int(self._background_label.place_info()['y']))
        self._music_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                y=int(self._background_label.place_info()['y']) +
                                  self._configs.gui_precondition_label_Y_distance_from_each_other)
        self._music_chosen_label.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                       y=int(self._music_label.place_info()['y']))
        self._screen_resolution_label.place(x=self._configs.gui_precondition_label_X_start_position,
                                            y=int(self._music_label.place_info()['y']) +
                                              self._configs.gui_precondition_label_Y_distance_from_each_other)

    def _create_entries(self):
        self._lives_entry = tkinter.Scale(self._precondition_window,
                                          from_=self._configs.gui_precondition_lives_minimum,
                                          to=self._configs.gui_precondition_lives_maximum,
                                          orient=tkinter.HORIZONTAL)

        self._create_difficulty_variants()
        self._create_bird_color_variants()
        self._create_pipes_color_variants()
        self._create_screen_resolution_variants()

    def _create_difficulty_variants(self):
        self._easy_difficulty = tkinter.Radiobutton(self._precondition_window, text='Easy',
                                                    variable=self._difficulty, value=1,
                                                    font=self._configs.gui_precondition_radio_buttons_font)
        self._medium_difficulty = tkinter.Radiobutton(self._precondition_window, text='Medium',
                                                      variable=self._difficulty, value=2,
                                                      font=self._configs.gui_precondition_radio_buttons_font)
        self._hard_difficulty = tkinter.Radiobutton(self._precondition_window, text='Hard',
                                                    variable=self._difficulty, value=3,
                                                    font=self._configs.gui_precondition_radio_buttons_font)

    def _create_bird_color_variants(self):
        self._yellow_bird = tkinter.Radiobutton(self._precondition_window, text='Yellow',
                                                variable=self._bird_color, value=1,
                                                font=self._configs.gui_precondition_radio_buttons_font)
        self._red_bird = tkinter.Radiobutton(self._precondition_window, text='Red',
                                             variable=self._bird_color, value=2,
                                             font=self._configs.gui_precondition_radio_buttons_font)
        self._blue_bird = tkinter.Radiobutton(self._precondition_window, text='Blue',
                                              variable=self._bird_color, value=3,
                                              font=self._configs.gui_precondition_radio_buttons_font)

    def _create_pipes_color_variants(self):
        self._green_pipes = tkinter.Radiobutton(self._precondition_window, text='Green',
                                                variable=self._pipes_color, value=1,
                                                font=self._configs.gui_precondition_radio_buttons_font)
        self._red_pipes = tkinter.Radiobutton(self._precondition_window, text='Red',
                                              variable=self._pipes_color, value=2,
                                              font=self._configs.gui_precondition_radio_buttons_font)

    def _create_screen_resolution_variants(self):
        self._1920x1080 = tkinter.Radiobutton(self._precondition_window, text='1920x1080',
                                              variable=self._screen_resolution, value=1,
                                              font=self._configs.gui_precondition_radio_buttons_font)
        self._1600x900 = tkinter.Radiobutton(self._precondition_window, text='1600x900',
                                             variable=self._screen_resolution, value=2,
                                             font=self._configs.gui_precondition_radio_buttons_font)
        self._1536x864 = tkinter.Radiobutton(self._precondition_window, text='1536x864',
                                             variable=self._screen_resolution, value=3,
                                             font=self._configs.gui_precondition_radio_buttons_font)
        self._1440x900 = tkinter.Radiobutton(self._precondition_window, text='1440x900',
                                             variable=self._screen_resolution, value=4,
                                             font=self._configs.gui_precondition_radio_buttons_font)
        self._1366x768 = tkinter.Radiobutton(self._precondition_window, text='1366x768',
                                             variable=self._screen_resolution, value=5,
                                             font=self._configs.gui_precondition_radio_buttons_font)
        self._1280x720 = tkinter.Radiobutton(self._precondition_window, text='1280x720',
                                             variable=self._screen_resolution, value=6,
                                             font=self._configs.gui_precondition_radio_buttons_font)

    def _place_entries(self):
        self._lives_entry.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                y=int(self._lives_label.place_info()['y']) - self._lives_label.winfo_reqheight() // 2,
                                height=self._configs.gui_precondition_entry_height,
                                bordermode=self._configs.gui_precondition_entry_border_mode,
                                width=self._configs.gui_precondition_lives_scale_width)

        self._place_difficulty_variants()
        self._place_bird_color_variants()
        self._place_pipes_color_variants()
        self._place_screen_resolution_variants()

    def _place_difficulty_variants(self):
        self._easy_difficulty.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                    y=int(self._difficulty_label.place_info()['y']) +
                                      self._difficulty_label.winfo_reqheight() // 6)
        self._medium_difficulty.place(x=int(self._easy_difficulty.place_info()['x']) +
                                        self._easy_difficulty.winfo_reqwidth() +
                                        self._configs.gui_precondition_distance_between_radio_buttons,
                                      y=int(self._difficulty_label.place_info()['y']) +
                                        self._difficulty_label.winfo_reqheight() // 6)
        self._hard_difficulty.place(x=int(self._medium_difficulty.place_info()['x']) +
                                      self._medium_difficulty.winfo_reqwidth() +
                                      self._configs.gui_precondition_distance_between_radio_buttons,
                                    y=int(self._difficulty_label.place_info()['y']) +
                                      self._difficulty_label.winfo_reqheight() // 6)

    def _place_bird_color_variants(self):
        self._yellow_bird.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                y=int(self._bird_color_label.place_info()['y']) +
                                  self._bird_color_label.winfo_reqheight() // 6)
        self._red_bird.place(x=int(self._yellow_bird.place_info()['x']) +
                               self._yellow_bird.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._bird_color_label.place_info()['y']) +
                               self._bird_color_label.winfo_reqheight() // 6)
        self._blue_bird.place(x=int(self._red_bird.place_info()['x']) +
                                self._red_bird.winfo_reqwidth() +
                                self._configs.gui_precondition_distance_between_radio_buttons,
                              y=int(self._bird_color_label.place_info()['y']) +
                                self._bird_color_label.winfo_reqheight() // 6)

    def _place_pipes_color_variants(self):
        self._green_pipes.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                                y=int(self._pipes_color_label.place_info()['y']) +
                                  self._pipes_color_label.winfo_reqheight() // 6)
        self._red_pipes.place(x=int(self._green_pipes.place_info()['x']) +
                                self._green_pipes.winfo_reqwidth() +
                                self._configs.gui_precondition_distance_between_radio_buttons,
                              y=int(self._pipes_color_label.place_info()['y']) +
                                self._pipes_color_label.winfo_reqheight() // 6)

    def _place_screen_resolution_variants(self):
        self._1920x1080.place(x=self._configs.gui_precondition_entry_X_distance_from_label,
                              y=int(self._screen_resolution_label.place_info()['y']) +
                                self._screen_resolution_label.winfo_reqheight() // 6)
        self._1600x900.place(x=int(self._1920x1080.place_info()['x']) + self._1920x1080.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._screen_resolution_label.place_info()['y']) +
                               self._screen_resolution_label.winfo_reqheight() // 6)
        self._1536x864.place(x=int(self._1600x900.place_info()['x']) + self._1600x900.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._screen_resolution_label.place_info()['y']) +
                               self._screen_resolution_label.winfo_reqheight() // 6)
        self._1440x900.place(x=int(self._1536x864.place_info()['x']) + self._1536x864.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._screen_resolution_label.place_info()['y']) +
                               self._screen_resolution_label.winfo_reqheight() // 6)
        self._1366x768.place(x=int(self._1440x900.place_info()['x']) + self._1440x900.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._screen_resolution_label.place_info()['y']) +
                               self._screen_resolution_label.winfo_reqheight() // 6)
        self._1280x720.place(x=int(self._1366x768.place_info()['x']) + self._1366x768.winfo_reqwidth() +
                               self._configs.gui_precondition_distance_between_radio_buttons,
                             y=int(self._screen_resolution_label.place_info()['y']) +
                               self._screen_resolution_label.winfo_reqheight() // 6)

    def _create_buttons(self):
        self._change_background_picture_button = tkinter.Button(self._precondition_window,
                                                                text='Change background picture',
                                                                width=self._configs.
                                                                gui_precondition_default_button_width,
                                                                command=self._change_background,
                                                                borderwidth=self._configs.
                                                                gui_precondition_default_button_border_width,
                                                                background=self._configs.
                                                                gui_precondition_default_button_background_color)

        self._change_music_button = tkinter.Button(self._precondition_window,
                                                   text='Change music',
                                                   width=self._configs.
                                                   gui_precondition_default_button_width,
                                                   command=self._change_music,
                                                   borderwidth=self._configs.
                                                   gui_precondition_default_button_border_width,
                                                   background=self._configs.
                                                   gui_precondition_default_button_background_color)
        self._play_button = tkinter.Button(self._precondition_window,
                                           text='Play',
                                           width=self._configs.gui_precondition_play_button_width,
                                           height=self._configs.gui_precondition_play_button_height,
                                           font=self._configs.gui_precondition_play_button_font,
                                           command=self._play,
                                           borderwidth=self._configs.gui_precondition_play_button_border_width,
                                           background=self._configs.gui_precondition_play_button_background_color)

        self._buttons = [self._change_background_picture_button, self._change_music_button, self._play_button]

    def _place_buttons(self):
        self._change_background_picture_button.place(x=self._configs.gui_precondition_entry_X_distance_from_label +
                                                       self._background_picture_label.winfo_reqwidth() +
                                                       self._configs.gui_precondition_default_button_distance_from_entry,
                                                     y=self._background_picture_label.place_info()['y'])
        self._change_music_button.place(x=self._configs.gui_precondition_entry_X_distance_from_label +
                                          self._music_chosen_label.winfo_reqwidth() +
                                          self._configs.gui_precondition_default_button_distance_from_entry,
                                        y=self._music_label.place_info()['y'])
        self._play_button.place(x=self._precondition_window_width // 2 - self._play_button.winfo_reqwidth() / 3 * 2,
                                y=int(self._screen_resolution_label.place_info()['y']) +
                                  self._screen_resolution_label.winfo_reqheight() +
                                  (self._precondition_window_height -
                                   int(self._screen_resolution_label.place_info()['y']) -
                                   self._screen_resolution_label.winfo_reqheight()) // 8)

    def _change_background(self):
        self._background_picture_browser = filedialog.Open(filetypes=self._configs.gui_background_filetypes)
        path_to_background = self._background_picture_browser.show()
        if path_to_background != '' and path_to_background != ():
            self._configs.path_to_background_picture = path_to_background
            self._destroy_labels_and_buttons()
            self._create_and_place_labels()
            self._create_and_place_buttons()

    def _change_music(self):
        self._music_browser = filedialog.Open(filetypes=self._configs.gui_music_filetypes)
        path_to_music = self._music_browser.show()
        if path_to_music != '' and path_to_music != ():
            self._configs.path_to_music = path_to_music
            self._destroy_labels_and_buttons()
            self._create_and_place_labels()
            self._create_and_place_buttons()

    def _fill_last_configs(self, difficulty_index, lives, bird_color_index, pipes_color_index, screen_resolution_index):
        self._last_configs['difficulty_index'] = difficulty_index
        self._last_configs['lives'] = lives
        self._last_configs['bird_color_index'] = bird_color_index
        self._last_configs['pipes_color_index'] = pipes_color_index
        self._last_configs['screen_resolution_index'] = screen_resolution_index
        self._last_configs['path_to_background'] = self._configs.path_to_background_picture
        self._last_configs['path_to_music'] = self._configs.path_to_music

    def _get_data_from_gui_fields(self):
        self._difficulty_index = self._difficulty.get()
        self._lives = int(self._lives_entry.get())
        self._bird_color_index = self._bird_color.get()
        self._pipes_color_index = self._pipes_color.get()
        self._screen_resolution_index = self._screen_resolution.get()

    def _upload_data_to_database(self):
        self._database.upload_last_config(pickle.dumps(self._last_configs))
        self._database.upload_difficulty(self._configs.game_difficulties_dict[self._difficulty_index])
        screen_resolution = "x".join(str(val) for val in
                                     self._configs.screen_resolutions_dict[self._screen_resolution_index])
        self._database.upload_screen_resolution(screen_resolution)
        self._database.upload_main(self._lives)

    def _check_record(self):
        record_on_current_configs = self._database.check_record_existence()
        self._configs.record = record_on_current_configs
        self._configs.record_from_database = record_on_current_configs

    def _play(self):
        self._get_data_from_gui_fields()

        self._fill_last_configs(self._difficulty_index, self._lives, self._bird_color_index,
                                self._pipes_color_index, self._screen_resolution_index)
        self._upload_data_to_database()
        self._check_record()

        self._configs.update_configs_after_gui(self._difficulty_index, self._lives, self._bird_color_index,
                                               self._pipes_color_index, self._screen_resolution_index)
        self._precondition_window.destroy()
        flappy_bird_game = FlappyBirdGame(self._configs, self._database)
        flappy_bird_game.main()

    def _destroy_labels_and_buttons(self):
        for label in self._labels:
            label.destroy()
        for button in self._buttons:
            button.destroy()

    def main(self):
        self._create_and_place_labels()
        self._create_and_place_entries()
        self._create_and_place_buttons()
        self._precondition_window.mainloop()

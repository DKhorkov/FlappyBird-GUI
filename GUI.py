import tkinter
from tkinter import filedialog
from configs import Configs
from game import FlappyBirdGame


class GUI:

    def __init__(self):
        self._configs = Configs()

        self._precondition_window = tkinter.Tk()
        self._precondition_window.attributes('-zoomed', True)  # Full screen
        self._precondition_window_width, self._precondition_window_height = self._precondition_window.wm_maxsize()
        self._precondition_window.title(self._configs.gui_precondition_screen_title)
        self._precondition_window.geometry(f'{self._configs.gui_precondition_screen_width}x'
                                           f'{self._configs.gui_precondition_screen_height}')

        self._radio_buttons = []
        self._difficulty = tkinter.IntVar()
        self._difficulty.set(1)
        self._bird_color = tkinter.IntVar()
        self._bird_color.set(1)
        self._pipes_color = tkinter.IntVar()
        self._pipes_color.set(1)
        self._screen_resolution = tkinter.IntVar()
        self._screen_resolution.set(1)

        self._entries = []

        self._create_and_place()

    def _create_and_place(self):
        self._create_labels()
        self._place_labels()
        self._create_entries()
        self._place_entries()
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
        self._entries.append(self._lives_entry)

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
        self._radio_buttons.append(self._easy_difficulty)
        self._radio_buttons.append(self._medium_difficulty)
        self._radio_buttons.append(self._hard_difficulty)

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
        self._radio_buttons.append(self._yellow_bird)
        self._radio_buttons.append(self._red_bird)
        self._radio_buttons.append(self._blue_bird)

    def _create_pipes_color_variants(self):
        self._green_pipes = tkinter.Radiobutton(self._precondition_window, text='Green',
                                                variable=self._pipes_color, value=1,
                                                font=self._configs.gui_precondition_radio_buttons_font)
        self._red_pipes = tkinter.Radiobutton(self._precondition_window, text='Red',
                                              variable=self._pipes_color, value=2,
                                              font=self._configs.gui_precondition_radio_buttons_font)
        self._radio_buttons.append(self._green_pipes)
        self._radio_buttons.append(self._red_pipes)

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

        self._radio_buttons.append(self._1920x1080)
        self._radio_buttons.append(self._1600x900)
        self._radio_buttons.append(self._1536x864)
        self._radio_buttons.append(self._1440x900)
        self._radio_buttons.append(self._1366x768)
        self._radio_buttons.append(self._1280x720)

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
            self._destroy_labels_entries_radiobuttons_and_buttons()
            self._create_and_place()

    def _change_music(self):
        self._music_browser = filedialog.Open(filetypes=self._configs.gui_music_filetypes)
        path_to_music = self._music_browser.show()
        if path_to_music != '' and path_to_music != ():
            self._configs.path_to_music = path_to_music
            self._destroy_labels_entries_radiobuttons_and_buttons()
            self._create_and_place()

    def _play(self):
        difficulty_index = self._difficulty.get()
        lives = self._lives_entry.get()
        bird_color_index = self._bird_color.get()
        pipes_color_index = self._pipes_color.get()
        screen_resolution_index = self._screen_resolution.get()
        self._configs.update_configs_after_gui(difficulty_index, int(lives), bird_color_index, pipes_color_index,
                                               screen_resolution_index)
        self._precondition_window.destroy()
        flappy_bird_game = FlappyBirdGame(self._configs)
        flappy_bird_game.main()

    def _destroy_labels_entries_radiobuttons_and_buttons(self):
        for label in self._labels:
            label.destroy()
        for entry in self._entries:
            entry.destroy()
        for button in self._buttons:
            button.destroy()
        for radiobutton in self._radio_buttons:
            radiobutton.destroy()

    def main(self):
        self._precondition_window.mainloop()


if __name__ == '__main__':
    gui = GUI()
    gui.main()

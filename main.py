import os
import tkinter
from tkinter import END
from tkinter import messagebox as msg
import pickle
from hashlib import blake2b

from configs import Configs
from database import DataBase
from precondition import PreconditionsGUI
from game import FlappyBirdGame


class MainGUI:

    def __init__(self):
        self._database = DataBase()
        self._configs = Configs()
        self._main_window = tkinter.Tk()
        self._main_window.title(self._configs.gui_main_screen_title)
        self._main_window.geometry(f'{self._configs.gui_main_screen_width}x{self._configs.gui_main_screen_height}')

    def _create_and_place(self):
        self._create_labels()
        self._place_labels()
        self._create_entries()
        self._place_entries()
        self._create_buttons()
        self._place_buttons()

    def _create_labels(self):
        self._username_label = tkinter.Label(self._main_window, text='Username: ',
                                             font=self._configs.gui_main_text_font,
                                             fg=self._configs.gui_main_text_color)
        self._password_label = tkinter.Label(self._main_window, text='Password: ',
                                             font=self._configs.gui_main_text_font,
                                             fg=self._configs.gui_main_text_color)

    def _place_labels(self):
        self._username_label.place(x=self._configs.gui_main_label_X_start_position,
                                   y=self._configs.gui_main_label_Y_start_position)
        self._password_label.place(x=self._configs.gui_main_label_X_start_position,
                                   y=int(self._username_label.place_info()['y']) +
                                     self._configs.gui_main_label_Y_distance_from_each_other)

    def _create_entries(self):
        self._username_entry = tkinter.Entry(self._main_window, width=self._configs.gui_main_entry_width,
                                             borderwidth=self._configs.gui_main_entry_border_width)
        self._password_entry = tkinter.Entry(self._main_window, width=self._configs.gui_main_entry_width,
                                             borderwidth=self._configs.gui_main_entry_border_width)

    def _place_entries(self):
        self._username_entry.place(x=self._configs.gui_main_entry_X_distance_from_label,
                                   y=int(self._username_label.place_info()['y']) -
                                     self._username_label.winfo_reqheight() // 6,
                                   height=self._configs.gui_main_entry_height,
                                   bordermode=self._configs.gui_main_entry_border_mode)
        self._password_entry.place(x=self._configs.gui_main_entry_X_distance_from_label,
                                   y=int(self._password_label.place_info()['y']) -
                                     self._password_label.winfo_reqheight() // 6,
                                   height=self._configs.gui_main_entry_height,
                                   bordermode=self._configs.gui_main_entry_border_mode)

    def _create_buttons(self):
        self._login_button = tkinter.Button(self._main_window, text='Login',
                                            width=self._configs.gui_main_default_button_width,
                                            command=self._login,
                                            borderwidth=self._configs.
                                            gui_main_default_button_border_width,
                                            background=self._configs.
                                            gui_main_login_button_background_color)
        self._register_button = tkinter.Button(self._main_window, text='Register',
                                               width=self._configs.gui_main_default_button_width,
                                               command=self._register,
                                               borderwidth=self._configs.
                                               gui_main_default_button_border_width,
                                               background=self._configs.
                                               gui_main_register_button_background_color)

    def _place_buttons(self):
        # Располагаем кнопки прямо под полем дял ввода пароля посередине:
        self._login_button.place(x=int(self._password_entry.place_info()['x']) +
                                   (self._password_entry.winfo_reqwidth() -
                                    self._login_button.winfo_reqwidth()) / 2,
                                 y=int(self._password_entry.place_info()['y']) +
                                   self._password_entry.winfo_reqheight() +
                                   self._configs.gui_main_default_button_Y_distance_from_entry)
        self._register_button.place(x=self._login_button.place_info()['x'],
                                    y=int(self._login_button.place_info()['y']) +
                                      self._login_button.winfo_reqheight() +
                                      self._configs.gui_main_default_button_Y_distance_from_each_other)

    def _get_username_and_hashed_password(self):
        entered_username = self._username_entry.get()
        entered_password = self._password_entry.get()
        self._clear_entries()
        hashed_password = blake2b(entered_password.encode(), digest_size=self._configs.hash_len).hexdigest()
        return entered_username, hashed_password

    @staticmethod
    def _parse_last_configs_for_user(last_configs):
        parsed_configs_list = []
        for key, value in last_configs.items():
            line = f'{key}: {value}'
            parsed_configs_list.append(line)
        parsed_configs = '\n\n'.join(parsed_configs_list)
        return parsed_configs

    def _upload_data_to_database(self, difficulty_index, screen_resolution_index, lives):
        self._database.upload_difficulty(self._configs.game_difficulties_dict[difficulty_index])
        screen_resolution = "x".join(str(val) for val in self._configs.screen_resolutions_dict[screen_resolution_index])
        self._database.upload_screen_resolution(screen_resolution)
        self._database.upload_main(lives)

    def _check_record(self):
        record_on_current_configs = self._database.check_record_existence()
        self._configs.record = record_on_current_configs
        self._configs.record_from_database = record_on_current_configs

    def _login(self):
        user_exists, valid_password = self._database.check_user_existence(*self._get_username_and_hashed_password())
        if user_exists and valid_password:
            last_config_exists, last_configs = self._database.check_configs_existence()
            if last_config_exists:
                unpacked_configs = pickle.loads(last_configs)
                parsed_configs = self._parse_last_configs_for_user(unpacked_configs)
                use_last_configs = msg.askquestion(title='Configs', message=f'Do you want to use configs from last '
                                                                            f'game?\n\n\n\n{parsed_configs}')
                if use_last_configs == 'yes':
                    self._upload_data_to_database(unpacked_configs['difficulty_index'],
                                                  unpacked_configs['screen_resolution_index'],
                                                  unpacked_configs['lives'])
                    self._check_record()
                    self._configs.update_configs_after_gui(unpacked_configs['difficulty_index'],
                                                           unpacked_configs['lives'],
                                                           unpacked_configs['bird_color_index'],
                                                           unpacked_configs['pipes_color_index'],
                                                           unpacked_configs['screen_resolution_index'])
                    if unpacked_configs['path_to_background'] != self._configs.path_to_background_picture:
                        if os.path.exists(unpacked_configs['path_to_background']):
                            self._configs.path_to_background_picture = unpacked_configs['path_to_background']
                    if unpacked_configs['path_to_music'] != self._configs.path_to_music:
                        if os.path.exists(unpacked_configs['path_to_music']):
                            self._configs.path_to_music = unpacked_configs['path_to_music']
                    self._main_window.destroy()
                    flappy_bird_game = FlappyBirdGame(self._configs, self._database)
                    flappy_bird_game.main()
                else:
                    self._main_window.destroy()
                    precondition = PreconditionsGUI(self._database, self._configs)
                    precondition.main()
            else:
                self._main_window.destroy()
                precondition = PreconditionsGUI(self._database, self._configs)
                precondition.main()

        elif user_exists and not valid_password:
            self._clear_entries()
            msg.showerror(title='Login error', message="Invalid password! Entered password doesn't match the password, "
                                                       "which was entered during registration! Please, try again!")
        elif not user_exists:
            self._clear_entries()
            msg.showerror(title='Login error', message="User doesn't exist! There is no user with such username! "
                                                       "Please, use another username or register a new one!")

    def _register(self):
        username, password = self._get_username_and_hashed_password()
        user_exists, _ = self._database.check_user_existence(username, password)
        if user_exists:
            msg.showerror(title='Registration error', message="User already exists! Please login or use another "
                                                              "username to register!")
        else:
            self._database.upload_users(username, password)
            cont_event = msg.showinfo(title='Registration complete',
                                      message='You have been successfully registered!')
            if cont_event == 'ok':
                self._main_window.destroy()
                precondition = PreconditionsGUI(self._database, self._configs)
                precondition.main()

    def _clear_entries(self):
        self._username_entry.delete(0, END)
        self._password_entry.delete(0, END)

    def main(self):
        self._create_and_place()
        self._main_window.mainloop()


if __name__ == '__main__':
    main = MainGUI()
    main.main()

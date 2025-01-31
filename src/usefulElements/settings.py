import json
from os.path import exists
# ------------------------ app code files
from usefulElements import log_error, settings_file_path

SYSTEM_THEME = "system"
DARK_THEME = "dark"
LIGHT_THEME = "light"

ACTIVE_THEME_NAME = "active_theme"
DISPLAY_TIME_NAME = "display_time"
ACTIVE_SOUNDS_NAME = "active_sounds"
SHORTCUT_QUIT_NAME = "shortcut_quit"
CHECK_UPDATE_AT_STARTUP_NAME = "check_update_at_startup"

class Settings():
    def __init__(self):
        # ------------------------ default values
        self.value_active_theme = SYSTEM_THEME
        self.value_display_time = True
        self.value_active_sounds = False
        self.value_shortcut_quit = True
        self.value_check_update_at_startup = True
        # ------------------------ check if file exists then read it
        self.load_settings()

    def load_settings(self):
        if exists(settings_file_path):
            try:
                with open(settings_file_path, 'r') as file:
                    # update attributs
                    data = json.load(file)
                    self.value_active_theme = data[ACTIVE_THEME_NAME]
                    self.value_display_time = data[DISPLAY_TIME_NAME]
                    self.value_active_sounds = data[ACTIVE_SOUNDS_NAME]
                    self.value_shortcut_quit = data[SHORTCUT_QUIT_NAME]
                    self.value_check_update_at_startup = data[CHECK_UPDATE_AT_STARTUP_NAME]
            except FileNotFoundError:
                log_error(f"Settings file was not found. Default values will be used")
            except json.JSONDecodeError:
                log_error(f"The settings file is corrupted. Default values will be used")
            except KeyError:
                log_error(f"One or several key are missing... Default values will be used")
        # if the settings file doesn't exist, create it with default values
        else:
            self.record_data()

    def record_data(self):
        # ------------------------ serialize class parameters to file
        data = {
            ACTIVE_THEME_NAME: self.value_active_theme,
            DISPLAY_TIME_NAME: self.value_display_time,
            ACTIVE_SOUNDS_NAME: self.value_active_sounds,
            SHORTCUT_QUIT_NAME: self.value_shortcut_quit,
            CHECK_UPDATE_AT_STARTUP_NAME: self.value_check_update_at_startup
        }
        with open(settings_file_path, 'w') as file:
            json.dump(data, file, indent=4)

settings = Settings()
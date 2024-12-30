import json
from os.path import exists
# ------------------------ app code files
from filePaths import settings_file_path
from usefulElements import log_error

THEME_SYSTEM = "system"
THEME_DARK = "dark"
THEME_LIGHT = "light"

class Settings():
    def __init__(self):
        # ------------------------ default values
        self.value_active_theme = THEME_SYSTEM
        self.value_display_time = True
        self.value_active_sounds = False
        self.value_shortcut_quit = True
        # ------------------------ check if file exists then read it
        self.load_settings()

    def load_settings(self):
        if exists(settings_file_path):
            try:
                with open(settings_file_path, 'r') as file:
                    try: # update attributs
                        data = json.load(file)
                        self.value_active_theme = data.get("active_theme", self.value_active_theme)
                        self.value_display_time = data.get("display_time", self.value_display_time)
                        self.value_active_sounds = data.get("active_sounds", self.value_active_sounds)
                        self.value_shortcut_quit = data.get("shortcut_quit", self.value_shortcut_quit)
                    except json.JSONDecodeError:
                        log_error(f"The settings file is corrupted. Default values will be used")
            except FileNotFoundError:
                log_error(f"Settings file was not found. Default values will be used")
        # if the settings file doesn't exist, create it with default values
        else:
            self.record_data()

    def record_data(self):
        # ------------------------ serialize class parameters to file
        data = {
            "active_theme": self.value_active_theme,
            "display_time": self.value_display_time,
            "active_sounds": self.value_active_sounds,
            "shortcut_quit": self.value_shortcut_quit
        }
        with open(settings_file_path, 'w') as file:
            json.dump(data, file, indent=4)

settings = Settings()
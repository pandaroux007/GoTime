import sys
from getpass import getuser
from socket import gethostname
from datetime import datetime
from customtkinter import CTkToplevel
from PIL import Image, ImageTk
# ------------------------ app code files
from filePaths import *

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

# ------------------------ colors
class Colors:
    # dark_text = "#242424"
    # light_text = "#ffffff"
    timeframe_green = ("#73ff14", "#347507")
    timeframe_yellow = ("#f4Ef12", "#b3af0c")
    timeframe_red = ("#f84615", "#ad2f0c")

class ModalCustomCTk(CTkToplevel):
    def __init__(self, master=None, *args, fg_color = None, **kwargs):
        super().__init__(master=master, *args, fg_color=fg_color, **kwargs)
        if "master" in kwargs:
            self.master = kwargs.pop("master")
        elif "master" in args:
            self.master = args["master"]
        
        self.transient(self.master)
        if exploitation_system == "win": self.after(250, lambda: self.iconbitmap(app_icon_file_path))
        else: self.def_icon_modal_window_unix()

    def def_icon_modal_window_unix(self):
        icon_image = Image.open(app_icon_file_path)
        icon_image = icon_image.resize((32, 32)) # Image.Resampling.LANCZOS
        self.icon = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, self.icon)
        self.wm_iconbitmap()

# ------------------------ useful functions
def log_error(message_erreur):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getuser()
    hostname = gethostname()
    error_data = f"{timestamp}   |   {username} sur {hostname}   |   {message_erreur}"
    with open(log_file_path, mode='a', newline='') as file:
        # if file.tell() == 0: # check the file is empty
        #     header = "Date + Time    |   User et hostname   |   Error"
        #     file.write(f"{header}\n")
        file.write(f"{error_data}\n")

current_ring = None
def play_sound(state_sound):
    try:
        from pygame import mixer
        mixer.init()
        global current_ring
        if current_ring == None:
            current_ring = mixer.Sound(time_end_sound_file_path)
        current_ring.play() if state_sound else current_ring.stop()
    
    except Exception as e:
        log_error(f"Exception in play_sound function : {str(e)}")
        pass

# ------------------------ useful variables
exploitation_system = sys.platform
max_time = 10800 # 3 heures en secondes
colors = Colors()
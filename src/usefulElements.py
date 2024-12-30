import sys
from getpass import getuser
from socket import gethostname
from datetime import datetime
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

# ------------------------ useful functions
def log_error(message_erreur):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getuser()
    hostname = gethostname()
    error_data = f"{timestamp}   |   {username} sur {hostname}   |   {message_erreur}"
    with open(log_file_path, mode='a', newline='') as file:
        if file.tell() == 0: # check the file is empty
            header = "Date + Time    |   User et hostname   |   Error"
            file.write(f"{header}\n")
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
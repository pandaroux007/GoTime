from getpass import getuser
from socket import gethostname
from datetime import datetime
# ------------------------ app code files
from .filePaths import log_file_path, time_end_sound_file_path

# ------------------------ useful functions
def log_error(error_message: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getuser()
    hostname = gethostname()
    error_data = f"{timestamp}   |   {username} on {hostname}   |   {error_message}"
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

# ------------------------------------ to finish
# def debugged_function(func):
#     def wrapper():
#         try:
#             return func()
#         except Exception as error:
#             print(f"Error in {func.__name__}! Error is: {error}")
#     return wrapper()
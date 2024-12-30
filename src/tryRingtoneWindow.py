import customtkinter as ctk
# ------------------------ app code files
from usefulElements import play_sound
from appInfos import app_name

class TryRingtoneWindow(ctk.CTkToplevel):
    def __init__(self, master):
        super().__init__(master=master)
        # ------------------------ window configuration
        self.title(f"Try ringtone - {app_name}")
        self.resizable(False, False)
        self.transient(master)
        self.protocol("WM_DELETE_WINDOW", self.close_window)
        self.grid_columnconfigure((0, 1), weight=1)
        self.grid_rowconfigure((0, 1), weight=1)
        # ------------------------ section's title
        self.try_ringtone_title = ctk.CTkLabel(self, text="Try the ringtone!", font=ctk.CTkFont(size=24))
        self.try_ringtone_title.grid(row=0, column=0, columnspan=2, pady=10)
        # ------------------------ buttons' frame
        self.buttons_frame = ctk.CTkFrame(self)
        self.buttons_frame.grid(row=1, column=0, columnspan=2, sticky=ctk.NSEW, padx=10, pady=10)
        # ------------------------ button to play the ringtone
        self.play_button = ctk.CTkButton(self.buttons_frame, text="Play the ringtone", command=lambda: play_sound(True))
        self.play_button.grid(row=1, column=0, sticky=ctk.EW, padx=10, pady=7)
        # ------------------------ button to stop the ringtone
        self.stop_button = ctk.CTkButton(self.buttons_frame, text="Stop the ringtone", command=lambda: play_sound(False))
        self.stop_button.grid(row=1, column=1, sticky=ctk.EW, padx=10, pady=7)

    def close_window(self):
        play_sound(False)
        self.destroy()
from sys import exit
import customtkinter as ctk
from datetime import datetime
from PIL import Image, ImageTk
import webbrowser
from lib.CTkMessagebox import CTkMessagebox
from lib.CTkMenuBar import CTkMenuBar, CTkTitleMenu, CustomDropdownMenu
# ------------------------ app code files
from settingsWindow import SettingsWindow
from licenseWindow import LicenseWindow
from aboutWindow import AboutWindow
from spinbox import Spinbox
from appInfos import *
from filePaths import app_icon_file_path
from usefulElements import *
from settings import settings

REMAINING_TIME_DEFAULT_TXT = "Remaining time"
MOVE_TIMER_BUTTON_TXT = "Move the timer to a new dedicated window"
PAUSE_BUTTON_TXT = "PAUSE"
ACTIVE_PAUSE_BUTTON_TXT = "RESUME"

class Application(ctk.CTk):
    def __init__(self):
        super().__init__()
        # ------------------------ variables
        self.paused = False
        self.remaining_time = 0
        self.pause_button_lock = False # to avoid timer bugs after double clicks on the pause button
        
        self.config_window_app()
        # ------------------------ menu bar
        if exploitation_system == "win32":
            self.menu_bar = CTkTitleMenu(self)
        else:
            self.menu_bar = CTkMenuBar(self)
        window_button = self.menu_bar.add_cascade("Window")
        commands_button = self.menu_bar.add_cascade("Edit")
        sources_button = self.menu_bar.add_cascade("Source")
        # ------------------------ creating a "Window" menu
        dropdown_window = CustomDropdownMenu(widget=window_button)
        dropdown_window.add_option(option="Settings", command=lambda: SettingsWindow(self))
        dropdown_window.add_separator()
        dropdown_window.add_option(option="Quit", command=self.quit)
        # ------------------------ creating a second "Commands" menu
        dropdown_commands = CustomDropdownMenu(widget=commands_button)
        dropdown_commands.add_option(option="Clear entries", command=self.clear_entries)
        dropdown_commands.add_option(option="Move timer", command=self.move_timer_in_new_window)
        # ------------------------ creating a third "Source" menu
        dropdown_source = CustomDropdownMenu(widget=sources_button)
        dropdown_source.add_option(option="License", command=lambda: LicenseWindow(self))
        dropdown_source.add_option(option="Report bugs", command=lambda: webbrowser.open_new_tab(app_source_code_link + "/issues"))
        dropdown_source.add_option(option="About", command=lambda: AboutWindow(self))
        # ------------------------ adding the menu bar to the window
        self.configure(menu=self.menu_bar)
        
        # ------------------------ main frame for allow the use of grid function
        self.main = ctk.CTkFrame(self, corner_radius=0, fg_color=self.cget("fg_color"))
        self.main.pack(fill="both", expand=True)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure((1, 2, 3), weight=1)
        # ------------------------ display time at top of window
        if settings.value_display_time == True:
            self.time_label = ctk.CTkLabel(self.main, text="", font=ctk.CTkFont(size=24))
            self.time_label.grid(row=0, column=0, pady=12)
            self.update_time()
        
        # ------------------------ creating the frame with the remaining time
        self.remaining_frame = ctk.CTkFrame(self.main, fg_color=colors.timeframe_green)
        self.remaining_frame.grid(row=1, column=0, padx=25, pady=10, sticky="nsew")
        self.remaining_frame.grid_columnconfigure(0, weight=1)
        self.remaining_frame.grid_rowconfigure(0, weight=1)
        self.remaining_label = ctk.CTkLabel(self.remaining_frame, text=REMAINING_TIME_DEFAULT_TXT, font=ctk.CTkFont(size=36))
        self.remaining_label.grid(row=0, column=0, padx=10, pady=10)

        # ------------------------ create control timer buttons
        default_button_style = {"row": 0, "padx": 5, "pady": 5, "sticky": "ew"}

        self.button_frame = ctk.CTkFrame(self.main)
        self.button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="new")
        self.button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.start_button = ctk.CTkButton(self.button_frame, text="START", height=50, command=self.start_timer)
        self.start_button.grid(column=0, **default_button_style)
        self.pause_button = ctk.CTkButton(self.button_frame, text=PAUSE_BUTTON_TXT, height=50, state=ctk.DISABLED, command=self.pause_timer)
        self.pause_button.grid(column=1, **default_button_style)
        self.stop_button = ctk.CTkButton(self.button_frame, text="STOP", height=50, state=ctk.DISABLED, command=lambda: self.stop_timer(True))
        self.stop_button.grid(column=2, **default_button_style)
        # ------------------------ create the move timer button
        self.move_button = ctk.CTkButton(self.button_frame, text=MOVE_TIMER_BUTTON_TXT, command=self.move_timer_in_new_window)
        self.move_button.grid(row=1, padx=5, pady=(10, 20), sticky="sew", columnspan=3)

        # ------------------------ entries for timer management
        self.entries_frame = ctk.CTkFrame(self.main, fg_color=self.cget("fg_color"))
        self.entries_frame.grid(row=3, column=0, padx=20, pady=10, sticky="new")
        self.entries_frame.grid_columnconfigure((0, 2, 4), weight=1)
        self.entries_frame.grid_rowconfigure((0, 1), weight=1)
        # ------------------------ dynamic variables
        self.minutes_entry_variable = ctk.StringVar(self)
        self.minutes_entry_variable.trace_add("write", self.handle_start_button)
        self.seconds_entry_variable = ctk.StringVar(self)
        self.seconds_entry_variable.trace_add("write", self.handle_start_button)
        # ------------------------ section's title
        self.titre_section_temps_entry = ctk.CTkLabel(self.entries_frame, text="Enter timelaps here :", font=ctk.CTkFont(size=20))
        self.titre_section_temps_entry.grid(row=0, sticky="NEW", pady=(0, 20), columnspan=5)

        # ------------ minutes entry
        self.minutes_entry = Spinbox(self.entries_frame, value_from=0, value_to=60, enter_key_command=self.start_timer,
                                    placeholder="minutes here...", text_variable=self.minutes_entry_variable)
        self.minutes_entry.grid(row=1, column=0, padx=(0, 5), sticky=ctk.EW)
        self.minutes_entry_indicator = ctk.CTkLabel(self.entries_frame, text="min")
        self.minutes_entry_indicator.grid(row=1, column=1, padx=(0, 15), sticky=ctk.W)
        # ------------ seconds entry
        self.seconds_entry = Spinbox(self.entries_frame, value_from=0, value_to=10800, enter_key_command=self.start_timer,
                                    placeholder="and seconds here.", text_variable=self.seconds_entry_variable)
        self.seconds_entry.grid(row=1, column=2, padx=5, sticky=ctk.EW)
        self.seconds_entry_indicator = ctk.CTkLabel(self.entries_frame, text="s")
        self.seconds_entry_indicator.grid(row=1, column=3, padx=(0, 15), sticky=ctk.W)
        # ------------ create clear entries button
        self.clear_button = ctk.CTkButton(self.entries_frame, text="Clear entries", command=self.clear_entries)
        self.clear_button.grid(row=1, column=4, padx=(0, 5), sticky=ctk.EW)
        self.clear_entries()

    def def_icon_app(self):
        icon_image = Image.open(app_icon_file_path)
        icon_image = icon_image.resize((32, 32)) # Image.Resampling.LANCZOS
        self.icon = ImageTk.PhotoImage(icon_image)
        self.iconphoto(True, self.icon)
        self.wm_iconbitmap()

    def config_window_app(self):
        self.title(f"{app_name} v{app_version}")
        self.width = int(self.winfo_screenwidth()/2.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1000, 680)
        self.def_icon_app()
        # ------------------------ handle events
        self.bind("<1>", lambda event: event.widget.focus_set())
        if settings.value_shortcut_quit:
            self.bind(f"<Control-q>", lambda event, *args: self.quit())

    def update_time(self):
        if hasattr(self, "time_label"):
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.configure(text=current_time)
            self.after(1000, self.update_time)

    def start_timer(self):
        if self.handle_disponibility_start_command():
            play_sound(False)
            self.start_button.configure(state=ctk.DISABLED)
            self.pause_button.configure(state=ctk.NORMAL)
            self.stop_button.configure(state=ctk.NORMAL)
            self.clear_button.configure(state=ctk.DISABLED)
            self.minutes_entry.desabled()
            self.seconds_entry.desabled()

            self.remaining_time = self.get_total_seconds()
            self.update_timer()

    def update_timer(self):
        if self.remaining_time > 0 and not self.paused:
            self.remaining_time -= 1
            time_str = self.get_str_remaining_time()
            self.remaining_label.configure(text=time_str, fg_color=colors.timeframe_green)

            if hasattr(self, 'minimized_window') and self.minimized_window.winfo_exists():
                self.remaining_time_minimized_window.configure(text=time_str, fg_color=colors.timeframe_green)

            # calculating the percentage of remaining time
            total_time = self.get_total_seconds()
            time_left = self.remaining_time
            remaining_percent = time_left / total_time
            # timeframe color change based on percentage of remaining time
            if remaining_percent <= 0.2:
                self.remaining_frame.configure(fg_color=colors.timeframe_red)
                self.remaining_label.configure(fg_color=colors.timeframe_red)
                if hasattr(self, 'minimized_window') and self.minimized_window.winfo_exists():
                    self.minimized_window.configure(fg_color=colors.timeframe_red)
                    self.remaining_time_minimized_window.configure(fg_color=colors.timeframe_red)
            
            elif remaining_percent <= 0.3:
                self.remaining_frame.configure(fg_color=colors.timeframe_yellow)
                self.remaining_label.configure(fg_color=colors.timeframe_yellow)
                if hasattr(self, 'minimized_window') and self.minimized_window.winfo_exists():
                    self.minimized_window.configure(fg_color=colors.timeframe_yellow)
                    self.remaining_time_minimized_window.configure(fg_color=colors.timeframe_yellow)
            
            else:
                self.remaining_frame.configure(fg_color=colors.timeframe_green)
                self.remaining_label.configure(fg_color=colors.timeframe_green)
                if hasattr(self, 'minimized_window') and self.minimized_window.winfo_exists():
                    self.minimized_window.configure(fg_color=colors.timeframe_green)
                    self.remaining_time_minimized_window.configure(fg_color=colors.timeframe_green)
            
            if self.remaining_time == 0:
                self.stop_timer(False)
            else:
                self.after(1000, self.update_timer)
               
        # else if self.paused is true, skips the timer
        # without decrementing the remaining time

    def pause_timer(self):
        if self.pause_button_lock == True:
            return # if the function is locked, we don't enter it !
        else:
            self.pause_button_lock = True # lock the function to prevent other simultaneous executions
        if not hasattr(self, 'paused'):
            self.paused = False
        else:
            self.paused = not self.paused
            if self.paused:
                self.pause_button.configure(text=ACTIVE_PAUSE_BUTTON_TXT)
            else:
                self.pause_button.configure(text=PAUSE_BUTTON_TXT)
                self.update_timer()
        self.pause_button_lock

        # unlock the function when completed
        self.after(1000, lambda: setattr(self, 'pause_button_lock', False))

    def stop_timer(self, call_from_button):
        self.paused = False
        self.remaining_time = 0  # restart remaining time
        # ------------------------ config entries and buttons state
        self.start_button.configure(state=ctk.NORMAL)
        self.pause_button.configure(state=ctk.DISABLED, text=PAUSE_BUTTON_TXT)
        self.stop_button.configure(state=ctk.DISABLED)
        self.clear_button.configure(state=ctk.NORMAL)
        self.minutes_entry.enable()
        self.seconds_entry.enable()
        # ------------------------ handle clearing remaining time
        self.remaining_frame.configure(fg_color=colors.timeframe_green)
        self.remaining_label.configure(text=REMAINING_TIME_DEFAULT_TXT, fg_color=colors.timeframe_green)
        if hasattr(self, 'minimized_window') and self.minimized_window.winfo_exists():
            self.minimized_window.configure(fg_color=colors.timeframe_green)
            self.remaining_time_minimized_window.configure(text=REMAINING_TIME_DEFAULT_TXT, fg_color=colors.timeframe_green)
        # ------------------------ handle sound
        if call_from_button == False and settings.value_active_sounds: # the function is called at the end of timer
            play_sound(True)

    def handle_disponibility_start_command(self) -> bool:
        total_seconds = self.get_total_seconds()
        if total_seconds >= 5 and total_seconds <= max_time:
            return True
        else:
            return False
        
    def get_total_seconds(self) -> int:
        minutes_str = self.minutes_entry_variable.get()
        seconds_str = self.seconds_entry_variable.get()
        if minutes_str and seconds_str:
            minutes = int(minutes_str)
            seconds = int(seconds_str)
        else:
            minutes = 0
            seconds = 0
        total_seconds = minutes * 60 + seconds
        return total_seconds
    
    def get_str_remaining_time(self) -> str:
        if self.remaining_time:
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            return f"{minutes:02d}:{seconds:02d}"
        else:
            return "00:00"

    def handle_start_button(self, *args):
        # ------------------------ manage the state of the "START" button based on the total number of seconds
        if self.handle_disponibility_start_command():
            self.start_button.configure(state=ctk.NORMAL)
        else:
            self.start_button.configure(state=ctk.DISABLED)

    def clear_entries(self):
        self.minutes_entry.clear()
        self.seconds_entry.clear()

    def move_timer_in_new_window(self):
        self.minimized_window = ctk.CTkToplevel(self, fg_color=colors.timeframe_green)
        self.minimized_window.title(f"{REMAINING_TIME_DEFAULT_TXT} - {app_name}")
        self.minimized_window.geometry("600x400")
        self.minimized_window.minsize(300, 200)
        self.minimized_window.transient(self)
        self.minimized_window.protocol("WM_DELETE_WINDOW", self.fermer_fenetre_temps_restant_deporte)
        self.minimized_window.wm_attributes("-topmost", 1)

        self.move_button.configure(text="Close the window containing the remaining time", command=self.fermer_fenetre_temps_restant_deporte)
        # ------------------------ display remaining time in center
        self.remaining_time_minimized_window = ctk.CTkLabel(self.minimized_window, font=ctk.CTkFont(size=50), fg_color=colors.timeframe_green)
        self.remaining_time_minimized_window.pack(expand=True)

        if self.remaining_time > 0 and not self.paused:
            temp_remaining_time_str = self.get_str_remaining_time()
            self.remaining_time_minimized_window.configure(text=temp_remaining_time_str)
            del temp_remaining_time_str
        else:
            self.remaining_time_minimized_window.configure(text=REMAINING_TIME_DEFAULT_TXT)

    def fermer_fenetre_temps_restant_deporte(self):
        self.move_button.configure(text=MOVE_TIMER_BUTTON_TXT, command=self.move_timer_in_new_window)
        self.minimized_window.destroy()
        self.focus_set()

if __name__ == "__main__":
    try:
        ctk.set_appearance_mode(settings.value_active_theme)
        ctk.set_default_color_theme("dark-blue")

        root = Application()
        root.mainloop()

        exit(EXIT_SUCCESS)

    except Exception as error:
        CTkMessagebox(title="Error... Something went wrong", message=error, icon="cancel").get()
        log_error(str(error))
        exit(EXIT_FAILURE)
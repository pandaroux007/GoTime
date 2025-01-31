import customtkinter as ctk
# ------------------------ app code files
from tryRingtoneWindow import TryRingtoneWindow
from usefulElements import *
from appInfos import app_name

class SettingsWindow(CTkModalWindow):
    def __init__(self, _master):
        super().__init__(master=_master)
        # ------------------------ settings window configuration
        self.title(f"Settings - {app_name}")
        self.geometry("600x400")
        self.resizable(False, False)
        self.transient(_master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)
        # ------------------------ create the settings page title
        self.title_settings_label = ctk.CTkLabel(self, text=f"Settings - {app_name}", font=ctk.CTkFont(size=24))
        self.title_settings_label.grid(row=0, column=0, sticky=ctk.N, pady=10)
        # ------------------------ create a tabview to separate the different settings
        self.tabview = ctk.CTkTabview(self)
        self.theme_tab = self.tabview.add(name="Appearance and Theme")
        # self.tabview.set(self.theme_tab)
        self.ringtone_tab = self.tabview.add(name="Ringtone")
        self.tabview.grid(row=1, column=0, sticky=ctk.EW, padx=20, pady=(0, 20))

        # ------------------------------------------------ Appearance and Theme tab
        self.theme_tab.grid_columnconfigure((0, 1, 2), weight=1)
        self.theme_tab.grid_rowconfigure((0, 1, 2, 3), weight=1)
        # ------------------------ frame to group the radiobuttons together
        self.theme_selection_frame = ctk.CTkFrame(self.theme_tab, fg_color=("#cccccc", "#323232"))
        self.theme_selection_frame.grid(row=0, column=0, sticky=ctk.NSEW, pady=20, padx=20, rowspan=4)
        self.theme_selection_frame.grid_columnconfigure(0, weight=1)
        self.theme_selection_frame.grid_rowconfigure((0, 1, 2), weight=1)
        # ------------------------ values
        self.active_theme_selection_value = ctk.StringVar(value=settings.value_active_theme)
        if exploitation_system != WINDOWS_NAME: 
            self.active_theme_selection_value.trace_add("write", lambda event, *args: ctk.set_appearance_mode(self.active_theme_selection_value.get()))
        self.display_time_selection_value = ctk.BooleanVar(value=settings.value_display_time)
        self.active_shortcut_quit_value = ctk.BooleanVar(value=settings.value_display_time)
        self.check_update_at_startup = ctk.BooleanVar(value=settings.value_check_update_at_startup)
        # ------------------------ radiobuttons for choose theme
        self.system_theme_selection_button = ctk.CTkRadioButton(self.theme_selection_frame, text=f"{SYSTEM_THEME} mode",
                                                                value=SYSTEM_THEME, variable=self.active_theme_selection_value)
        self.system_theme_selection_button.grid(row=0, column=0, sticky=ctk.EW, padx=7)
        self.dark_theme_selection_button = ctk.CTkRadioButton(self.theme_selection_frame, text=f"{DARK_THEME} mode",
                                                              value=DARK_THEME, variable=self.active_theme_selection_value)
        self.dark_theme_selection_button.grid(row=1, column=0, sticky=ctk.EW, padx=7)
        self.light_theme_selection_button = ctk.CTkRadioButton(self.theme_selection_frame, text=f"{LIGHT_THEME} mode",
                                                               value=LIGHT_THEME, variable=self.active_theme_selection_value)
        self.light_theme_selection_button.grid(row=2, column=0, sticky=ctk.EW, padx=7)
        # ------------------------ switchs for choose state of time displaying and shortcut for quit
        self.switch_display_time_at_top = ctk.CTkSwitch(self.theme_tab, text="Display time at top\n(requires restart)",
                                                                variable=self.display_time_selection_value, onvalue=True, offvalue=False)
        self.switch_display_time_at_top.grid(row=1, column=2, sticky=ctk.NSEW, padx=(10, 0))
        self.switch_active_shortcut_quit = ctk.CTkSwitch(self.theme_tab, text="Active the quit shortcut (Ctrl-Q)\n(requires restart)",
                                                        variable=self.active_shortcut_quit_value, onvalue=True, offvalue=False)
        self.switch_active_shortcut_quit.grid(row=2, column=2, sticky=ctk.NSEW, padx=(10, 0))
        self.switch_check_update_at_startup = ctk.CTkSwitch(self.theme_tab, text="Active the checking of update at startup",
                                                        variable=self.check_update_at_startup, onvalue=True, offvalue=False)
        self.switch_check_update_at_startup.grid(row=3, column=2, sticky=ctk.NSEW, padx=(10, 0))

        # ------------------------------------------------ Ringtone tab
        self.active_sound_selection_value = ctk.BooleanVar(value=settings.value_active_sounds)
        self.ringtone_tab.grid_columnconfigure((0, 1), weight=1)
        self.ringtone_tab.grid_rowconfigure(0, weight=1)
        # ------------------------ switch to select if the ringtone is active
        self.switch_active_sound = ctk.CTkSwitch(self.ringtone_tab, text="Ringtone active", variable=self.active_sound_selection_value,
                                                onvalue = True, offvalue = False)
        self.switch_active_sound.grid(row=0, column=0, padx=(0, 5), pady=2)
        # ------------------------ button to try the current ringtone
        self.test_ringtone_button = ctk.CTkButton(self.ringtone_tab, text="Try the ringtone", command=lambda: TryRingtoneWindow(self))
        self.test_ringtone_button.grid(row=0, column=1, padx=(0, 5), pady=2)
        # ------------------------ frame to group the buttons together
        self.buttons_frame_settings = ctk.CTkFrame(self)
        self.buttons_frame_settings.grid(row=2, column=0, sticky="SEW", padx=20, pady=(0, 15))
        self.buttons_frame_settings.grid_columnconfigure((0, 1), weight=1)
        self.buttons_frame_settings.grid_rowconfigure(0, weight=1)

        self.apply_settings_button = ctk.CTkButton(self.buttons_frame_settings, text="Apply settings and close this", command=self.apply_settings)
        self.apply_settings_button.grid(row=0, column=0, sticky=ctk.EW, padx=20, pady=7)

        self.cancel_button = ctk.CTkButton(self.buttons_frame_settings, text="Cancel", command=self.quit_app)
        self.cancel_button.grid(row=0, column=1, sticky=ctk.EW, padx=20, pady=7)

    def apply_settings(self):
        settings_changes = False
        # light or dark theme management
        selected_theme = self.active_theme_selection_value.get()
        if selected_theme != settings.value_active_theme:
            settings.value_active_theme = selected_theme
            settings_changes = True
        # ringtone activation management
        selected_state_sounds = self.active_sound_selection_value.get()
        if selected_state_sounds != settings.value_active_sounds:
            settings.value_active_sounds = selected_state_sounds
            settings_changes = True
        # managing the time display at the top of the application window
        selected_state_display_time = self.display_time_selection_value.get()
        if selected_state_display_time != settings.value_display_time:
            settings.value_display_time = selected_state_display_time
            settings_changes = True
        # set the state of the quit shortcut
        selected_state_shortcut_quit = self.active_shortcut_quit_value.get()
        if selected_state_shortcut_quit != settings.value_shortcut_quit:
            settings.value_shortcut_quit = selected_state_shortcut_quit
            settings_changes = True
        # state of checking update at startup
        selected_state_checking_update_at_startup = self.check_update_at_startup.get()
        if selected_state_checking_update_at_startup != settings.value_check_update_at_startup:
            settings.value_check_update_at_startup = selected_state_checking_update_at_startup
            settings_changes = True
        
        # if one or more settings have changed, we save
        if settings_changes is not False:
            settings.record_data()
        
        self.quit_app()

    def quit_app(self):
        if exploitation_system != WINDOWS_NAME: 
            ctk.set_appearance_mode(settings.value_active_theme)
        self.destroy()

# app = SettingsWindow(None)
# app.mainloop()
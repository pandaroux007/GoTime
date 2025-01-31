import customtkinter as ctk
import webbrowser
from PIL import Image
# ------------------------ app code files
from systemCheckUpdate import SystemCheckUpdate
from licenseWindow import LicenseWindow
from usefulElements import *
from appInfos import *

class AboutWindow(CTkModalWindow):
    def __init__(self, _master):
        self._master = _master
        super().__init__(master=self._master)
        # ------------------------ window configuration
        self.title(f"About - {app_name}")
        self.geometry("450x360")
        self.resizable(False, False)
        self.transient(self._master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(5, weight=1)
        # ------------------------ informations
        ctk.CTkLabel(self, text=app_name, font=ctk.CTkFont(size=24, weight="bold")).grid(row=0, column=0, pady=(20, 10))
        ctk.CTkLabel(self, text="A cross-platform python timer application based on tkinter.", 
                    wraplength=300, justify="center", font=ctk.CTkFont(size=14)).grid(row=1, column=0, pady=7)
        ctk.CTkLabel(self, text=f"Version : {app_version}", font=ctk.CTkFont(size=16)).grid(row=2, column=0)
        ctk.CTkLabel(self, text=f"Author : {app_author}", font=ctk.CTkFont(size=16)).grid(row=3, column=0, pady=(0, 10))
        try:
            with open(license_file_path, 'r') as license_file:
                self.license_button = ctk.CTkButton(self, text=license_file.readline().strip(), command=lambda: LicenseWindow(self._master))
                self.license_button.grid(row=4, column=0, sticky=ctk.EW, padx=30, pady=5)
        except: pass
        # ------------------------ github link
        self.github_button = ctk.CTkButton(self, image=ctk.CTkImage(Image.open(github_icon_file_path)),
                                           text="Project github link", command=lambda: webbrowser.open_new_tab(app_source_code_link))
        if hasattr(self, "license_button") and self.license_button.winfo_exists():
            self.github_button.grid(row=5, column=0, sticky=ctk.EW, padx=30, pady=10)
        else:
            self.github_button.grid(row=4, column=0, sticky=ctk.EW, padx=30, pady=10)
        # ------------------------ buttons frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.buttons_frame.grid(row=6, column=0, sticky=ctk.EW, padx=20, pady=20)
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        # ------------------------ check updates button
        self.check_uptates_button = ctk.CTkButton(self.buttons_frame, text="Check for updates", command=self.run_check_updates)
        self.check_uptates_button.grid(row=0, column=0, padx=10, pady=10, sticky=ctk.EW)
        # ------------------------ cancel button
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky=ctk.EW)

    def run_check_updates(self):
        self.check_updates_system = SystemCheckUpdate(self._master)
        self.check_uptates_button.configure(state=ctk.DISABLED, cursor="watch")
        self.check_updates_system.set_callback_end_check_update(lambda: self.check_uptates_button.configure(state=ctk.NORMAL, cursor="arrow"))
        self.check_updates_system.run_check_update()
    
# if __name__ == "__main__":
#     app = ctk.CTk()
#     AboutWindow(app)
#     app.mainloop()
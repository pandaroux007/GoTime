import customtkinter as ctk
import webbrowser
from PIL import Image
# ------------------------ app code files
# from SystemCheckUpdate import SystemCheckUpdate
from licenseWindow import LicenseWindow
from appInfos import *
from filePaths import license_file_path, github_icon_file_path

class AboutWindow(ctk.CTkToplevel):
    def __init__(self, _master):
        super().__init__(master=_master)
        # ------------------------ window configuration
        self.title(f"About - {app_name}")
        self.geometry("450x360")
        self.resizable(False, False)
        self.transient(_master)
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
                self.license_button = ctk.CTkButton(self, text=license_file.readline().strip(), command=lambda: LicenseWindow(_master))
                self.license_button.grid(row=4, column=0, sticky=ctk.EW, padx=30, pady=5)
        except: pass
        # ------------------------ github link
        self.github_button = ctk.CTkButton(self, image=ctk.CTkImage(Image.open(github_icon_file_path)),
                                           text="Project github link", command=lambda: webbrowser.open_new_tab(app_source_code_link))
        if self.license_button.winfo_exists():
            self.github_button.grid(row=5, column=0, sticky=ctk.EW, padx=30, pady=10)
        else:
            self.github_button.grid(row=4, column=0, sticky=ctk.EW, padx=30, pady=10)
        # ------------------------ buttons frame
        self.buttons_frame = ctk.CTkFrame(self, fg_color=self.cget("fg_color"))
        self.buttons_frame.grid(row=6, column=0, sticky=ctk.EW, padx=20, pady=20)
        self.buttons_frame.grid_columnconfigure((0, 1), weight=1)
        # ------------------------ check updates button
        self.check_uptates_button = ctk.CTkButton(self.buttons_frame, text="Check for updates", command=lambda: print("Check for updates"))
        self.check_uptates_button.grid(row=0, column=0, padx=10, pady=10, sticky=ctk.EW)
        # ------------------------ cancel button
        self.cancel_button = ctk.CTkButton(self.buttons_frame, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky=ctk.EW)

    # def run_check_updates(self):
    #     self.check_updates_system = SystemCheckUpdate()
    #     self.check_uptates_button.configure(state=ctk.DISABLED, cursor="watch")
    #     self.check_updates_system.setCallbackEndUpdate(lambda: self.check_uptates_button.config(state=ctk.NORMAL, cursor="arrow"))
    #     self.check_updates_system.runCheckUpdates()
    
if __name__ == "__main__":
    app = ctk.CTk()
    AboutWindow(app)
    app.mainloop()
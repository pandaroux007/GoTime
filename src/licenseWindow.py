import customtkinter as ctk
from lib.CTkMessagebox import CTkMessagebox
# ------------------------ app code files
from appInfos import app_name
from filePaths import license_file_path
from usefulElements import ModalCustomCTk, log_error

class LicenseWindow(ModalCustomCTk):
    def __init__(self, _master):
        super().__init__(master=_master)
        # ------------------------ license window configuration
        self.title(f"License - {app_name}")
        self.geometry("600x500")
        self.resizable(False, False)
        self.transient(_master)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        # ------------------------ display license's text
        try:
            with open(license_file_path, "r") as file:
                licence_content = file.read()
            
            self.license_text = ctk.CTkTextbox(self, wrap="word")
            self.license_text.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10), sticky=ctk.NSEW)
            self.license_text.insert("1.0", licence_content)
            self.license_text.configure(state=ctk.DISABLED)
        except FileNotFoundError as error:
            self.destroy()
            CTkMessagebox(title="License reading error...",
                          message="An error occurred while trying to read the LICENSE file. It was not found.",
                          icon="cancel").get()
            log_error(str(error))
            return
        # ------------------------ button to close the window
        self.close_button = ctk.CTkButton(self, text="OK - Cancel", command=self.destroy)
        self.close_button.grid(row=1, column=0, sticky=ctk.EW, padx=20, pady=(0, 20))
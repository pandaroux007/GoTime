import customtkinter as ctk
from PIL import Image
import os
# ------------------------ app code files
# from .filePaths import ctkmessagebox_icons_path

# constants
CHECK = "check"
CANCEL = "cancel"
INFO = "info"
QUESTION = "question"
WARNING = "warning"

class CTkPopup(ctk.CTkToplevel):
    def __init__(self, master: any = None, title: str = "CTkPopup", message: str = "This is a CTkPopup!",
                 icon: str = INFO, icon_size: tuple = None, width: int = 400, height: int = 170):
        self._width = width
        self._height = height
        self._master_window = master
        self._result = False
        super().__init__(master=self._master_window)
        # ------------------------ configure the popup
        self.wm_title(title)
        self.resizable(False, False)
        self.tkraise()
        self.grab_set()
        self.wm_attributes("-topmost", 1)
        self.wm_protocol("WM_DELETE_WINDOW", self._on_closing)
        self.wm_transient(master)
        # ------------------------ place window on the center of parent widget
        self._center_window()

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=0, column=0, sticky=ctk.NSEW, padx=10, pady=10)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        self.main_frame.grid_rowconfigure((0, 1), weight=1)

        if icon:
            ctk_icon = self._load_icon(icon, icon_size)
            self.icon_label = ctk.CTkLabel(self.main_frame, image=ctk_icon, text="")
            self.icon_label.grid(row=0, column=0, padx=10, pady=10)

        self.message_label = ctk.CTkLabel(self.main_frame, text=message, wraplength=self._width-150)
        self.message_label.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkButton(self, text="Ok", command=lambda: self._set_result(True)).grid(row=1, column=0, columnspan=2, sticky=ctk.E, padx=10, pady=10)

    def _center_window(self):
        if self._master_window is None:
            self.spawn_x = int((self.winfo_screenwidth() - self._width) / 2)
            self.spawn_y = int((self.winfo_screenheight() - self._height) / 2)
        else:
            # print(self._master_window.winfo_width(), self._master_window.winfo_height()) # for debug
            self.spawn_x = int(self._master_window.winfo_width() * .5 + self._master_window.winfo_x() - .5 * self._width + 7)
            self.spawn_y = int(self._master_window.winfo_height() * .5 + self._master_window.winfo_y() - .5 * self._height + 20)
        self.geometry(f"{self._width}x{self._height}+{self.spawn_x}+{self.spawn_y}")

    def _load_icon(self, icon: str, icon_size: tuple = None):
        if icon in [CHECK, CANCEL, INFO, QUESTION, WARNING]:
            # image_path = os.path.join(ctkmessagebox_icons_path, icon + ".png")
            image_path = os.path.join("gui/GoTime/src/usefulElements/icons", icon + ".png") # for tests only!
        else:
            image_path = icon
        
        if icon_size:
            size_height = min(icon_size[1], self._height - 100)
            size = (icon_size[0], size_height)
        else:
            size = (self._height // 3, self._height // 3)
        
        return ctk.CTkImage(Image.open(image_path), size=size)
    
    def _set_result(self, value):
        self._result = value
        self._on_closing()

    def _on_closing(self):
        self.grab_release()
        self.destroy()

    def get(self):
        try:
            if(self._master_window.winfo_exists()):
                self._master_window.wait_window(self)
        except AttributeError:
            self.wait_window()
        return self._result

class CTkAskYesNo(CTkPopup):
    def __init__(self, master, title, message):
        super().__init__(master, title=title, message=message, icon=QUESTION)
        # ------------------------ remove the Ok button
        for widget in self.winfo_children():
            if isinstance(widget, ctk.CTkButton):
                widget.destroy()
        # ------------------------ Yes and No buttons
        ctk.CTkButton(self, text="Yes", command=lambda: self._set_result(True)).grid(row=1, column=0, sticky=ctk.E, padx=(0, 5), pady=10)
        ctk.CTkButton(self, text="No", command=lambda: self._set_result(False)).grid(row=1, column=0, sticky=ctk.W, padx=(5, 0), pady=10)

if __name__ == "__main__":
    root = ctk.CTk()
    def show_popup():
        print("Result:", CTkAskYesNo(root, "Confirming", "Do you want to continue?").get())
    ctk.CTkButton(root, text="Show question", command=show_popup).pack(pady=20)
    ctk.CTkButton(root, text="Show popup", command=lambda: CTkPopup(root, icon=WARNING)).pack(pady=20)
    root.mainloop()
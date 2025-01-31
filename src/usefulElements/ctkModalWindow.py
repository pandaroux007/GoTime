from customtkinter import CTkToplevel as _ctktoplevel
from PIL import Image as _img, ImageTk as _imgtk
# ------------------------ app code files
from .filePaths import app_icon_file_path
from .constants import exploitation_system, WINDOWS_NAME

class CTkModalWindow(_ctktoplevel):
    def __init__(self, master=None, *args, fg_color = None, **kwargs):
        super().__init__(master=master, *args, fg_color=fg_color, **kwargs)
        if "master" in kwargs:
            self.master = kwargs.pop("master")
        elif "master" in args:
            self.master = args["master"]
        
        self.transient(self.master)
        if exploitation_system == WINDOWS_NAME:
            self.after(250, lambda: self.iconbitmap(app_icon_file_path))
        else:
            self.def_icon_modal_window_unix()

    def def_icon_modal_window_unix(self):
        icon_image = _img.open(app_icon_file_path)
        icon_image = icon_image.resize((32, 32)) # Image.Resampling.LANCZOS
        self.icon = _imgtk.PhotoImage(icon_image)
        self.iconphoto(True, self.icon)
        self.wm_iconbitmap()
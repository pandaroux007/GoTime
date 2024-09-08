from tkinter import messagebox
from sys import exit
# ------------------------ fichiers de l'application
from Application import Application
from Definitions import log_error

if __name__ == "__main__":
    try:
        root = Application()
        root.mainloop()
    except Exception as e:
        messagebox.showerror(title=f"Erreur", message=f"Hmm...Quelque chose semble s'être mal passé...\nL'erreur est : {str(e)}")
        log_error(str(e))
        exit()
from Application import Application
from tkinter import messagebox
from sys import exit

if __name__ == "__main__":
    try:
        root = Application()
        root.mainloop()
    except Exception as e:
        messagebox.showerror(title=f"Erreur", message=f"Hmm...something seems to have gone wrong.\nError is : {e}")
        exit()
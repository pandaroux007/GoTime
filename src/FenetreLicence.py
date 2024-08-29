import tkinter as tk
from variables import *

class FenetreLicence(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.geometry("800x500")
        self.title(f"Licence de {nom_application}")
        self.wm_iconbitmap()
        self.logo = tk.PhotoImage(file=chemin_image_application)
        self.iconphoto(False, self.logo)
        self.resizable(False, False)
        try:
            with open(chemin_fichier_licence, "r") as file:
                licence_content = file.read()
            licence_text = tk.Text(self, wrap="word")
            licence_text.pack(side="top", fill="both", expand=True, padx=10, pady=10)
            licence_text.insert("1.0", licence_content)
            licence_text.config(state="disabled")
        except FileNotFoundError:
            self.destroy()
            messagebox.showwarning(title=f"Avertissement", message="Une erreur s'est produite lors de la tentative de lecture du fichier de LICENCE. Celle-ci n'a pas été trouvée.")
            return
        close_button = tk.Button(self, text="Fermer", activebackground=couleur_frame_minuteur_rouge,
                                 width=100, justify="center", relief="groove", command=self.destroy)
        close_button.pack(side="bottom", padx=10, pady=10)
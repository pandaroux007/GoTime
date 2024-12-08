import tkinter as tk
from tkinter import messagebox
# ------------------------ fichiers de l'application
from InfoApp import *
from CheminsFichiers import *
from Utiles import *

class FenetreLicence(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # ------------------------ Paramètrage de la fenêtre affichage licence
        self.geometry("800x500")
        self.title(f"Licence de {nom_application}")
        self.resizable(False, False)
        # ------------------------ si fichier existe afficher son contenu (la licence) dans le widget Text
        try:
            with open(chemin_fichier_licence, "r") as file:
                licence_content = file.read()
            licence_text = tk.Text(self, wrap="word")
            licence_text.pack(side="top", fill="both", expand=True, padx=10, pady=10)
            licence_text.insert("1.0", licence_content)
            licence_text.config(state="disabled")
        # ------------------------ Sinon si erreur détruire la fenêtre et afficher message d'avertissement
        except FileNotFoundError as e:
            self.destroy()
            messagebox.showerror(title=f"Erreur", message="Une erreur s'est produite lors de la tentative de lecture du fichier de LICENCE. Celle-ci n'a pas été trouvée.")
            log_error(str(e))
            return
        # ------------------------ Bouton pour fermer la fenêtre, prenant toute la largeur
        close_button = tk.Button(self, text="Fermer", activebackground=couleurs.frame_rouge,
                                 width=100, justify="center", relief="solid", command=self.destroy)
        close_button.pack(side="bottom", padx=10, pady=10)
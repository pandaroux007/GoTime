import tkinter as tk
from tkinter import messagebox
import webbrowser
# ------------------------ fichiers de l'application
from Definitions import *

class LienHypertexte(tk.Label):
    def __init__(self, master, text, url, *args, **kwargs):
        super().__init__(master, text=text, fg="blue", cursor="hand2", *args, **kwargs)
        self.url = url
        self.bind("<Button-1>", lambda action: webbrowser.open_new_tab(self.url))
        self.bind("<Enter>", lambda action: self.config(font=("TkDefaultFont", 10, "underline")))
        self.bind("<Leave>", lambda action: self.config(font=("TkDefaultFont", 10)))

class FenetreInfo(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title(f"À propos de {nom_application}")
        self.geometry("400x300")
        self.resizable(False, False)
        # ------------------------ Frame principale
        self.frame_infos = tk.Frame(self, padx=20, pady=20)
        self.frame_infos.pack(fill=tk.BOTH, expand=True)
        # ------------------------ Informations
        tk.Label(self.frame_infos, text=nom_application, font=("Helvetica", 16, "bold")).pack()
        tk.Label(self.frame_infos, text=f"Version: {version_application}").pack()
        tk.Label(self.frame_infos, text=f"Auteur: {developpeur_application}").pack()
        tk.Label(self.frame_infos, text="Une application multiplateforme python de minuteur/timer basée sur tkinter", wraplength=350, justify="center").pack(pady=10)
        # ------------------------ lien du GitHub
        LienHypertexte(self.frame_infos, text="GitHub du projet", url=lien_du_github).pack(pady=10)
        # ------------------------ Frame pour les boutons
        button_frame = tk.Frame(self.frame_infos)
        button_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        # ------------------------ Bouton verif les mises à jours
        update_button = tk.Button(button_frame, text="Vérifier les mises à jour maintenant", command=self.check_updates)
        update_button.pack(side=tk.LEFT, expand=True)
        # ------------------------ Bouton "OK"
        ok_button = tk.Button(button_frame, text="OK", command=self.destroy)
        ok_button.pack(side=tk.RIGHT, expand=True)
        
    def check_updates(self):
        messagebox.showwarning("Mise à jour", "Cette partie de l'application est encore en développement!") # "Vérification des mises à jour en cours..."
import tkinter as tk
import webbrowser
# ------------------------ fichiers de l'application
from SystemeVerifUpdate import SystemeVerifUpdate
from Utiles import log_error
from InfoApp import *

class LienHypertexte(tk.Label):
    def __init__(self, master, text, url, *args, **kwargs):
        super().__init__(master, text=text, fg="blue", cursor="hand2", *args, **kwargs)
        self.url = url
        self.bind("<Button-1>", lambda action: webbrowser.open_new_tab(self.url))
        self.bind("<Enter>", lambda action: self.config(font=("TkDefaultFont", 10, "underline")))
        self.bind("<Leave>", lambda action: self.config(font=("TkDefaultFont", 10)))

class FenetreInfo(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # ------------------------ Parametrage fenêtre
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
        self.frame_boutons = tk.Frame(self.frame_infos)
        self.frame_boutons.pack(side=tk.BOTTOM, fill=tk.X, pady=(20, 0))
        # ------------------------ Bouton verif les mises à jours
        self.bouton_verif_mises_a_jour = tk.Button(self.frame_boutons, text="Vérifier les mises à jour maintenant", command=self.lancer_verif_update)
        self.bouton_verif_mises_a_jour.pack(side=tk.LEFT, expand=True)
        # ------------------------ Bouton "OK"
        self.bouton_ok = tk.Button(self.frame_boutons, text="OK", command=self.destroy)
        self.bouton_ok.pack(side=tk.RIGHT, expand=True)

    def lancer_verif_update(self):
        self.systeme_verif_update = SystemeVerifUpdate()
        self.bouton_verif_mises_a_jour.config(state="disabled", cursor="watch")
        self.systeme_verif_update.defCallbackFinVerifMag(lambda: self.bouton_verif_mises_a_jour.config(state="normal", cursor="arrow"))
        self.systeme_verif_update.lancerVerifUpdate()
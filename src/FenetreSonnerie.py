import tkinter as tk
from tkinter import ttk
# ------------------------ fichiers de l'application
from Utiles import *

class FenetreEssayerSonnerie(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # ------------------------ Configuration de la fenêtre
        self.title("Essayer la sonnerie")
        self.resizable(False, False)
        self.config(background=couleurs.clair)
        self.protocol("WM_DELETE_WINDOW", self.fermer_fenetre_essayer_sonnerie_et_arreter_sonnerie)
        # ------------------------ Configuration du style ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ------------------------ Frame pour les boutons
        self.frame_boutons = tk.Frame(self, background=couleurs.clair)
        self.frame_boutons.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        # ------------------------ Bouton pour jouer la sonnerie
        self.bouton_jouer_sonnerie = ttk.Button(self.frame_boutons, text="Jouer la sonnerie", command=lambda: jouer_sonnerie(True))
        self.bouton_jouer_sonnerie.grid(row=0, column=0, padx=10, pady=10)
        # ------------------------ Bouton pour arrêter la sonnerie
        self.bouton_stopper_sonnerie = ttk.Button(self.frame_boutons, text="Arrêter la sonnerie", command=lambda: jouer_sonnerie(False))
        self.bouton_stopper_sonnerie.grid(row=0, column=1, padx=10, pady=10)

    def fermer_fenetre_essayer_sonnerie_et_arreter_sonnerie(self):
        jouer_sonnerie(False)
        self.destroy()
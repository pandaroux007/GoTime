import tkinter as tk
from tkinter import ttk
import sys, os
# ------------------------ fichiers de l'application
from SystemeAppUpdate import SystemeAppUpdate
# l'importation relative ne fonctionnant pas, obligation d'ajouter les fichiers au PATH de python...
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))
from InfoApp import *

repertoire_courant = os.path.abspath(os.path.realpath(sys.argv[0]))
fichier_icone_select_theme = os.path.join(os.path.dirname(repertoire_courant), "select_theme.png")
fichier_theme_azure_tcl = os.path.join(os.path.dirname(repertoire_courant), "azure.tcl")

class FenetreUpdate(tk.Tk):
    def __init__(self):
        super().__init__()
        self.theme = "DARK"
        self.theme_appli_select_par_utilisateur = str(sys.argv[1])
        self.url_telechargement = str(sys.argv[2])
        # ------------------------ paramètrage de la fenêtre du système de MàJ
        self.title(f"Mise à jour de {nom_application}")
        self.geometry("400x200")
        self.resizable(False, False)
        # appliquer le theme "Azure" (sous licence MIT)
        self.tk.call("source", f"{fichier_theme_azure_tcl}")
        if self.theme_appli_select_par_utilisateur == "DARK":
            self.tk.call("set_theme", "dark")
        else:
            self.tk.call("set_theme", "light")
        # ------------------------ boite englobante contenant la partie importante de la fenêtre
        self.frame_princiale = ttk.Frame(self)
        self.frame_princiale.pack(fill=tk.BOTH, expand=True, pady=(10, 0), padx=20)
        # ------------------------ titre de la fenêtre
        self.titre = ttk.Label(self.frame_princiale, text="Mise à jour en cours...", font=("TkDefaultFont", 12))
        self.titre.pack(pady=(0, 20))
        # ------------------------ barre de progression
        self.barre_de_progression_maj = ttk.Progressbar(self.frame_princiale, length=320, mode='determinate')
        self.barre_de_progression_maj.pack()
        # ------------------------ sortie texte pour afficher l'état de l'installation
        self.sortie_etapes_installation = tk.Text(self, wrap="word", borderwidth=1, relief="solid", state="disabled")
        self.sortie_etapes_installation.pack(expand=True, pady=10, padx=10)
        # ------------------------ bouton (masqué par défaut) pour quitter l'outil de mise à jour
        self.bouton_action_maj = ttk.Button(self, text="Lancer la mise à jour", command=self.action_bouton_maj)
        self.bouton_action_maj.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def update_progression(self, valeur_progression, txt_statut):
        self.barre_de_progression_maj['value'] = valeur_progression
        self.sortie_etapes_installation.config(state="normal")
        self.sortie_etapes_installation.insert(tk.END, "\n" + txt_statut)
        self.sortie_etapes_installation.config(state="disabled")
        self.update_idletasks()

    def action_bouton_maj(self):
        # creation de l'instance de l'outil de màj
        self.systeme_maj = SystemeAppUpdate()
        self.systeme_maj.defCallbackFinInstallMag(lambda: self.bouton_action_maj.config(text="Installation terminée, quitter la MàJ", command=lambda: self.destroy and sys.exit))
        self.systeme_maj.telecharger_et_installer_mise_a_jour()

if __name__ == "__main__":
    root = FenetreUpdate()
    root.mainloop()
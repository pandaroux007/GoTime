import tkinter as tk
from tkinter import messagebox
from threading import Thread
from packaging import version
import re
import webbrowser
import socket
from urllib import request
# ------------------------ fichiers de l'application
from Definitions import *

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
        self.bouton_verif_mises_a_jour = tk.Button(self.frame_boutons, text="Vérifier les mises à jour maintenant", command=self.lancer_verif_mise_a_jour)
        self.bouton_verif_mises_a_jour.pack(side=tk.LEFT, expand=True)
        # ------------------------ Bouton "OK"
        self.bouton_ok = tk.Button(self.frame_boutons, text="OK", command=self.destroy)
        self.bouton_ok.pack(side=tk.RIGHT, expand=True)

    def verif_connection(self):
        try:
            # ------------------------ on tente de se connecter à un serveur DNS de google
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except (socket.timeout, OSError):
            return False

    def verif_acces_api_github(self):
        try:
            # ------------------------ on essaye de faire une requête à l'api de github
            socket.create_connection(("api.github.com", 443), timeout=5)
            return True
        except (socket.timeout, OSError):
            return False
        
    def lancer_verif_mise_a_jour(self):
        self.bouton_verif_mises_a_jour.config(state="disabled", cursor="watch")
        Thread(target=self.process_verif_mise_a_jour, daemon=True).start()
    
    def process_verif_mise_a_jour(self):
        if not self.verif_connection():
            self.after(0, lambda: messagebox.showwarning("Pas d'Internet", "Aucune connexion Internet détectée. Veuillez vérifier votre connexion et réessayer."))
            self.after(0, lambda: self.bouton_verif_mises_a_jour.config(state="normal", cursor="arrow"))
            return
        if not self.verif_acces_api_github():
            self.after(0, lambda: messagebox.showwarning("GitHub inaccessible", "Impossible d'accéder à GitHub. Veuillez vérifier votre connexion Internet et réessayer."))
            self.after(0, lambda: self.bouton_verif_mises_a_jour.config(state="normal", cursor="arrow"))
            return
        self.verif_mise_a_jour()
    
    # utilisation de self.after(0, ...) pour modifier la gui depuis le thread car tkinter n'est pas thread-safe
    def verif_mise_a_jour(self):
        try:
            # ------------------------ Requête à l'api de github pour obtenir la dernière version
            url = "https://api.github.com/repos/" + developpeur_application + "/" + nom_application + "/releases/latest"
            with request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())
                derniere_version_app_sur_github = data['tag_name']
            # ------------------------ enlever les éléments inutiles dans le numéro de version
            version_app_local = re.sub(r"[^\d.]", "", version_application)
            version_app_github = re.sub(r"[^\d.]", "", derniere_version_app_sur_github)
            # ------------------------ comparer les deux versions
            if version.parse(version_app_local) < version.parse(version_app_github):
                def afficher_message_mise_a_jour_dispo():
                    reponse = messagebox.askyesno(
                        title="Mise à jour disponible", icon="info",
                        message=f"Une nouvelle version {version_app_github} de {nom_application} est disponible!\n\nVoulez-vous ouvrir la page de téléchargement ?")
                    if reponse == tk.YES: webbrowser.open_new_tab(url=lien_du_github + "/releases/latest")
                self.after(0, afficher_message_mise_a_jour_dispo)
            else: self.after(0, lambda: messagebox.showinfo(title="Aucune mise à jour disponible", message=f"Aucune nouvelle version de {nom_application} n'est disponible!"))
        # ------------------------ Si une erreur est levée afficher un message d'avertissement
        except Exception as e:
            self.after(0, lambda: messagebox.showwarning(title="Avertissement", message=f"Erreur lors de la vérification des mises à jour!\n{e}"))
        # ------------------------ réactiver le bouton de verif des mises à jours
        finally: self.after(0, lambda: self.bouton_verif_mises_a_jour.config(state="normal", cursor="arrow"))
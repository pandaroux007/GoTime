import re
import json
import socket
import os, subprocess, sys
from tkinter import messagebox
from urllib import request
from threading import Thread
from packaging import version
# ------------------------ fichiers de l'application
from Utiles import log_error, systeme_exploitation
from InfoApp import *
from CheminsFichiers import chemin_programme_maj

class SystemeVerifUpdate():
    def __init__(self):
        super().__init__()
        self.callback_fin_verif_maj = None
        self.lien_telechargement_zip = None
        self.maj_disponible = False

    def verif_connection(self):
        try:
            # on essaye de faire une requête à l'api de GitHub
            socket.create_connection(("api.github.com", 443), timeout=3)
            return True
        except (socket.timeout, OSError): # pas d'Internet ou api indisponible
            messagebox.showwarning("GitHub inaccessible", "Impossible d'accéder à GitHub pour vérifier les MàJ. Vérifiez votre connexion Internet et réessayez.")
            return False

    def defCallbackFinVerifMag(self, param_callback_fin_verif_maj=None):
        self.callback_fin_verif_maj = param_callback_fin_verif_maj

    def lancerVerifUpdate(self):
        try: 
            Thread(target=self.process_verif_mise_a_jour, daemon=True).start()
            return True
        except Exception:
            return False

    def process_verif_mise_a_jour(self):
        if self.verif_connection() == True:
            try:
                # Requête à l'api de github pour obtenir la dernière version
                url = "https://api.github.com/repos/" + developpeur_application + "/" + nom_application + "/releases/latest"
                with request.urlopen(url, timeout=10) as response:
                    donnees = json.loads(response.read().decode())
                    derniere_version_app_sur_github = donnees['tag_name']
                
                # enlever les éléments inutiles dans le numéro de version
                self.version_app_local = re.sub(r"[^\d.]", "", version_application)
                self.version_app_github = re.sub(r"[^\d.]", "", derniere_version_app_sur_github)

                # comparer les deux versions
                if version.parse(self.version_app_local) < version.parse(self.version_app_github):
                    reponse = messagebox.askyesno(title="Mise à jour disponible", icon="info", message=f"Une nouvelle version {self.version_app_github} de {nom_application} est disponible!\n\nVoulez-vous l'installer ?")
                    if reponse == messagebox.YES:
                        zip_asset = next((asset for asset in donnees['assets'] if asset['name'].endswith('.zip')), None)
                        if zip_asset is not None:
                            self.lancerProgUpdate(chemin_programme_maj, zip_asset['browser_download_url'])
                        else:
                            erreur = "Impossible de lancer l'outil de mise à jour: aucun lien de téléchargement trouvé!"
                            messagebox.showerror(title="Erreur", message=erreur)
                            log_error(erreur)
                            del erreur
                else:
                    messagebox.showinfo(title="Aucune mise à jour disponible", message=f"Aucune nouvelle version de {nom_application} n'est disponible!")
            
            # Si une erreur est levée afficher un message d'erreur
            except Exception as e:
                messagebox.showerror(title="Erreur", message=f"Erreur lors de la vérification des mises à jour!\n{str(e)}")
                log_error(str(e))
        
        if self.callback_fin_verif_maj is not None:
            self.callback_fin_verif_maj()

    # ------------------------------------------------ Fonction à tester!
    def lancerProgUpdate(self, nom_fichier_programme_update, lien_telechargement_zip_maj):
        if self.maj_disponible == True:
            try:
                chemin_fichier_prog_update_version_python = str(nom_fichier_programme_update) + ".py"
                chemin_fichier_prog_update_version_win_exec = str(nom_fichier_programme_update) + ".exe"
                # si le programme des MàJ est la version python
                if os.path.exists(chemin_fichier_prog_update_version_python):
                    subprocess.Popen([sys.executable, chemin_fichier_prog_update_version_python, sys.argv[1]]) # lien_telechargement_zip_maj ?????????
                    sys.exit(0)
                # si le programme des MàJ est compilé
                elif systeme_exploitation == "win32":
                    if os.path.exists(chemin_fichier_prog_update_version_win_exec):
                        subprocess.Popen([chemin_fichier_prog_update_version_win_exec])
                        sys.exit(0)
                elif systeme_exploitation == ("linux" or "darwin"):
                    if os.path.exists(nom_fichier_programme_update) and os.access(nom_fichier_programme_update, os.X_OK):
                        subprocess.Popen([nom_fichier_programme_update])
                        sys.exit(0)
                # sinon afficher erreur
                else: messagebox.showerror(title="Lancement MàJ impossible", message="Impossible de lancer le programme de mise à jour : fichier exécutable introuvable ou inexistant")
            except Exception as e:
                messagebox.showerror(title="Erreur lancement MàJ", message=f"Une erreur s'est produite : {str(e)}")
                log_error(str(e))
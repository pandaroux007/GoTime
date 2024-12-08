import sys
from getpass import getuser
from socket import gethostname
from datetime import datetime
# ------------------------ fichiers de l'application
from CheminsFichiers import *

# ------------------------ Couleurs
class Couleurs:
    sombre = "#242424"
    clair = "#FFFFFF"
    frame_verte = "#73FF14"
    frame_jaune = "#F4EF12"
    frame_rouge = "#F84615"

# ------------------------ Fonctions utiles
def log_error(message_erreur):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getuser()
    hostname = gethostname()
    error_data = f"{timestamp}   |   {username} sur {hostname}   |   {message_erreur}"
    with open(chemin_fichier_logs, mode='a', newline='') as file:
        if file.tell() == 0:  # verif si le fichier est vide
            header = "Date + Heure   |   User et hostname   |   Erreur"
            file.write(f"{header}\n")
        file.write(f"{error_data}\n")

sonnerie_actuelle = None
def jouer_sonnerie(etat_jouer_son):
    try:
        from pygame import mixer
        mixer.init()
        global sonnerie_actuelle
        if sonnerie_actuelle is None:
            sonnerie_actuelle = mixer.Sound(chemin_fichier_wav_fin_temps)
        if etat_jouer_son: sonnerie_actuelle.play()
        else: sonnerie_actuelle.stop()
    except Exception as e: log_error(f"Exception dans la fonction jouer_sonnerie : {str(e)}"); pass

# ------------------------ Variables utiles
systeme_exploitation = sys.platform
temps_max = 10800 # 3 heures en secondes
couleurs = Couleurs()
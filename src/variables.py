import os
import sys
from tkinter import messagebox
from json import load, dump
from platform import system
import getpass
import socket
from datetime import datetime
# https://stackoverflow.com/questions/59427353/how-to-get-the-current-path-of-compiled-binary-from-python-using-nuitka
repertoire_courant = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))
chemin_fichier_parametres = os.path.join(os.path.dirname(repertoire_courant), "dep", "settings.json")
chemin_fichier_logs = os.path.join(os.path.dirname(repertoire_courant), 'log', "error_log.csv")
chemin_image_application = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'icon.ico')
chemin_image_checkmark = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'checkmark.png')
chemin_fichier_wav_fin_temps = os.path.join(os.path.dirname(repertoire_courant), 'sons', 'digital-clock-alarm.wav')
chemin_fichier_licence = os.path.join(os.path.dirname(repertoire_courant), "LICENCE.txt")

lien_du_github = "https://github.com/pandaroux007/GoTime"
nom_application = "GoTime"
version_application = "1.0.0" # version compilée, distribuable et fonctionnelle à 100%

def load_config():
    try:
        with open(chemin_fichier_parametres, 'r') as file:
            config = load(file)
        return config
    except FileNotFoundError:
        messagebox.showerror(title=f"Erreur", message=f"Le fichier de paramètre de {nom_application} n'a pas été trouvé pour lecture.\r\n {chemin_fichier_parametres}")
        return None; exit()
    
def save_config(config):
    try:
        with open(chemin_fichier_parametres, 'w') as file:
            dump(config, file, indent=4)
    except FileNotFoundError:
        messagebox.showerror(title=f"Erreur", message=f"Le fichier de paramètre de {nom_application} n'a pas été trouvé pour écriture.")
        return None; exit()

def log_error(error_message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    username = getpass.getuser()
    hostname = socket.gethostname()

    error_data = f"{timestamp}   |   {username} sur {hostname}   |   {error_message}"

    with open(chemin_fichier_logs, mode='a', newline='') as file:
        if file.tell() == 0:  # Vérifie si le fichier est vide
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
        if etat_jouer_son:
            sonnerie_actuelle.play()
        else:
            sonnerie_actuelle.stop()
    except Exception as e: log_error(e); pass

parametres_fichier_json = load_config()
systeme_exploitation = system()
theme_sombre = "#242424"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max = 10800 # 3 heures en secondes
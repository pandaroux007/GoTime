from os import path
from tkinter import messagebox
from json import load, dump
from platform import system
import getpass
import socket
from datetime import datetime

repertoire_courant = path.dirname(path.abspath(__file__))
chemin_fichier_parametres = path.join(path.dirname(repertoire_courant), "log", "settings.json")
chemin_fichier_logs = path.join(path.dirname(repertoire_courant), 'log', "error_log.csv")
chemin_image_application = path.join(path.dirname(repertoire_courant), 'dep', 'icon.ico')
chemin_image_checkmark = path.join(path.dirname(repertoire_courant), 'dep', 'checkmark.png')
chemin_fichier_wav_fin_temps = path.join(path.dirname(repertoire_courant), 'dep', 'digital-clock-alarm.wav')
chemin_fichier_licence = path.join(path.dirname(repertoire_courant), "LICENCE.txt")
lien_du_github = "https://github.com/RP7-CODE/GoTime"
nom_application = "GoTime"
version_application = "1.0.1"

def load_config():
    try:
        with open(chemin_fichier_parametres, 'r') as file:
            config = load(file)
        return config
    except FileNotFoundError:
        messagebox.showerror(title=f"Erreur", message=f"Le fichier de paramètre de {nom_application} n'a pas été trouvé pour lecture.")
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
    except ImportError: pass

parametres_fichier_json = load_config()
systeme_exploitation = system()
theme_sombre = "#242424"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max = 10800 # 3 heures en secondes
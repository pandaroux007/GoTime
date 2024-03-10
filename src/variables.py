from os import path
from tkinter import messagebox
from json import load, dump
from platform import system

repertoire_courant = path.dirname(path.abspath(__file__))
chemin_fichier_parametres = path.join(repertoire_courant, "settings.json")
chemin_fichier_licence = path.join(path.dirname(repertoire_courant), "LICENCE.txt")
chemin_image_application = path.join(path.dirname(repertoire_courant), 'img', 'icon.ico')
lien_du_github = "https://github.com/RP7-CODE/GoTime"
nom_application = "GoTime"
version_application = "0.29.1"

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

parametres_fichier_json = load_config()
systeme_exploitation = system()
theme_sombre = "#242424"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max = 10800 # 3 heures
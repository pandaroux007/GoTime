import os, sys, json
from platform import system
from getpass import getuser
from socket import gethostname
from datetime import datetime

# ------------------------ Def des chemins de fichiers
# https://github.com/Nuitka/Nuitka/issues/1737#issuecomment-1224488673
# https://stackoverflow.com/questions/59427353/how-to-get-the-current-path-of-compiled-binary-from-python-using-nuitka
repertoire_courant = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))
""" # variables définie par nuitka lors de la compilation (UNIQUEMENT Nuitka, pas un autre compilateur!)
chemin_fichier_parametres = os.path.join(repertoire_courant, "dep", "settings.json")
chemin_fichier_logs = os.path.join(repertoire_courant, 'log', "error_log.csv")
chemin_image_application = os.path.join(repertoire_courant, 'dep', 'icon.png')
chemin_image_checkmark = os.path.join(repertoire_courant, 'dep', 'checkmark.png')
chemin_fichier_wav_fin_temps = os.path.join(repertoire_courant, 'sons', 'digital-clock-alarm.wav')
chemin_fichier_licence = os.path.join(repertoire_courant, "LICENCE.txt") """
chemin_fichier_parametres = os.path.join(os.path.dirname(repertoire_courant), "dep", "settings.json")
chemin_fichier_logs = os.path.join(os.path.dirname(repertoire_courant), 'log', "error_log.csv")
chemin_image_application = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'icon.png')
chemin_image_checkmark = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'checkmark.png')
chemin_fichier_wav_fin_temps = os.path.join(os.path.dirname(repertoire_courant), 'sons', 'digital-clock-alarm.wav')
chemin_fichier_licence = os.path.join(os.path.dirname(repertoire_courant), "LICENCE.txt")

class Parametres():
    def __init__(self):
        # ------------------------ valeurs par défaut
        self.value_theme = "DEFAULT"
        self.value_affichage_heure = True
        self.value_sounds = False
        # ------------------------ verif si fichier présent puis lecture
        self.charger_parametres()

    def charger_parametres(self):
        if os.path.exists(chemin_fichier_parametres):
            try:
                with open(chemin_fichier_parametres, 'r') as fichier:
                    try: # mettre à jour les attributs
                        donnees = json.load(fichier)
                        self.value_theme = donnees.get("value_theme", self.value_theme)
                        self.value_affichage_heure = donnees.get("value_affichage_heure", self.value_affichage_heure)
                        self.value_sounds = donnees.get("value_sounds", self.value_sounds)
                    except json.JSONDecodeError: log_error(f"Le fichier de paramètres est corrompu. Les valeurs par défaut seront utilisés.")
            except FileNotFoundError: log_error(f"Le fichier de paramètres n'a pas été trouvé. Les valeurs par défaut seront utilisés.")
        # si le fichier n'existe pas, le créer avec les valeurs par défaut
        else: self.sauvegarde()

    def sauvegarde(self):
        # ------------------------ sérialiser les paramètres de la classe dans le fichier
        donnees = {
            "value_theme": self.value_theme,
            "value_affichage_heure": self.value_affichage_heure,
            "value_sounds": self.value_sounds
        }
        with open(chemin_fichier_parametres, 'w') as fichier:
            json.dump(donnees, fichier, indent=4)

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
    except Exception as e: log_error(f"Exception dans la fonction jouer_sonnerie : {e}"); pass

# ------------------------ Variables utiles
systeme_exploitation = system()
parametres = Parametres()
theme_sombre = "#242424"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max = 10800 # 3 heures en secondes

# ------------------------ Infos App
lien_du_github = "https://github.com/pandaroux007/GoTime"
nom_application = "GoTime"
version_application = "1.0.3-bêta"
developpeur_application = "Pandaroux007"
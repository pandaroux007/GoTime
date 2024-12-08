import json, os
# ------------------------ fichiers de l'application
from CheminsFichiers import *
from Utiles import log_error

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

parametres = Parametres()
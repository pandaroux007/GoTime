import os, sys

# ------------------------ Def des chemins de fichiers
# https://github.com/Nuitka/Nuitka/issues/1737#issuecomment-1224488673
# https://stackoverflow.com/questions/59427353/how-to-get-the-current-path-of-compiled-binary-from-python-using-nuitka
repertoire_courant = os.path.dirname(os.path.abspath(os.path.realpath(sys.argv[0])))

chemin_fichier_parametres = os.path.join(os.path.dirname(repertoire_courant), "dep", "settings.json")
chemin_fichier_logs = os.path.join(os.path.dirname(repertoire_courant), 'log', "error_log.csv")
chemin_image_application = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'icon.png')
chemin_image_info = os.path.join(os.path.dirname(repertoire_courant), 'dep', 'info.png')
chemin_fichier_wav_fin_temps = os.path.join(os.path.dirname(repertoire_courant), 'sons', 'digital-clock-alarm.wav')
chemin_fichier_licence = os.path.join(os.path.dirname(repertoire_courant), "LICENCE.txt")
chemin_programme_maj = os.path.join(repertoire_courant, "update", "FenetreUpdate")

del os, sys
import requests
import sys, os
import tempfile
import zipfile
import json
import shutil
import subprocess

class SystemeAppUpdate():
    def __init__(self, barre_de_progression_master, url, version):
        self.barre_de_progression = barre_de_progression_master
        self.master = self.barre_de_progression.master
        self.url_nouvelle_version = url
        self.version = version
        self.callback_fin_maj = None

    def defCallbackFinInstallMag(self, callback_fin_maj):
        self.callback_fin_maj = callback_fin_maj

    def telecharger_et_installer_mise_a_jour(self):
        self.barre_de_progression.update_progression(0, "Préparation de la mise à jour...")
        # en cours...
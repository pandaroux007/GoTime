#!/bin/bash

set -e # arrête le script si une commande échoue
# Vérification des droits root
if [ "$EUID" -ne 0 ]; then
    echo -e "\e[1;31mERREUR! Ce script doit être exécuté en tant que superutilisateur (utiliser la commande 'sudo ./install.sh')" && exit 1
fi

# def des chemins
APP_NAME="GoTime"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/$APP_NAME.desktop"
ICON_FILE="$INSTALL_DIR/dep/icon.png"
EXEC_NAME="gotime-linux"

echo "Merci d'avoir téléchargé et installé $APP_NAME! Démarrage du programme d'installation..."
# verif fichiers sources
for file in "LICENCE.txt" "sons" "log" "dep"; do
    if [ ! -e "$PWD/$file" ]; then
        echo -e "\e[1;31mERREUR! Le fichier ou dossier '$file' est manquant."
    else
        echo -e "\e[1;33mINFO! Le fichier ou dossier '$file' est présent."
    fi
done

if [ -d "$INSTALL_DIR" ]; then
    echo -e "\e[1;33mWARNING! L'application est déjà installée, elle va être remplacée (cela va supprimer vos paramètres)..."
    sleep 1s && rm -rf "$INSTALL_DIR" && echo -e "\t >> Répertoire d'une installation précédente supprimé!"
    if [ -f "$DESKTOP_FILE" ]; then
        rm "$DESKTOP_FILE" && echo -e "\t >> Fichier .desktop d'une installation précédente supprimé!"
    fi
fi

# creer le répertoire d'installation
mkdir -p "$INSTALL_DIR" || { echo -e "\e[1;31mERREUR! IMpossible de créer le répertoire d'installation"; exit 1; }
echo ">> Création du répertoire d'installation au chemin $INSTALL_DIR"
mv "$EXEC_NAME" "$INSTALL_DIR/" && echo ">> Déplacement du fichier exécutable $EXEC_NAME dans $INSTALL_DIR"
mv sons log dep "$INSTALL_DIR/" && echo ">> Déplacement des dossiers de dépendance 'sons', 'log', et 'dep' dans $INSTALL_DIR"
cp LICENCE.txt README.md "$INSTALL_DIR/" && echo ">> Copie des fichiers LICENCE.txt et README.md dans $INSTALL_DIR"

echo "Création du fichier $APP_NAME.desktop dans $DESKTOP_FILE..."
# creer l'entrée dans le menu démarrer
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0.2-beta
Name=$APP_NAME
Comment=Une application de minuteur/timer
Exec=$INSTALL_DIR/$EXEC_NAME
Terminal=false
Icon=$ICON_FILE
Type=Application
Categories=Office;
EOF
echo ">> Création du fichier $APP_NAME.desktop terminée!"

chmod +x "$INSTALL_DIR/$EXEC_NAME" && echo "Ajout de l'autorisation d'exécution au fichier exécutable..."
update-desktop-database && echo "Mise à jour de la base de données des applis..."
echo ">> Mise à jour de la base de données terminée!"

echo -e "\e[1;32mSUCCESS! Installation de $APP_NAME terminée avec succès!"
echo -n "Voulez-vous supprimer ce script d'installation ? [Y/n] "
read reponse

# convertir la réponse en minuscules
reponse=$(echo "$reponse" | tr '[:upper:]' '[:lower:]')

if [[ $reponse == "y" || $reponse == "yes" || $reponse == "" ]]; then
    echo "Suppression du script d'installation..." && rm "$0"
    echo "Script d'installation supprimé." && exit 0
else
    echo "Le script d'installation n'a pas été supprimé." && exit 0
fi
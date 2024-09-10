#!/bin/bash

set -e # arrête le script si une commande échoue

# def des chemins
APP_NAME="GoTime"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/$APP_NAME.desktop"
ICON_FILE="$INSTALL_DIR/dep/icon.png"
EXEC_NAME="gotime-linux"
# def des raccourcis pour les couleurs
COLOR_ERROR_RED="\e[1;31m"
COLOR_SUCCESS_GREEN="\e[1;32m"
COLOR_WARN_YELLOW="\e[1;33m"
COLOR_TERMINAL_DEFAULT="\e[0;0m"

# verif des droits root
if [ "$EUID" -ne 0 ]; then
    echo -e "${COLOR_ERROR_RED}ERREUR! Ce script doit être exécuté en tant que superutilisateur (utiliser la commande 'sudo ./install.sh')${COLOR_TERMINAL_DEFAULT}" && exit 1
fi

echo "Merci d'avoir téléchargé et installé $APP_NAME! Démarrage du programme d'installation..."
# verif fichiers sources
for file in "LICENCE.txt" "sons" "log" "dep"; do
    if [ ! -e "$PWD/$file" ]; then
        echo -e "${COLOR_ERROR_RED}ERREUR! Le fichier ou dossier '$file' est manquant.${COLOR_TERMINAL_DEFAULT}" && exit 1
    fi
done

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${COLOR_WARN_YELLOW}WARNING! L'application est déjà installée, elle va être remplacée (cela va supprimer vos paramètres)...${COLOR_TERMINAL_DEFAULT}"
    sleep 1s && rm -rf "$INSTALL_DIR" && echo -e "\t >> Répertoire d'une installation précédente supprimé!"
    if [ -f "$DESKTOP_FILE" ]; then
        rm "$DESKTOP_FILE" && echo -e "\t >> Fichier .desktop d'une installation précédente supprimé!"
    fi
fi

# creer le répertoire d'installation
mkdir -p "$INSTALL_DIR" || { echo -e "${COLOR_ERROR_RED}ERREUR! Impossible de créer le répertoire d'installation${COLOR_TERMINAL_DEFAULT}"; exit 1; }
echo ">> Création du répertoire d'installation au chemin $INSTALL_DIR"
mv "$EXEC_NAME" "$INSTALL_DIR/" || { echo -e "${COLOR_ERROR_RED}ERREUR! Impossible de déplacer le fichier exécutable $EXEC_NAME dans $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"; exit 1; }
echo ">> Déplacement du fichier exécutable $EXEC_NAME dans $INSTALL_DIR"
mv sons log dep "$INSTALL_DIR/" || { echo -e "${COLOR_ERROR_RED}ERREUR! Impossible de déplacer les dossiers de dépendance dans $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"; exit 1; }
echo ">> Déplacement des dossiers de dépendance 'sons', 'log', et 'dep' dans $INSTALL_DIR"
cp LICENCE.txt "$INSTALL_DIR/" || { echo -e "${COLOR_ERROR_RED}ERREUR! Impossible de copier LICENCE.txt dans $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"; exit 1; }
echo ">> Copie des fichiers LICENCE.txt dans $INSTALL_DIR"

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
if command -v update-desktop-database > /dev/null 2>&1; then
    echo "Mise à jour de la base de données des applis..."
    update-desktop-database
    echo ">> Mise à jour de la base de données terminée!"
else
    echo -e "${COLOR_WARN_YELLOW}WARNING! update-desktop-database n'est pas disponible. Vous devrez peut-être l'exécuter manuellement ou redémarrer votre ordinateur pour voir le logiciel dans la liste des applications installées.${COLOR_TERMINAL_DEFAULT}"
fi

echo -e "${COLOR_SUCCESS_GREEN}SUCCESS! Installation de $APP_NAME terminée avec succès!${COLOR_TERMINAL_DEFAULT}"
# verif pour supprimer le script d'installation à la fin
while true; do
    read -p "Voulez-vous supprimer ce script d'installation ? [Y/n] " reponse
    reponse=$(echo "$reponse" | tr '[:upper:]' '[:lower:]')
    if [[ $reponse == "y" || $reponse == "yes" || $reponse == "" ]]; then
        echo "Suppression du script d'installation..." && rm "$0"
        echo ">> Script d'installation supprimé!" && exit 0
    elif [[ $reponse == "n" || $reponse == "no" ]]; then
        echo ">> OK - fin du script d'installation de $APP_NAME" && exit 0
    else
        echo -e "${COLOR_WARN_YELLOW}Veuillez entrer 'Y' pour oui ou 'N' pour non.${COLOR_TERMINAL_DEFAULT}"
    fi
done
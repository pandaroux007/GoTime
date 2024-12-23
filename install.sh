#!/bin/bash

set -e # stops the script if a command fails

# path def
APP_NAME="GoTime"
APP_VERSION="v2.0.0-beta"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/$APP_NAME.desktop"
ICON_FILE="$INSTALL_DIR/dep/icon.png"
EXEC_NAME="gotime-linux"
# def shortcuts for colors
COLOR_ERROR_RED="\e[1;31m"
COLOR_SUCCESS_GREEN="\e[1;32m"
COLOR_WARN_YELLOW="\e[1;33m"
COLOR_TERMINAL_DEFAULT="\e[0;0m"

# root rights check
if [ "$EUID" -ne 0 ]; then
    echo -e "${COLOR_ERROR_RED}ERROR! This script must be run as superuser (use command 'sudo ./install.sh')${COLOR_TERMINAL_DEFAULT}" && exit 1
fi

echo "Thank you for downloading and installing $APP_NAME! Starting the installer..."
# check file sources
for file in "LICENSE.txt" "sound" "log" "dep"; do
    if [ ! -e "$PWD/$file" ]; then
        echo -e "${COLOR_ERROR_RED}ERROR! The file or folder '$file' is missing.${COLOR_TERMINAL_DEFAULT}" && exit 1
    fi
done

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${COLOR_WARN_YELLOW}WARNING! The application is already installed, it will be replaced (this will delete your settings)...${COLOR_TERMINAL_DEFAULT}"
    sleep 1s && rm -rf "$INSTALL_DIR" && echo -e "\t >> Directory from previous installation deleted!"
    if [ -f "$DESKTOP_FILE" ]; then
        rm "$DESKTOP_FILE" && echo -e "\t >> '.desktop' file from previous installation deleted!"
    fi
fi

# create the installation directory
mkdir -p "$INSTALL_DIR" || {
    echo -e "${COLOR_ERROR_RED}ERROR! Unable to create installation directory${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Creating the installation directory at path $INSTALL_DIR"

mv "$EXEC_NAME" "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}ERROR! Unable to move executable file $EXEC_NAME to $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Moving the executable file $EXEC_NAME to $INSTALL_DIR"

mv sound log dep "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}ERROR! Unable to move dependency folders into $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Moved 'sound', 'log', and 'dep' dependency folders to $INSTALL_DIR"

cp LICENSE.txt "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}ERROR! Unable to copy LICENSE.txt to $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Copy the LICENSE.txt file to $INSTALL_DIR"

echo "Creating file $APP_NAME.desktop in $DESKTOP_FILE..."
# create entry in start menu
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=$APP_VERSION
Name=$APP_NAME
Comment=A timer application
Exec=$INSTALL_DIR/$EXEC_NAME
Terminal=false
Icon=$ICON_FILE
Type=Application
Categories=Office;
EOF
echo ">> Creation of $APP_NAME.desktop file completed!"

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
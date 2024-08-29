#!/bin/bash

# Vérifier si l'utilisateur a les droits root
if [ "$EUID" -ne 0 ]; then
  echo "Ce script doit être exécuté en tant que root (utiliser la commande 'sudo ./install.sh')"
  exit 1
fi

# Définir les chemins
APP_NAME="GoTime"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/$APP_NAME.desktop"
ICON_FILE="$INSTALL_DIR/dep/icon.png"
EXEC_NAME="gotime-linux"

# Créer le répertoire d'installation
mkdir -p "$INSTALL_DIR"

# Copier l'exécutable et les dossiers de dépendances
cp "$EXEC_NAME" "$INSTALL_DIR/"
cp -r sons log dep "$INSTALL_DIR/"

# Créer l'entrée dans le menu démarrer
cat > "$DESKTOP_FILE" << EOF
[Desktop Entry]
Version=1.0
Name=$APP_NAME
Comment=Une application de minuteur/timer
Exec=$INSTALL_DIR/$EXEC_NAME
Terminal=false
Icon=$ICON_FILE
Type=Application
Categories=Office;
EOF

# Rendre l'exécutable... exécutable
chmod +x "$INSTALL_DIR/$EXEC_NAME"

# Mettre à jour la base de données des applications
update-desktop-database

echo "Installation de $APP_NAME terminée avec succès !"
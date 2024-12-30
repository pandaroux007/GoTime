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
COLOR_ERROR_RED="\e[1;31mERROR! "
COLOR_SUCCESS_GREEN="\e[1;32mSUCCESS! "
COLOR_WARN_YELLOW="\e[1;33mWARNING! "
COLOR_TERMINAL_DEFAULT="\e[0;0m"

# root rights check
if [ "$EUID" -ne 0 ]; then
    echo -e "${COLOR_ERROR_RED}This script must be run as superuser (use command 'sudo ./install.sh')${COLOR_TERMINAL_DEFAULT}" && exit 1
fi

echo "Thank you for downloading and installing $APP_NAME! Starting the installer..."
# check file sources
for file in "LICENSE.txt" "sound" "log" "dep"; do
    if [ ! -e "$PWD/$file" ]; then
        echo -e "${COLOR_ERROR_RED}The file or folder '$file' is missing.${COLOR_TERMINAL_DEFAULT}" && exit 1
    fi
done

if [ -d "$INSTALL_DIR" ]; then
    echo -e "${COLOR_WARN_YELLOW}The application is already installed, it will be replaced (this will delete your settings)...${COLOR_TERMINAL_DEFAULT}"
    sleep 1s && rm -rf "$INSTALL_DIR" && echo -e "\t >> Directory from previous installation deleted!"
    if [ -f "$DESKTOP_FILE" ]; then
        rm "$DESKTOP_FILE" && echo -e "\t >> '.desktop' file from previous installation deleted!"
    fi
fi

# create the installation directory
mkdir -p "$INSTALL_DIR" || {
    echo -e "${COLOR_ERROR_RED}Unable to create installation directory${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Creating the installation directory at path $INSTALL_DIR"

mv "$EXEC_NAME" "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}Unable to move executable file $EXEC_NAME to $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Moving the executable file $EXEC_NAME to $INSTALL_DIR"

mv sound log dep "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}Unable to move dependency folders into $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
    exit 1
}
echo ">> Moved 'sound', 'log', and 'dep' dependency folders to $INSTALL_DIR"

cp LICENSE.txt "$INSTALL_DIR/" || {
    echo -e "${COLOR_ERROR_RED}Unable to copy LICENSE.txt to $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
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

chmod +x "$INSTALL_DIR/$EXEC_NAME" && echo "Adding execute permission to executable file..."
if command -v update-desktop-database > /dev/null 2>&1; then
    echo "Updating the apps database..."
    update-desktop-database
    echo ">> Database update completed!"
else
    echo -e "${COLOR_WARN_YELLOW}update-desktop-database is not available. You may need to run it manually or restart your computer to see the software in the list of installed applications.${COLOR_TERMINAL_DEFAULT}"
fi

echo -e "${COLOR_SUCCESS_GREEN}Installation of $APP_NAME completed successfully!${COLOR_TERMINAL_DEFAULT}"
# check to remove the installation script at the end
while true; do
    read -p "Do you want to delete this installation script? [Y/n] " response
    response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    if [[ $response == "y" || $response == "yes" || $response == "" ]]; then
        echo "Deleting the installation script..." && rm "$0"
        echo ">> Installation script removed!" && exit 0
    elif [[ $response == "n" || $response == "no" ]]; then
        echo ">> OK - end of $APP_NAME installation script" && exit 0
    else
        echo -e "${COLOR_WARN_YELLOW}Please enter 'Y' for yes or 'N' for no.${COLOR_TERMINAL_DEFAULT}"
    fi
done
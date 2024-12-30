# USER GUIDE (EN)
## Installation
1. Download the latest version of the application in zip format [on GitHub](https://github.com/pandaroux007/GoTime/releases) or on the website here ➜ 
<p align="center">

  [![Download on the project website](https://custom-icon-badges.demolab.com/badge/-Download-blue?logo=download&logoColor=white "Download app")](https://pandaroux007.github.io/gotime)
</p>

2. Unzip the zip file, then go to the folder obtained.
### On Microsoft Windows
1. Run the installation file `gotime-win-install.exe`, then follow the instructions.
### On Linux
(must work on debian and its subdistributions)
#### *Via* the command terminal
1. Place yourself in the unzipped directory with `cd` if it is not already done.
2. Execute the command `chmod +x install.sh` to authorize the execution of the file as a program.
3. Launch the installation program with the command `sudo ./install.sh` (to launch it in superuser mode)

### On MacOS-X
The application is not compiled on Mac for now, you can run it from python3 if you want to use it (`python3 -m runApp.py`).

> [!WARNING]
> Potential incompatibilities because the application is not tested on this platform!

## Uninstall
### On Linux (and maybe MacOS-X)
Create a file `uninstall.sh`, then copy paste this bash shell script inside.
```sh
#!/bin/bash

set -e # stops the script if a command fails

# path def
APP_NAME="GoTime"
INSTALL_DIR="/opt/$APP_NAME"
DESKTOP_FILE="/usr/share/applications/$APP_NAME.desktop"
# def shortcuts for colors
COLOR_ERROR_RED="\e[1;31mERROR! "
COLOR_SUCCESS_GREEN="\e[1;32mSUCCESS! "
COLOR_WARN_YELLOW="\e[1;33mWARNING! "
COLOR_TERMINAL_DEFAULT="\e[0;0m"

# root rights check
if [ "$EUID" -ne 0 ]; then
    echo -e "${COLOR_ERROR_RED}This script must be run as superuser (use command 'sudo ./install.sh')${COLOR_TERMINAL_DEFAULT}" && exit 1
fi

# delete the installation directory
if [ -d "$INSTALL_DIR" ]; then
  rm -rf "$INSTALL_DIR" && echo ">> Installation directory deleted : $INSTALL_DIR"
else
  echo "${COLOR_WARN_YELLOW}The installation directory does not exist : $INSTALL_DIR${COLOR_TERMINAL_DEFAULT}"
fi

if [ -f "$DESKTOP_FILE" ]; then
  rm "$DESKTOP_FILE" && echo ">> Deleted .desktop file : $DESKTOP_FILE"
else
  echo "${COLOR_WARN_YELLOW}The .desktop file does not exist:$DESKTOP_FILE${COLOR_TERMINAL_DEFAULT}"
fi

if command -v update-desktop-database > /dev/null 2>&1; then
    echo "Updating the apps database..."
    update-desktop-database
    echo ">> Database update completed!"
else
    echo -e "${COLOR_WARN_YELLOW}update-desktop-database is not available. You may need to run it manually or restart your computer to no longer see the software in the list of installed applications.${COLOR_TERMINAL_DEFAULT}"
fi

echo -e "${COLOR_SUCCESS_GREEN}Uninstallation of $APP_NAME completed successfully!${COLOR_TERMINAL_DEFAULT}"
# check to remove the installation script at the end
while true; do
    read -p "Do you want to delete this uninstall script? [Y/n] " response
    response=$(echo "$response" | tr '[:upper:]' '[:lower:]')
    if [[ $response == "y" || $response == "yes" || $response == "" ]]; then
        echo "Deleting the uninstall script..." && rm "$0"
        echo ">> Uninstall script removed!" && exit 0
    elif [[ $response == "n" || $response == "no" ]]; then
        echo ">> OK - end of $APP_NAME uninstall script" && exit 0
    else
        echo -e "${COLOR_WARN_YELLOW}Please enter 'Y' for yes or 'N' for no.${COLOR_TERMINAL_DEFAULT}"
    fi
done
```
Once this is done, you can allow the file to run as a program as described in the [Installation chapter](#installation), and then launch it with the command `sudo ./uninstall.sh`.

*You can also open your file explorer in superuser mode and manually delete the installation directory in `/opt/GoTime` and the start menu entry `/usr/share/applications/GoTime.desktop`*

### On Microsoft Windows
1. Close all instances of the application (all windows)
2. Go to your Settings, then in the Applications menu search for "*GoTime*" (if you can't find it, the application is already uninstalled - to make sure, go to your file explorer, to `C:\Program Files (x86)` or `C:\Program Files`, and see if the *GoTime* folder exists.), then click uninstall.
___
@echo off

:: variables pour les noms et les chemins
set APP_NAME=GoTime
set INSTALL_DIR=C:\Program Files\%APP_NAME%
set SHORTCUT_DIR=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Office
set EXEC_NAME=gotime-windows.exe

:: répertoire d'installation
mkdir "%INSTALL_DIR%" 

:: copie l'exécutable et les dossiers de dépendances dans le répertoire d'installation
:: /E copie les sous-répertoires, même vides, et /I spécifie que la destination est un répertoire
xcopy /E /I "%EXEC_NAME%" "%INSTALL_DIR%"
xcopy /E /I "sons" "%INSTALL_DIR%\sons"
xcopy /E /I "log" "%INSTALL_DIR%\log"
xcopy /E /I "dep" "%INSTALL_DIR%\dep"

:: crée le raccourci dans le menu Démarrer
powershell -Command "$WshShell = New-Object -comObject WScript.Shell; $Shortcut = $WshShell.CreateShortcut('%SHORTCUT_DIR%\%APP_NAME%.lnk'); $Shortcut.TargetPath = '%INSTALL_DIR%\%EXEC_NAME%'; $Shortcut.IconLocation = '%INSTALL_DIR%\dep\icon.ico'; $Shortcut.Save()"

echo Installation de %APP_NAME% terminée avec succès !
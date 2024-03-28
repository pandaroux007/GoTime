# Présentation
Ce projet est une application de minuteur ne nécessitant pas de connexion Internet, qui a débuté le 9 février 2024 pour les professeurs du collège.

## Licence
Ce projet est sous [licence BSL 1.0](https://choosealicense.com/licenses/bsl-1.0/) (Boost Software License 1.0).
J'autorise quiconque à utiliser, modifier et commercialiser le code, tant que l'auteur **R-P7 - CODE** est mentionné.

## Interface
GoTime peut être agrandi et mis en plein écran. Sur la fenêtre principale, est disponible, dans l'ordre :
- Au niveau de la barre de menu, trois onglets :
  - **Fenêtre** -> Propose des options pour l'interface et l'application
  - **Commandes** -> Permet d'effectuer des actions
  - **Source** -> Donne des informations sur l'application
- L'heure, en grand, en haut (décalage de 1s environ normalement, possibilité de ne plus l'afficher dans les paramètres)
- Un rectangle coloré contenant le nom de l'application, puis le temps restant pendant le décompte.
- Trois boutons (start, stop et pause).
- Deux entrées (minutes/secondes) et un bouton pour les effacer rapidement.
- Un bouton pour déporter le temps restant dans une nouvelle fenêtre.

## Installation
Attention, certains des modules utilisés par le projet ne sont pas inclus par défauts dans python. Pour les installer, il vous suffit de
lancer la commande suivante (après vous être déplacé dans le répertoire du projet téléchargé - commande 'cd path' sous linux):
```bat
pip install -r requirements.txt
```

## Bugs
- À tester sur Windows : 
  - l'icon de l'application, qui à été modifiée.
  - le son à la fin du minuteur si option activée.
- À voir si autres...

## Fonctionnement
...
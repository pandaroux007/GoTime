<div align="center">

[![Licence](https://img.shields.io/badge/License-MIT-brightgreen.svg)](https://github.com/pandaroux007/GoTime/blob/main/LICENCE.txt)
[![GitHub Release](https://img.shields.io/github/v/release/pandaroux007/GoTime?include_prereleases&style=flat&logo=auto&color=red&link=https%3A%2F%2Fgithub.com%2Fpandaroux007%2FGoTime%2Freleases)](https://github.com/pandaroux007/GoTime/releases)
[![Built with Python3](https://img.shields.io/badge/built%20with-Python3-yellow.svg)](https://www.python.org/)
[![Commits](https://img.shields.io/github/commit-activity/t/pandaroux007/GoTime)](https://github.com/pandaroux007/GoTime/commits/main/)
[![Stars](https://img.shields.io/github/stars/pandaroux007/GoTime.svg?style=social&label=Stars)](https://github.com/pandaroux007/GoTime)
</div>

# Présentation
## Projet
Ce projet est une application de minuteur ne nécessitant pas de connexion Internet, qui a débuté le 9 février 2024 pour les professeurs du collège.
Je place le code et tout élément associé au projet sur GitHub, à ce lien : [https://github.com/pandaroux007/GoTime](https://github.com/pandaroux007/GoTime)
Pour tout signalement de bug ou proposition de nouvelle.s fonctionnalitée.s, merci de créer une [issue](https://github.com/pandaroux007/GoTime/issues).

## Licence
Ce projet est sous [Licence MIT](LICENCE.txt) - [The MIT License (MIT)](https://choosealicense.com/licenses/mit/).
Retrouvez les détails de cette licence sur le site officiel : https://opensource.org/licenses/MIT.

## Crédits
1. Merci à `Lounys` pour son aide sur le bug du bouton 'copier le lien' dans Source;
2. Merci à `Solme` pour son soutien pendant les longues phases de correction de bugs;
3. Merci à `Roucoule/PandaR09` pour son aide au début de mon apprentissage de tkinter;
4. Merci à `Petitours` pour ses conseils sur l'ergonomie et pour le module py vers exe;
5. Merci à ma professeur d'anglais, qui a lancer l'idée et qui m'a fait confiance pour réaliser ce projet;
6. Merci à tous les développeurs des modules utilisés ici pour leurs travaux et leurs contributions à la communauté open-source;
7. Enfin, merci à tous les créateurs de contenus techniques sur internet qui m'ont permis de trouver de la documentation pour chaque éléments des modules.

# Apparence globale
## Interface
### Barre de Menu
Au niveau de la barre de menu, trois onglets :
  - **Fenêtre** -> Propose des options pour l'interface et l'application;
    - *Paramètres* -> Ouvre la fenêtre des paramètres.
    - *Redémarrer* -> Redémarre l'application.
    - *Quitter* -> Ferme l'application.
  - **Commandes** -> Permet d'effectuer des actions;
    - *Effacer les entrées* -> Efface le temps actuellement entré dans les sélecteurs.
    - *Déporter minuteur* -> Affiche le temps restant dans une nouvelle fenêtre.
  - **Source** -> Donne des informations sur l'application;
    - *Ouvrir GitHub* -> Ouvre directement le dépôt GitHub dans le navigateur.
    - *Afficher GitHub* -> Ouvre une fenêtre affichant le lien vers le dépôt GitHub, avec un bouton permettant de le copier.
    - *Afficher LICENCE* -> Affiche une fenêtre avec la licence du projet (voir le [chapitre LICENCE](#licence))
### Fenêtre
Sur la fenêtre principale, est disponible, dans l'ordre :
- L'heure, en grand, en haut (possibilité de ne plus l'afficher dans les paramètres)
- Un rectangle coloré contenant le nom de l'application, puis le temps restant pendant le décompte.
- Trois boutons (LANCER, PAUSE, ARRÊTER).
- Un bouton pour déporter le temps restant dans une nouvelle fenêtre.
- Deux entrées (minutes/secondes) et un bouton pour les effacer rapidement.
L'application peut être agrandie et mise en plein écran.

**Détails sur la déportation du temps restant** :
Comme indiqué plus haut, sur la fenêtre se trouve un bouton permettant de "déporter le temps restant". Concrètement cela signifie ouvrir
une nouvelle fenêtre avec affiché seulement le temps restant, sur un fond de couleur. Cette fenêtre à l'avantage d'être beaucoup plus
visible que l'affichage de l'application, mais aussi le fait qu'elle reste toujours au premier plan (même si vous cliquez à côté, elle
restera apparente).

## Améliorations et Ajouts
Maintenant qu'il n'y a plus de bugs **dans le code python** d'après les tests fait récemment, voici une petite liste non exhaustive des futurs améliorations.
- Ajout d'un système permettant à l'utilisateur d'enregistrer des temps (par exemple ceux qu'il utilise régulièrement), en
  plus du système initial avec les entrées/`spinbox`. Cela consisterai en un menu déroulant de type `combobox`, qui ne
  s'afficherai que si au moins un temps est déjà enregistré, sinon un bouton pour créer un nouveau temps prédéfini.
  Si un ou plusieurs temps a déjà été enregistré, le sélecteur s'affiche, à côté un bouton pour lancer le temps prédéfini
  sur le minuteur et un autre permettant d'ajouter un nouveau temps à la liste. **Cette amélioration sera l'objectif de la V2**.

- Ajout d'un système d'extension à l'application, comme un générateur de mots de passe sécurisé, un chronomètre, ou un générateur de
  plan de classe aléatoire, par exemple. Les extensions seraient stockées sur un GitHub séparé de celui de l'application, et celle-ci
  viendrai télécharger et intégrer celle que l'utilisateur souhaitera dans un onglets spécifique des paramètres. **Cette amélioration sera l'objectif de la V3**.

- Choix de la sonnerie. Dans les versions à venir de l'application, il sera possible de choisir la sonnerie via un sélecteur dans les
  paramètres, de type `combobox`. Ce sélecteur sera géré dynamiquement via la variable `tkinter` du `checkbutton` permettant d'activer la
  sonnerie. Concrètement, si la sonnerie est désactivé alors le sélecteur sera grisé, inutilisable.

- Si un jour, une fois l'application terminée completement avec toutes les améliorations présentées ci-haut, j'ai envie de perdre mon temps, je passerai probablement sur une version 4 cross-platform, avec wxWidgets (**wxPython**) ou Toga (?). Mais comme cela nécessite de refaire toute l'interface, je ne le ferai probablement pas avant longtemps (j'en profiterai pour changer quelques détails pour rendre l'application plus conviviale).

# Développement
## Installation
Attention, **certains des modules utilisés par le projet ne sont pas inclus par défauts dans python**. Pour les installer, il vous suffit de
lancer la commande suivante (après vous être déplacé dans le répertoire du projet téléchargé - commande '*cd path*' sous Windows et Unix):
```sh
pip install -r requirements.txt
```
Cette commande installera tous les modules listés dans le fichier *requirements.txt*, utilisés par les programmes Python de l'application.

## Fonctionnement
GoTime fonctionne avec la fonction `after` de `tkinter`. L'affichage de l'heure fonctionne de cette manière et le minuteur également.
Cette méthode permet d'appeller une fonction un certain temps plus tard, temps défini en ms. Pour modifier chaque seconde l'heure, par exemple,
on utilise cette commande (l.130)
```py
self.after(1000, self.update_time)  # Met à jour toutes les secondes
```
Cela crée une boucle qui met à jour l'heure toutes les 1000ms, soit 1s. **C'est le même principe qui est utilisé pour le rafraichissement du minuteur.**
Pour ce qui est des paramètres, l'application fonctionne grâce à une lecture/écriture dans un fichier json ([settings.json](dep/settings.json)).
Tout le reste de l'application n'est qu'une question d'apparence et de widgets, la base fonctionne comme ceci.

## Dépendance
Pour fonctionner l'application requiert les modules suivants.
Quelques uns ne sont pas inclus par défaut dans python3, ils sont listés dans le fichier [requirements.txt](requirements.txt).
1. tkinter
2. datetime
3. webbrowser
4. sys
5. subprocess
6. darkdetect
7. PIL (pillow)
8. os
9. json
10. platform
11. getpass
12. socket
13. pygame

## Compilation
Pour compiler et distribuer l'application, j'utilise [`nuitka`](https://github.com/Nuitka/Nuitka), avec cette commande :
```sh
python3 -m nuitka --run --onefile --output-filename="GoTime" --disable-console --follow-imports --enable-plugin=tk-inter --linux-icon="dep/icon.ico" --macos-app-icon="dep/icon.ico" --windows-icon-from-ico="dep/icon.ico" runApp.py
```
**Sous Windows, j'ai eu beaucoup de problème avec un antivirus (Avast) qui supprimait l'exécutable sous prétexte que c'était un cheval de trois. Si vous compilez l'application, je vous conseille de désactiver votre antivirus (je ne souhaitais pas le faire au début mais j'y ai été contraint, c'est la seule solution - même créer des exceptions ne fonctionne pas!).** <span style="color:red">**De plus, comme les pirates informatiques utilisent beaucoup nuitka pour compiler leurs virus, mon application a la même signature qu'un programme malveillant et se fait donc bloquer par les antivirus!**<span>
Pour tenter de corriger ce problème, je vais tenter d'ajouter `--mingw64` lors de la compilation sous windows pour changer de compilateur.
*Si un message d'erreur vous indique que python n'existe pas ou n'est pas reconnu ou autre, essayez de changer `python3` en `python` au début de la commande.*

**TIP** : Installez nuitka avec `pip install nuitka`, puis installez l'utilitaire de compression d'exécutables si il n'est pas installé (`pip install zstandard`), configurez le cache des fichiers `C` (ccache), puis lancez la commande indiquez plus haut.
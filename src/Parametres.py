import tkinter as tk
from tkinter import ttk
from variables import *

class FenetreParametres(tk.Toplevel):
    def __init__(self, callback_theme=None, callback_restart=None):
        super().__init__()
        # ------------------------ Variables
        self.callback_theme = callback_theme # Callback pour rafraichir le thème après modification des paramètres
        self.callback_restart = callback_restart # Callback pour exécuter des actions après modification des paramètres
        self.reboot_app_ou_non = False
        self.sonnerie_en_cours = False
        # ------------------------ Paramétrage de la fenêtre des paramètres
        self.title(f"Paramètres")
        self.geometry("600x400")
        if systeme_exploitation == 'Windows':
            self.iconbitmap(chemin_image_application)
        else: pass
        self.resizable(False, False)
        self.wm_iconbitmap()
        self.logo = tk.PhotoImage(file=chemin_image_application)
        self.iconphoto(False, self.logo)
        # ------------------------ Créer le titre de la page de paramètres
        self.label_titre_parametres = tk.Label(self, text=f"{nom_application} - Paramètres", font=("Arial", 24))
        self.label_titre_parametres.pack(pady=10)
        # ------------------------ Créer les onglets noteboo0k et frame ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.onglets = ttk.Notebook(self)
        self.onglets.focus_set()
        self.onglet_theme = tk.Frame(self.onglets)
        self.onglet_sons = tk.Frame(self.onglets)
        self.onglets.add(child=self.onglet_theme, text="Thème et Apparence")
        self.onglets.add(child=self.onglet_sons, text="Sonnerie")
        self.onglets.pack(fill="x", padx=40, pady=(10, 20))

        # ------------------------------------------------ Onglet apparence et thème
        # ------------------------ Frame pour regrouper les radiobuttons entre eux
        self.frame_selection_theme = tk.Frame(self.onglet_theme, border=0)
        self.frame_selection_theme.pack(pady=20, padx=45, side=tk.LEFT, expand=True)
        # ------------------------ Valeur
        self.parametre_radiobutton_select_theme_value = tk.StringVar(value=parametres_fichier_json["value_theme"])
        self.parametre_checkbutton_select_sounds_on_or_off = tk.BooleanVar(value=parametres_fichier_json["value_sounds"])
        self.parametre_checkbutton_afficher_heure_en_haut = tk.BooleanVar(value=parametres_fichier_json["value_affichage_heure"])
        # ------------------------ RadioButtons
        self.selection_parametre_theme_os_default = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Default", value="DEFAULT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_dark = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Dark", value="DARK", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_light = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Light", value="LIGHT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_default.pack(anchor='w', pady=2)
        self.selection_parametre_theme_os_dark.pack(anchor='w', pady=2)
        self.selection_parametre_theme_os_light.pack(anchor='w', pady=2)
        # ------------------------ checkbutton
        self.checkbutton_afficher_heure_en_haut = tk.Checkbutton(self.onglet_theme, text="Afficher l'heure en haut\n(nécéssite de redémarrer)",
                                                                 variable=self.parametre_checkbutton_afficher_heure_en_haut,
                                                                 onvalue = True, offvalue = False)
        self.checkbutton_afficher_heure_en_haut.pack(side=tk.RIGHT, anchor="w", padx=(0, 45))

        # ------------------------------------------------ Onglet sonnerie
        # ------------------------ Frame pour regrouper les éléments de gauche
        self.frame_selection_sonnerie_et_volume_a_gauche = tk.Frame(self.onglet_sons)
        self.frame_selection_sonnerie_et_volume_a_gauche.pack(pady=20, padx=(45, 20), side=tk.LEFT)
        # ------------------------ Frame pour regrouper les éléments de droite
        self.frame_selection_sonnerie_et_volume_a_droite = tk.Frame(self.onglet_sons)
        self.frame_selection_sonnerie_et_volume_a_droite.pack(pady=20, padx=(20, 45), side=tk.RIGHT)
        # ------------------------ CheckButton sélection sonnerie ou pas
        self.checkbutton_parametre_sons = tk.Checkbutton(self.frame_selection_sonnerie_et_volume_a_gauche, text="Sonnerie/Alarme",
                                                         variable=self.parametre_checkbutton_select_sounds_on_or_off,
                                                         onvalue = True, offvalue = False)
        self.checkbutton_parametre_sons.pack(side='top', padx=(0, 5), pady=2, anchor='w')
        # ------------------------ Bouton pour tester la sonnerie
        self.bouton_tester_la_sonnerie = tk.Button(self.frame_selection_sonnerie_et_volume_a_droite, text="Essayer la sonnerie",
                                                   activebackground=couleur_frame_minuteur_jaune, command=lambda: FenetreEssayerSonnerie())
        self.bouton_tester_la_sonnerie.pack(side='top', padx=(0, 5), pady=2, anchor='w', fill="x")
        # ------------------------ Frame pour regrouper les boutons entre eux
        self.frame_boutons_parametres = tk.Frame(self, width=200, height=400)
        self.frame_boutons_parametres.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Appliquer les paramètres et quitter",
                                                     activebackground=couleur_frame_minuteur_verte, command=self.apply_parametres)
        self.bouton_validation_parametre.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Annuler",
                                                     activebackground=couleur_frame_minuteur_rouge, command=self.destroy)
        self.bouton_validation_parametre.pack(fill="x", padx=20)

    def apply_parametres(self):
        # Gestion du thème clair ou sombre
        self.reboot_app_ou_non = False
        selected_theme = self.parametre_radiobutton_select_theme_value.get()
        if selected_theme != parametres_fichier_json["value_theme"]:
            parametres_fichier_json["value_theme"] = selected_theme
            save_config(parametres_fichier_json)
            if self.callback_theme: self.callback_theme()
        # Gestion de l'activation de la sonnerie
        selected_state_sounds_for_windows = self.parametre_checkbutton_select_sounds_on_or_off.get()
        if selected_state_sounds_for_windows != parametres_fichier_json["value_sounds"]:
            parametres_fichier_json["value_sounds"] = selected_state_sounds_for_windows
            save_config(parametres_fichier_json)
        # Gestion de l'affichage de l'heure en haut de la fenêtre de l'application
        selected_state_affichage_heure_en_haut = self.parametre_checkbutton_afficher_heure_en_haut.get()
        if selected_state_affichage_heure_en_haut != parametres_fichier_json["value_affichage_heure"]:
            parametres_fichier_json["value_affichage_heure"] = selected_state_affichage_heure_en_haut
            save_config(parametres_fichier_json)
            self.reboot_app_ou_non = True
        # Fermer la fenêtre des paramètres
        self.destroy()
        if self.reboot_app_ou_non == True:
            if self.callback_restart: self.callback_restart()
        else: pass

class FenetreEssayerSonnerie(tk.Toplevel):
    def __init__(self):
        super().__init__()
        # ------------------------ Configuration de la fenêtre
        self.title("Essayer la sonnerie")
        # self.geometry("340x100")
        self.resizable(False, False)
        self.wm_iconbitmap()
        self.logo = tk.PhotoImage(file=chemin_image_application)
        self.iconphoto(False, self.logo)
        self.protocol("WM_DELETE_WINDOW", self.fermer_fenetre_essayer_sonnerie_et_arreter_sonnerie)
        # ------------------------ Configuration du style ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ------------------------ Frame pour les boutons
        self.frame_boutons = tk.Frame(self) # si je fais une frame ttk la couleur de fond est grise
        self.frame_boutons.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)
        # ------------------------ Bouton pour jouer la sonnerie
        self.bouton_jouer_sonnerie = ttk.Button(self.frame_boutons, text="Jouer la sonnerie", command=lambda: jouer_sonnerie(True))
        self.bouton_jouer_sonnerie.grid(row=0, column=0, padx=10, pady=10)
        # ------------------------ Bouton pour arrêter la sonnerie
        self.bouton_stopper_sonnerie = ttk.Button(self.frame_boutons, text="Arrêter la sonnerie", command=lambda: jouer_sonnerie(False))
        self.bouton_stopper_sonnerie.grid(row=0, column=1, padx=10, pady=10)

    def fermer_fenetre_essayer_sonnerie_et_arreter_sonnerie(self):
        jouer_sonnerie(False)
        self.destroy()
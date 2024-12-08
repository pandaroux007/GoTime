import tkinter as tk
from tkinter import ttk
# ------------------------ fichiers de l'application
from FenetreSonnerie import FenetreEssayerSonnerie
from InfoApp import *
from Utiles import *
from Parametres import parametres

class FenetreParametres(tk.Toplevel):
    def __init__(self, callback_theme=None):
        super().__init__()
        # ------------------------ Variables
        self.callback_theme = callback_theme # callback pour rafraichir le theme après modif paramètres
        self.reboot_app_ou_non = False
        self.sonnerie_en_cours = False
        # ------------------------ Paramétrage de la fenêtre des paramètres
        self.title(f"Paramètres")
        self.geometry("600x400")
        self.resizable(False, False)
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
        self.parametre_radiobutton_select_theme_value = tk.StringVar(value=parametres.value_theme)
        self.parametre_checkbutton_select_sounds_on_or_off = tk.BooleanVar(value=parametres.value_sounds)
        self.parametre_checkbutton_afficher_heure_en_haut = tk.BooleanVar(value=parametres.value_affichage_heure)
        # ------------------------ RadioButtons
        self.selection_parametre_theme_os_default = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Default", value="DEFAULT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_dark = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Dark", value="DARK", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_light = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Light", value="LIGHT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_default.pack(anchor='w', pady=2)
        self.selection_parametre_theme_os_dark.pack(anchor='w', pady=2)
        self.selection_parametre_theme_os_light.pack(anchor='w', pady=2)
        # ------------------------ checkbutton
        self.checkbutton_afficher_heure_en_haut = tk.Checkbutton(self.onglet_theme, text="Afficher l'heure en haut\n(nécessite de redémarrer)",
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
                                                   activebackground=couleurs.frame_jaune, command=lambda: FenetreEssayerSonnerie())
        self.bouton_tester_la_sonnerie.pack(side='top', padx=(0, 5), pady=2, anchor='w', fill="x")
        # ------------------------ Frame pour regrouper les boutons entre eux
        self.frame_boutons_parametres = tk.Frame(self, width=200, height=400)
        self.frame_boutons_parametres.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Appliquer les paramètres et quitter",
                                                     activebackground=couleurs.frame_verte, command=self.apply_parametres)
        self.bouton_validation_parametre.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Annuler",
                                                     activebackground=couleurs.frame_rouge, command=self.destroy)
        self.bouton_validation_parametre.pack(fill="x", padx=20)

    def apply_parametres(self):
        parametres_changes = False
        # Gestion du thème clair ou sombre
        selected_theme = self.parametre_radiobutton_select_theme_value.get()
        if selected_theme != parametres.value_theme:
            parametres.value_theme = selected_theme
            if self.callback_theme: self.callback_theme()
            parametres_changes = True
        # Gestion de l'activation de la sonnerie
        selected_state_sounds_for_windows = self.parametre_checkbutton_select_sounds_on_or_off.get()
        if selected_state_sounds_for_windows != parametres.value_sounds:
            parametres.value_sounds = selected_state_sounds_for_windows
            parametres_changes = True
        # Gestion de l'affichage de l'heure en haut de la fenêtre de l'application
        selected_state_affichage_heure_en_haut = self.parametre_checkbutton_afficher_heure_en_haut.get()
        if selected_state_affichage_heure_en_haut != parametres.value_affichage_heure:
            parametres.value_affichage_heure = selected_state_affichage_heure_en_haut
            parametres_changes = True
        # Fermer la fenêtre des paramètres
        self.destroy()
        # Si un ou plusieurs parametres ont changés, on enregistre
        if parametres_changes is not False: parametres.sauvegarde()
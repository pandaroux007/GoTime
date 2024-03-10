import tkinter as tk
from datetime import datetime
import webbrowser
from tkinter import messagebox
import darkdetect
from sys import exit
# ------------------------ fichier de l'application
from variables import *
from FenetreLicence import FenetreLicence

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Variables pour les paramètre du minuteur
        self.paused = False
        self.time_remaining = None
        self.valeur_state_bouton_start = None
        # ------------------------ Paramètrage de la fenêtre.
        self.title(f"{nom_application} V{version_application}")
        self.geometry("1080x720")
        self.minsize(1000, 680)
        self.config(background=theme_sombre)
        if systeme_exploitation == 'Windows':
            self.iconbitmap(chemin_image_application)
        else: pass
        # ------------------------ Barre de menu
        barre_de_menu = tk.Menu(self)
        # ------------------------ Création d'un menu 'Fenêtre'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="Paramètres", command=self.open_parametres)
        fenetre_menu.add_command(label="Quitter", command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ Création d'un second menu 'Commandes'
        commandes_menu = tk.Menu(barre_de_menu, tearoff=0)
        commandes_menu.add_command(label="Clear entry", command=self.clear_entrees)
        commandes_menu.add_command(label="Déporter timer", command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        barre_de_menu.add_cascade(label="Commandes", menu=commandes_menu)
        # ------------------------ Création d'un troisième menu 'Source'
        source_menu = tk.Menu(barre_de_menu, tearoff=0)
        source_menu.add_command(label="Open GitHub", command=self.open_github)
        source_menu.add_command(label="Show source", command=self.show_github)
        source_menu.add_command(label="Show LICENCE", command=lambda action: FenetreLicence())
        barre_de_menu.add_cascade(label="Source", menu=source_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        if parametres_fichier_json["value_affichage_heure"] == True:
            self.time_label = tk.Label(self, text="", font=("Arial", 24))
            self.time_label.pack(pady=20)
        # ------------------------ Création de la frame principale :
        self.frame_principale = tk.Frame(self, width=900)
        self.frame_principale.pack(padx=20, pady=(0, 20))
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self.frame_principale, bg=couleur_frame_minuteur_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.temps_restant_label = tk.Label(self.time_frame, text=f"{nom_application}", font=("Arial", 24),
                                            bg=couleur_frame_minuteur_verte, fg="black")
        self.temps_restant_label.pack(pady=20)
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self.frame_principale, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="START",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="normal", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.start_timer)
        self.valeur_state_bouton_start = False
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE",
                                      activebackground=couleur_frame_minuteur_jaune,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.pause_timer)
        self.bouton_stop = tk.Button(self.boutons_frame, text="STOP",
                                     activebackground=couleur_frame_minuteur_rouge,
                                     state="disabled", width=30, height=2,
                                     justify="center", relief="groove",
                                     command=self.stop_timer)
        self.bouton_start.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_pause.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_stop.pack(side="left", padx=10, pady=10, expand=True)
        # ------------------------ Entrées pour la gestion du temps du minuteur (minutes et secondes)
        self.entrees_frame = tk.Frame(self.frame_principale)
        self.entrees_frame.pack(padx=20, pady=(0, 20))
        # ------------ Entrée des minutes :
        self.minutes_entry = tk.Spinbox(self.entrees_frame, width=40, from_=0, to=180)
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.minutes_entry.pack(side="left", padx=(10, 10), expand=True)
        # ------------ Entrée des secondes :
        self.seconds_entry = tk.Spinbox(self.entrees_frame, width=40, from_=0, to=10800)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.seconds_entry.pack(side="left", padx=(10, 20), expand=True)
        self.clear_entrees()
        # ------------ Bouton pour effacer les entrées
        self.bouton_clear_entrees = tk.Button(self.entrees_frame, text="Effacer les entrées",
                                              activebackground=couleur_frame_minuteur_rouge,
                                              width=15,command=self.clear_entrees)
        self.bouton_clear_entrees.pack(side="left", padx=10, pady=20, expand=True)
        # ------------ Bouton pour déporter le temps restant dans une nouvelle fenêtre
        self.bouton_deporter_temps_restant = tk.Button(self.frame_principale, width=105,
                                                       text="Déporter le temps restant dans une nouvelle fenêtre",
                                                       activebackground=couleur_frame_minuteur_verte,
                                                       command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        self.bouton_deporter_temps_restant.pack(expand=True)
        # ------------------------ Mise à jour de l'heure, gestion du thème et activation de la gestion des entrées
        self.update_time()
        self.gestion_theme_par_defaut()

    def update_time(self):
        if hasattr(self, 'time_label'):
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
            self.after(1000, self.update_time)  # Met à jour toutes les secondes
        else: pass

    def start_timer(self):
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())
        self.total_seconds = minutes * 60 + seconds
        self.time_remaining = self.total_seconds
        if self.time_remaining >= temps_max:
            messagebox.showwarning("Avertissement", f"""\
Le temps total de seconde du minuteur ne peut pas dépasser {int(temps_max / 60)} min !\n\
Merci d'entrer une durée inférieure !""")
        elif self.time_remaining == 0:
            messagebox.showwarning(f"Avertissement", "Merci d'entrer une durée avant de lancer le minuteur")
        else:
            self.minutes_entry.config(state="disabled")
            self.seconds_entry.config(state="disabled")
            self.bouton_start.config(state="disabled")
            self.valeur_state_bouton_start = False
            self.bouton_clear_entrees.config(state="disabled")
            self.bouton_pause.config(state="normal")
            self.bouton_stop.config(state="normal")
            self.update_timer()

    def update_timer(self):
        if self.time_remaining > 0 and not self.paused:
            self.time_remaining -= 1
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.temps_restant_label.config(text=time_str, font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
            if hasattr(self, 'fenetre_deportee'):
                self.temps_restant_label_fenetre_deporte.config(text=time_str, font=("Arial", 35), bg=couleur_frame_minuteur_verte, fg="black")
            else: pass
            # Calcul des pourcentages
            total_time = self.total_seconds
            time_left = self.time_remaining
            percent_remaining = time_left / total_time
            # Changement de couleur en fonction du pourcentage restant
            if percent_remaining <= 0.2:
                self.time_frame.config(bg=couleur_frame_minuteur_rouge)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_rouge)
                if hasattr(self, 'fenetre_deportee'):
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_rouge)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_rouge)
                else: pass
            elif percent_remaining <= 0.3:
                self.time_frame.config(bg=couleur_frame_minuteur_jaune)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_jaune)
                if hasattr(self, 'fenetre_deportee'):
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_jaune)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_jaune)
                else: pass
            else:
                self.time_frame.config(bg=couleur_frame_minuteur_verte)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_verte)
                if hasattr(self, 'fenetre_deportee'):
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_verte)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_verte)
                else: pass
            self.after(1000, self.update_timer)
        elif self.paused:
            pass  # Passe le minuteur sans décrémenter le temps
        else:
            self.stop_timer(True)

    def pause_timer(self):
        if not hasattr(self, 'paused'):
            self.paused = False
        else:
            self.paused = not self.paused
            if self.paused:
                self.bouton_pause.config(text="REPRENDRE")
            else:
                self.bouton_pause.config(text="PAUSE")
                self.update_timer()

    def stop_timer(self, parametre_appel_bouton_ou_non = None):
        self.paused = False
        self.bouton_pause.config(text="PAUSE")
        self.time_remaining = 0  # Réinitialiser le temps restant
        self.bouton_start.config(state="normal")
        self.valeur_state_bouton_start = True
        self.bouton_pause.config(state="disabled")
        self.bouton_stop.config(state="disabled")
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
        self.bouton_clear_entrees.config(state="normal")
        self.time_frame.config(bg=couleur_frame_minuteur_verte)
        self.temps_restant_label.config(text=f"{nom_application}", font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
        if hasattr(self, 'fenetre_deportee'):
            self.fenetre_deportee.config(background=couleur_frame_minuteur_verte)
            self.temps_restant_label_fenetre_deporte.config(text="Temps restant", font=("Arial", 35), bg=couleur_frame_minuteur_verte, fg="black")
        # ------------------------ Gestion du son sur windows :
        if systeme_exploitation == "Windows" and parametres_fichier_json["value_sounds"] == True:
            try: import winsound
            except ImportError: pass
            winsound.Beep(1000, 500)
        else: pass
        if parametre_appel_bouton_ou_non == None:
            self.update_timer()  # Arrêter la récursion de la fonction update_timer()
        else: pass

    def gestion_theme_par_defaut(self):
        if parametres_fichier_json["value_theme"] == "DEFAULT":
            if darkdetect.theme() == 'Dark':
                self.mettre_app_en_mode_dark()
            elif darkdetect.theme() == 'Light':
                self.mettre_app_en_mode_light()
        elif parametres_fichier_json["value_theme"] == "LIGHT":
            self.mettre_app_en_mode_light()
        elif parametres_fichier_json["value_theme"] == "DARK":
            self.mettre_app_en_mode_dark()
        else:
            messagebox.showerror(f"Erreur", "La sélection automatique du thème de l'application a échoué... L'application va automatiquement se lancer en mode sombre.")
            self.mettre_app_en_mode_dark()

    def mettre_app_en_mode_dark(self):
        self.config(bg=theme_sombre)
        if hasattr(self, 'time_label'): self.time_label.config(bg=theme_sombre, fg="white")
        self.time_frame.config()
        self.frame_principale.config(bg=theme_sombre)
        self.boutons_frame.config(bg=theme_sombre)
        self.bouton_start.config(bg=theme_sombre, fg="white")
        self.bouton_pause.config(bg=theme_sombre, fg="white")
        self.bouton_stop.config(bg=theme_sombre, fg="white")
        self.bouton_clear_entrees.config(bg=theme_sombre, fg="white")
        self.entrees_frame.config(bg=theme_sombre)
        self.bouton_deporter_temps_restant.config(bg=theme_sombre, fg="white")

    def mettre_app_en_mode_light(self):
        self.config(bg="white")
        if hasattr(self, 'time_label'): self.time_label.config(bg="white", fg="black")
        self.time_frame.config()
        self.frame_principale.config(bg="white")
        self.boutons_frame.config(bg="white")
        self.bouton_start.config(bg="lightblue", fg="black")
        self.bouton_pause.config(bg="lightblue", fg="black")
        self.bouton_stop.config(bg="lightblue", fg="black")
        self.bouton_clear_entrees.config(bg="lightblue", fg="black")
        self.entrees_frame.config(bg="white")
        self.bouton_deporter_temps_restant.config(bg="lightblue", fg="black")

    def open_parametres(self):
        self.fenetre_parametres = tk.Toplevel()
        self.fenetre_parametres.title(f"Paramètres")
        self.fenetre_parametres.geometry("600x400")
        self.fenetre_parametres.resizable(False, False)
        # ------------------------ Créer le titre de la page de paramètres
        self.label_titre_parametres = tk.Label(self.fenetre_parametres, text=f"{nom_application} - Paramètres", font=("Arial", 24))
        self.label_titre_parametres.pack(pady=10)
        # ------------------------ Frame pour regrouper tous les paramètres entre eux
        self.frame_parametres = tk.Frame(self.fenetre_parametres)
        self.frame_parametres.pack(pady=20)
        # ------------------------ Frame pour regrouper les radiobuttons entre eux
        self.frame_selection_theme = tk.Frame(self.frame_parametres)
        self.frame_selection_theme.pack(pady=20, padx=50, side="left")
        # ------------------------ Valeur
        self.parametre_radiobutton_select_theme_value = tk.StringVar()
        self.parametre_radiobutton_select_theme_value.set(parametres_fichier_json["value_theme"])
        # ------------------------ RadioButtons
        self.selection_parametre_theme_os_default = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Default", value="DEFAULT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_dark = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Dark", value="DARK", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_light = tk.Radiobutton(self.frame_selection_theme, text=f"{nom_application} mode Light", value="LIGHT", variable=self.parametre_radiobutton_select_theme_value)
        self.selection_parametre_theme_os_default.pack(anchor='w')
        self.selection_parametre_theme_os_dark.pack(anchor='w')
        self.selection_parametre_theme_os_light.pack(anchor='w')
        # ------------------------ Frame pour regrouper les checkbuttons entre eux
        self.frame_checkbuttons_parametres = tk.LabelFrame(self.frame_parametres, text="(nécessite de redémarrer)", fg="black")
        self.frame_checkbuttons_parametres.pack(pady=20, padx=45, side="right")
        # ------------------------ Valeurs
        self.parametre_checkbutton_select_sounds_on_or_off = tk.BooleanVar(value=parametres_fichier_json["value_sounds"])
        self.parametre_checkbutton_afficher_heure_en_haut = tk.BooleanVar(value=parametres_fichier_json["value_affichage_heure"])
        # ------------------------ CheckButtons
        self.checkbutton_parametre_sons = tk.Checkbutton(self.frame_checkbuttons_parametres, text="Sons (Windows seulement)",
                                                         variable=self.parametre_checkbutton_select_sounds_on_or_off,
                                                         onvalue = True, offvalue = False)
        self.checkbutton_afficher_heure_en_haut = tk.Checkbutton(self.frame_checkbuttons_parametres, text="Afficher l'heure en haut",
                                                                 variable=self.parametre_checkbutton_afficher_heure_en_haut,
                                                                 onvalue = True, offvalue = False)
        self.checkbutton_parametre_sons.pack(pady=5, padx=5)
        self.checkbutton_afficher_heure_en_haut.pack(padx=5)
        if systeme_exploitation == "Windows":
            self.checkbutton_parametre_sons.config(state="normal")
        else: self.checkbutton_parametre_sons.config(state="disabled")
        # ------------------------ Frame pour regrouper les boutons entre eux
        self.frame_boutons_parametres = tk.Frame(self.fenetre_parametres, width=200, height=400)
        self.frame_boutons_parametres.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Appliquer les paramètres et quitter", activebackground=couleur_frame_minuteur_verte, command=self.apply_parametres)
        self.bouton_validation_parametre.pack(fill="x", padx=20)
        self.bouton_validation_parametre = tk.Button(self.frame_boutons_parametres, text="Annuler", activebackground=couleur_frame_minuteur_rouge, command=self.fenetre_parametres.destroy)
        self.bouton_validation_parametre.pack(fill="x", padx=20)

    def apply_parametres(self):
        # Gestion du thème depuis les paramètres
        selected_theme = self.parametre_radiobutton_select_theme_value.get()
        if selected_theme != parametres_fichier_json["value_theme"]:
            parametres_fichier_json["value_theme"] = selected_theme
            save_config(parametres_fichier_json)
            self.gestion_theme_par_defaut()  # Met à jour le thème en temps réel
        # Gestion du son depuis les paramètres
        if systeme_exploitation == "Windows":
            selected_state_sounds_for_windows = self.parametre_checkbutton_select_sounds_on_or_off.get()
            if selected_state_sounds_for_windows != parametres_fichier_json["value_sounds"]:
                parametres_fichier_json["value_sounds"] = selected_state_sounds_for_windows
                save_config(parametres_fichier_json)
        # Gestion de l'affichage de l'heure en haut de la fenêtre de l'application
        selected_state_affichage_heure_en_haut = self.parametre_checkbutton_afficher_heure_en_haut.get()
        if selected_state_affichage_heure_en_haut != parametres_fichier_json["value_affichage_heure"]:
            parametres_fichier_json["value_affichage_heure"] = selected_state_affichage_heure_en_haut
            save_config(parametres_fichier_json)
        # Fermer la fenêtre des paramètres
        self.fenetre_parametres.destroy()

    def deporter_frame_temps_restant_dans_une_nouvelle_fenetre(self):
        self.fenetre_deportee = tk.Toplevel(self, background=couleur_frame_minuteur_verte)
        self.fenetre_deportee.geometry("600x400")
        self.fenetre_deportee.minsize(300, 200)
        self.fenetre_deportee.title(f"Temps restant - {nom_application}")
        self.fenetre_deportee.protocol("WM_DELETE_WINDOW", self.fermer_fenetre_temps_restant_deporte)
        self.fenetre_deportee.wm_attributes("-topmost", 1)
        self.bouton_deporter_temps_restant.config(text="Fermer la fenêtre affichant le temps restant", activebackground=couleur_frame_minuteur_rouge, command=self.fermer_fenetre_temps_restant_deporte)
        # ------------------------ Afficher le temps restant au centre
        self.temps_restant_label_fenetre_deporte = tk.Label(self.fenetre_deportee, text="Temps restant", font=("Arial", 35), bg=couleur_frame_minuteur_verte, fg="black")
        self.temps_restant_label_fenetre_deporte.pack(expand=True)

    def fermer_fenetre_temps_restant_deporte(self):
        self.bouton_deporter_temps_restant.config(text="Déporter le temps restant dans une nouvelle fenêtre", activebackground=couleur_frame_minuteur_verte, command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        self.fenetre_deportee.destroy()

    def show_github(self): messagebox.showinfo(f"Source {nom_application}", f"Lien du GitHub du projet :\n{lien_du_github}")
    def open_github(self): webbrowser.open_new(lien_du_github)

    def clear_entrees(self):
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.insert(0, "0")

if __name__ == "__main__":
    try:
        root = Application()
        root.mainloop()
    except Exception as e:
        messagebox.showerror(title=f"Erreur", message=f"Hmm...something seems to have gone wrong.\nError is : {e}")
        exit()
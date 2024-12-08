import tkinter as tk # pour la création et la manipulation de la fenêtre
from datetime import datetime # pour la gestion du temps et du minuteur
import webbrowser # pour l'ouverture du navigateur avec le lien du github de l'application
from tkinter import messagebox # pour les erreur et les validations
import darkdetect # pour la détection du thème de l'OS
from PIL import ImageTk, Image
# ------------------------ fichiers de l'application
from FenetreLicence import FenetreLicence
from FenetreParametres import FenetreParametres
from FenetreInfo import FenetreInfo
from InfoApp import *
from Utiles import *
from Parametres import parametres
from CheminsFichiers import *
from SystemeVerifUpdate import SystemeVerifUpdate

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Variables
        self.theme_interne = None
        self.paused = False # pour le bouton pause
        self.time_remaining = None # pour le temps restant
        self.pause_verrouillage = False # pour éviter les bugs du minuteur après des doubles cliques sur le bp pause
        # ------------------------ Paramètrage de la fenêtre.
        self.title(f"{nom_application} v{version_application}")
        # self.geometry("1080x720")
        self.width = int(self.winfo_screenwidth()/2.5)
        self.height = int(self.winfo_screenheight()/1.5)
        self.geometry(f"{self.width}x{self.height}")
        self.minsize(1000, 680)
        self.logo = tk.PhotoImage(file=chemin_image_application)
        self.iconphoto(True, self.logo)
        self.call('wm', 'iconphoto', self._w, self.logo)
        self.bind("<1>", lambda event: event.widget.focus_set())
        # ------------------------ Barre de menu
        barre_de_menu = tk.Menu(self, relief="solid", borderwidth=0, background="grey", foreground="white")
        # ------------------------ Création d'un menu 'Fenêtre'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=False, relief="solid", borderwidth=0, background="grey", foreground="white")
        fenetre_menu.add_command(label="Paramètres", underline=0, command=lambda: FenetreParametres(callback_theme=self.gestion_theme_par_defaut))
        fenetre_menu.add_command(label="Quitter", underline=0, command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ Création d'un second menu 'Commandes'
        commandes_menu = tk.Menu(barre_de_menu, tearoff=False, relief="solid", borderwidth=0, background="grey", foreground="white")
        commandes_menu.add_command(label="Effacer les entrées", underline=0, command=self.clear_entrees)
        commandes_menu.add_command(label="Déporter minuteur", underline=0, command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        barre_de_menu.add_cascade(label="Commandes", menu=commandes_menu)
        # ------------------------ Création d'un troisième menu 'Source'
        source_menu = tk.Menu(barre_de_menu, tearoff=False, relief="solid", borderwidth=0, background="grey", foreground="white")
        source_menu.add_command(label="Afficher LICENCE", underline=0, command=lambda: FenetreLicence())
        source_menu.add_command(label="Signaler un bug", underline=0, command=lambda: webbrowser.open_new_tab(lien_du_github + "/issues"))
        source_menu.add_command(label="À propos", underline=2, command=lambda: FenetreInfo())
        barre_de_menu.add_cascade(label="Source", menu=source_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        if parametres.value_affichage_heure == True:
            self.time_label = tk.Label(self, text="", font=("Arial", 24))
            self.time_label.pack(pady=20)
        else:
            self.espace_vide = tk.Label(self, text="", height=1)
            self.espace_vide.pack()
        # ------------------------ Création de la frame principale :
        self.frame_principale = tk.Frame(self, width=900)
        self.frame_principale.pack(padx=20, pady=(0, 20))
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self.frame_principale, bg=couleurs.frame_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        if parametres.value_affichage_heure == True:
            self.time_frame.config(pady=10)
        self.temps_restant_label = tk.Label(self.time_frame, text=f"{nom_application}", font=("Arial", 24),
                                            bg=couleurs.frame_verte, fg=couleurs.sombre)
        self.temps_restant_label.pack(pady=20)
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self.frame_principale, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="LANCER",
                                      activebackground=couleurs.frame_verte,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.start_timer)
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE",
                                      activebackground=couleurs.frame_jaune,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.pause_timer)
        self.bouton_stop = tk.Button(self.boutons_frame, text="ARRÊTER",
                                     activebackground=couleurs.frame_rouge,
                                     state="disabled", width=30, height=2,
                                     justify="center", relief="groove",
                                     command=self.stop_timer)
        self.bouton_start.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_pause.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_stop.pack(side="left", padx=10, pady=10, expand=True)
        # ------------ Bouton pour déporter le temps restant dans une nouvelle fenêtre
        self.bouton_deporter_temps_restant = tk.Button(self.frame_principale, width=105,
                                                       text="Déporter le temps restant dans une nouvelle fenêtre",
                                                       activebackground=couleurs.frame_verte,
                                                       command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        self.bouton_deporter_temps_restant.pack(expand=True, pady=(5, 20))
        # ------------------------ Entrées pour la gestion du temps du minuteur (minutes et secondes)
        self.entrees_frame = tk.Frame(self.frame_principale)
        self.entrees_frame.pack(padx=20)
        # ------------------------ Variables dynamiques
        self.variable_entree_minutes = tk.StringVar(self)
        self.variable_entree_minutes.trace_add("write", self.gestion_etat_bouton_start_en_fonction_du_temps_entre)
        self.variable_entree_secondes = tk.StringVar(self)
        self.variable_entree_secondes.trace_add("write", self.gestion_etat_bouton_start_en_fonction_du_temps_entre)
        # ------------------------ Ajouter un titre à cette section
        self.titre_section_temps_entry = tk.Label(self.entrees_frame, text="Entrez un temps ici :", font=("Arial", 20), background=couleurs.clair)
        self.titre_section_temps_entry.pack(pady=10)
        # ------------ Entrée des minutes :
        self.labelframe_entree_minutes = tk.LabelFrame(self.entrees_frame, text="min", border=0, labelanchor="e")
        self.labelframe_entree_minutes.pack(side="left", padx=(10, 10))
        self.minutes_entry = tk.Spinbox(self.labelframe_entree_minutes, width=37, from_=0, to=60, textvariable=self.variable_entree_minutes)
        self.minutes_entry.configure(validate="key", validatecommand=(self.minutes_entry.register(self.validate_numeric_input), "%P"))
        self.minutes_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.minutes_entry.pack(padx=(0, 5), expand=True)
        # ------------ Entrée des secondes :
        self.labelframe_entree_secondes = tk.LabelFrame(self.entrees_frame, text="s", border=0, labelanchor="e")
        self.labelframe_entree_secondes.pack(side="left", padx=(10, 20))
        self.seconds_entry = tk.Spinbox(self.labelframe_entree_secondes, width=38, from_=0, to=10800, textvariable=self.variable_entree_secondes)
        self.seconds_entry.configure(validate="key", validatecommand=(self.seconds_entry.register(self.validate_numeric_input), "%P"))
        self.seconds_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.seconds_entry.pack(padx=(0, 5), expand=True)
        self.clear_entrees()
        # ------------ Bouton pour effacer les entrées
        self.bouton_clear_entrees = tk.Button(self.entrees_frame, text="Effacer les entrées",
                                              activebackground=couleurs.frame_rouge,
                                              width=15,command=self.clear_entrees)
        self.bouton_clear_entrees.pack(side="right", padx=10, pady=20, expand=True)
        # ------------------------ Mise à jour de l'heure et gestion du thème
        self.update_time()
        self.gestion_theme_par_defaut()
        # ------------------------ lancement verif MàJ
        self.systeme_verif_update = SystemeVerifUpdate()
        self.systeme_verif_update.lancerVerifUpdate()

    def update_time(self):
        if hasattr(self, 'time_label'):
            current_time = datetime.now().strftime("%H:%M:%S")
            self.time_label.config(text=current_time)
            self.after(1000, self.update_time)  # Met à jour toutes les secondes
        else: pass

    def start_timer(self):
        self.deselectionner_les_entry()
        # ------------------------ Récupération de la valeur du minuteur en secondes
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())
        self.total_seconds = minutes * 60 + seconds
        self.time_remaining = self.total_seconds
        # ------------------------ Configuration de l'état des boutons et entrées
        self.minutes_entry.config(state="disabled")
        self.seconds_entry.config(state="disabled")
        self.bouton_start.config(state="disabled")
        self.bouton_clear_entrees.config(state="disabled")
        self.bouton_pause.config(state="normal")
        self.bouton_stop.config(state="normal")
        # ------------------------ Lancement de la fonction de renouvellement du timer
        self.update_timer()

    def update_timer(self):
        if self.time_remaining > 0 and not self.paused:
            self.time_remaining -= 1
            minutes = self.time_remaining // 60
            seconds = self.time_remaining % 60
            time_str = f"{minutes:02d}:{seconds:02d}"
            self.temps_restant_label.config(text=time_str, font=("Arial", 24), bg=couleurs.frame_verte, fg=couleurs.sombre)
            if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                self.temps_restant_label_fenetre_deporte.config(text=time_str, font=("Arial", 35), bg=couleurs.frame_verte, fg=couleurs.sombre)
            else: pass
            # Calcul des pourcentages
            total_time = self.total_seconds
            time_left = self.time_remaining
            percent_remaining = time_left / total_time
            # Changement de couleur en fonction du pourcentage restant
            if percent_remaining <= 0.2:
                self.time_frame.config(bg=couleurs.frame_rouge)
                self.temps_restant_label.config(bg=couleurs.frame_rouge)
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleurs.frame_rouge)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleurs.frame_rouge)
                else: pass
            elif percent_remaining <= 0.3:
                self.time_frame.config(bg=couleurs.frame_jaune)
                self.temps_restant_label.config(bg=couleurs.frame_jaune)
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleurs.frame_jaune)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleurs.frame_jaune)
                else: pass
            else:
                self.time_frame.config(bg=couleurs.frame_verte)
                self.temps_restant_label.config(bg=couleurs.frame_verte)
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleurs.frame_verte)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleurs.frame_verte)
                else: pass
            self.after(1000, self.update_timer)
        elif self.paused:
            pass  # Passe le minuteur sans décrémenter le temps
        else:
            self.stop_timer(True)

    def pause_timer(self):
        self.deselectionner_les_entry()
        if self.pause_verrouillage: return # si la fonction est verrouillée, on ne rentre pas dedans !
        self.pause_verrouillage = True # Verrouillez la fonction pour empêcher d'autres exécutions simultanées
        if not hasattr(self, 'paused'):
            self.paused = False
        else:
            self.paused = not self.paused
            if self.paused:
                self.bouton_pause.config(text="REPRENDRE")
            else:
                self.bouton_pause.config(text="PAUSE")
                self.update_timer()
        # Déverrouillez la fonction une fois terminée
        self.after(1000, lambda: setattr(self, 'pause_verrouillage', False))

    def stop_timer(self, parametre_appel_bouton_ou_non = None):
        self.deselectionner_les_entry()
        self.paused = False
        self.bouton_pause.config(text="PAUSE")
        self.time_remaining = 0  # réinitialiser le temps restant
        # ------------------------ Configuration de l'état des entrées et des boutons
        self.bouton_start.config(state="normal")
        self.bouton_pause.config(state="disabled")
        self.bouton_stop.config(state="disabled")
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
        self.bouton_clear_entrees.config(state="normal")
        # ------------------------ Gestion affichage temps restant à effacer
        self.time_frame.config(bg=couleurs.frame_verte)
        self.temps_restant_label.config(text=f"{nom_application}", font=("Arial", 24), bg=couleurs.frame_verte, fg=couleurs.sombre)
        if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
            self.fenetre_deportee.config(background=couleurs.frame_verte)
            self.temps_restant_label_fenetre_deporte.config(text="Temps restant", font=("Arial", 35), bg=couleurs.frame_verte, fg=couleurs.sombre)
        # ------------------------ Gestion du son :
        if parametres.value_sounds == True:
            jouer_sonnerie(True) # jouer la sonnerie à la fin du timer
        else: pass
        if parametre_appel_bouton_ou_non == None:
            self.update_timer() # Arreter la récursion de la fonction update_timer()
        else: pass

    def gestion_theme_par_defaut(self):
        if parametres.value_theme == "DEFAULT":
            if darkdetect.theme() == 'Dark':
                self.mettre_app_en_mode_dark()
                self.theme_interne = "DARK"
            elif darkdetect.theme() == 'Light':
                self.mettre_app_en_mode_light()
                self.theme_interne = "LIGHT"
        elif parametres.value_theme == "LIGHT":
            self.mettre_app_en_mode_light()
        elif parametres.value_theme == "DARK":
            self.mettre_app_en_mode_dark()
        else:
            messagebox.showwarning(f"Erreur", "La sélection automatique du thème de l'application a échoué... L'application va automatiquement se lancer en mode sombre.")
            self.mettre_app_en_mode_dark()
            self.theme_interne = "DARK"

    def mettre_app_en_mode_dark(self):
        self.config(bg=couleurs.sombre)
        if hasattr(self, 'time_label'): self.time_label.config(bg=couleurs.sombre, fg=couleurs.clair)
        if hasattr(self, 'espace_vide'): self.espace_vide.config(bg=couleurs.sombre)
        self.time_frame.config()
        self.frame_principale.config(bg=couleurs.sombre)
        self.boutons_frame.config(bg=couleurs.sombre)
        self.bouton_start.config(bg=couleurs.sombre, fg=couleurs.clair)
        self.bouton_pause.config(bg=couleurs.sombre, fg=couleurs.clair)
        self.bouton_stop.config(bg=couleurs.sombre, fg=couleurs.clair)
        self.bouton_clear_entrees.config(bg=couleurs.sombre, fg=couleurs.clair)
        self.entrees_frame.config(bg=couleurs.sombre)
        self.labelframe_entree_minutes.config(background=couleurs.sombre, fg=couleurs.clair)
        self.labelframe_entree_secondes.config(background=couleurs.sombre, fg=couleurs.clair)
        self.bouton_deporter_temps_restant.config(bg=couleurs.sombre, fg=couleurs.clair)
        self.titre_section_temps_entry.config(bg=couleurs.sombre, fg=couleurs.clair)

    def mettre_app_en_mode_light(self):
        self.config(bg=couleurs.clair)
        if hasattr(self, 'time_label'): self.time_label.config(bg=couleurs.clair, fg=couleurs.sombre)
        if hasattr(self, 'espace_vide'): self.espace_vide.config(bg=couleurs.clair)
        self.time_frame.config()
        self.frame_principale.config(bg=couleurs.clair)
        self.boutons_frame.config(bg=couleurs.clair)
        self.bouton_start.config(bg="lightblue", fg=couleurs.sombre)
        self.bouton_pause.config(bg="lightblue", fg=couleurs.sombre)
        self.bouton_stop.config(bg="lightblue", fg=couleurs.sombre)
        self.bouton_clear_entrees.config(bg="lightblue", fg=couleurs.sombre)
        self.entrees_frame.config(bg=couleurs.clair)
        self.labelframe_entree_minutes.config(background=couleurs.clair, fg=couleurs.sombre)
        self.labelframe_entree_secondes.config(background=couleurs.clair, fg=couleurs.sombre)
        self.bouton_deporter_temps_restant.config(bg="lightblue", fg=couleurs.sombre)
        self.titre_section_temps_entry.config(bg=couleurs.clair, fg=couleurs.sombre)

    def deporter_frame_temps_restant_dans_une_nouvelle_fenetre(self):
        self.fenetre_deportee = tk.Toplevel(self, background=couleurs.frame_verte)
        self.fenetre_deportee.geometry("600x400")
        self.fenetre_deportee.minsize(300, 200)
        self.fenetre_deportee.title(f"Temps restant - {nom_application}")
        self.fenetre_deportee.protocol("WM_DELETE_WINDOW", self.fermer_fenetre_temps_restant_deporte)
        self.fenetre_deportee.wm_attributes("-topmost", 1)
        self.bouton_deporter_temps_restant.config(text="Fermer la fenêtre affichant le temps restant", activebackground=couleurs.frame_rouge, command=self.fermer_fenetre_temps_restant_deporte)
        # ------------------------ Afficher le temps restant au centre
        self.temps_restant_label_fenetre_deporte = tk.Label(self.fenetre_deportee, text="Temps restant", font=("Arial", 35), bg=couleurs.frame_verte, fg=couleurs.sombre)
        self.temps_restant_label_fenetre_deporte.pack(expand=True)

    def fermer_fenetre_temps_restant_deporte(self):
        self.bouton_deporter_temps_restant.config(text="Déporter le temps restant dans une nouvelle fenêtre", activebackground=couleurs.frame_verte, command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        self.fenetre_deportee.destroy()
        self.focus_set()

    def deselectionner_les_entry(self): self.focus_set()
    def clear_entrees(self):
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.insert(0, "0")
        self.deselectionner_les_entry()

    def validate_numeric_input(self, text):
        return text.isdigit() or text == ""
    
    def gestion_etat_bouton_start_en_fonction_du_temps_entre(self, *args):
        minutes_str = self.variable_entree_minutes.get()
        seconds_str = self.variable_entree_secondes.get()
        # ------------------------ convertir le contenu des spinbox en entier
        if minutes_str and seconds_str:
            minutes = int(minutes_str)
            seconds = int(seconds_str)
        else: minutes = 0; seconds = 0
        total_secondes = minutes * 60 + seconds
        # ------------------------ gestion état bouton "Start" en fonction du total des secondes
        if total_secondes >= 5 and total_secondes <= temps_max:
            self.bouton_start.config(state="normal")
        else: self.bouton_start.config(state="disabled")
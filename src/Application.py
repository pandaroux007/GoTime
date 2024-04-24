import tkinter as tk # pour la création et la manipulation de la fenêtre
from tkinter import ttk # pour ajouter quelques plugins à tkinter
from datetime import datetime # pour la gestion du temps et du minuteur
import webbrowser # pour l'ouverture du navigateur avec le lien du github de l'application
from tkinter import messagebox # pour les erreur et les validations
import darkdetect # pour la détection du thème de l'OS
import sys # Pour les fonctions suivantes : "exit", "executable", et "argv"
import subprocess # pour la fonction restart de l'application.
# ------------------------ fichiers de l'application
from variables import * # fichier contenant toutes les variables
from FenetreLicence import FenetreLicence # fichier contenant la fenêtre d'affichage de la licence
from Parametres import FenetreParametres # fichier contenant la fenêtre d'affichage des paramètres

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Variables
        self.paused = False # pour le bouton pause
        self.time_remaining = None # pour le temps restant
        self.pause_verrouillage = False # pour éviter les bugs du minuteur après des doubles cliques sur le bp pause
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
        fenetre_menu.add_command(label="Redémarrer", command=self.restart)
        fenetre_menu.add_command(label="Quitter", command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ Création d'un second menu 'Commandes'
        commandes_menu = tk.Menu(barre_de_menu, tearoff=0)
        commandes_menu.add_command(label="Effacer les entrées", command=self.clear_entrees)
        commandes_menu.add_command(label="Déporter minuteur", command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        barre_de_menu.add_cascade(label="Commandes", menu=commandes_menu)
        # ------------------------ Création d'un troisième menu 'Source'
        source_menu = tk.Menu(barre_de_menu, tearoff=0)
        source_menu.add_command(label="Ouvrir GitHub", command=lambda: webbrowser.open_new_tab(lien_du_github))
        source_menu.add_command(label="Afficher GitHub", command=lambda: FenetreInfoAffichageLienGitHub())
        source_menu.add_command(label="Afficher LICENCE", command=lambda: FenetreLicence())
        barre_de_menu.add_cascade(label="Source", menu=source_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        if parametres_fichier_json["value_affichage_heure"] == True:
            self.time_label = tk.Label(self, text="", font=("Arial", 24))
            self.time_label.pack(pady=20)
        else:
            self.espace_vide = tk.Label(self, text="", height=1, bg="white")
            self.espace_vide.pack()
        # ------------------------ Création de la frame principale :
        self.frame_principale = tk.Frame(self, width=900)
        self.frame_principale.pack(padx=20, pady=(0, 20))
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self.frame_principale, bg=couleur_frame_minuteur_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        if parametres_fichier_json["value_affichage_heure"] == True:
            self.time_frame.config(pady=10)
        self.temps_restant_label = tk.Label(self.time_frame, text=f"{nom_application}", font=("Arial", 24),
                                            bg=couleur_frame_minuteur_verte, fg="black")
        self.temps_restant_label.pack(pady=20)
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self.frame_principale, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="LANCER",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="normal", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.start_timer)
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE",
                                      activebackground=couleur_frame_minuteur_jaune,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.pause_timer)
        self.bouton_stop = tk.Button(self.boutons_frame, text="ARRÊTER",
                                     activebackground=couleur_frame_minuteur_rouge,
                                     state="disabled", width=30, height=2,
                                     justify="center", relief="groove",
                                     command=self.stop_timer)
        self.bouton_start.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_pause.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_stop.pack(side="left", padx=10, pady=10, expand=True)
        # ------------ Bouton pour déporter le temps restant dans une nouvelle fenêtre
        self.bouton_deporter_temps_restant = tk.Button(self.frame_principale, width=105,
                                                       text="Déporter le temps restant dans une nouvelle fenêtre",
                                                       activebackground=couleur_frame_minuteur_verte,
                                                       command=self.deporter_frame_temps_restant_dans_une_nouvelle_fenetre)
        self.bouton_deporter_temps_restant.pack(expand=True, pady=(5, 20))
        # ------------------------ Entrées pour la gestion du temps du minuteur (minutes et secondes)
        self.entrees_frame = tk.Frame(self.frame_principale)
        # self.entrees_frame.bind_all("<Button-1>", lambda event: event.widget.focus_set())
        self.entrees_frame.pack(padx=20)
        # ------------------------ Ajouter un titre à cette section
        self.titre_section_temps_entry = tk.Label(self.entrees_frame, text="Entrez un temps ici :", font=("Arial", 20), background="white")
        self.titre_section_temps_entry.pack(pady=10)
        # ------------ Entrée des minutes :
        self.labelframe_entree_minutes = tk.LabelFrame(self.entrees_frame, text="min", border=0, labelanchor="e")
        self.labelframe_entree_minutes.pack(side="left", padx=(10, 10))
        self.minutes_entry = tk.Spinbox(self.labelframe_entree_minutes, width=37, from_=0, to=60)
        self.minutes_entry.configure(validate="key", validatecommand=(self.minutes_entry.register(self.validate_numeric_input), "%P"))
        self.minutes_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.minutes_entry.pack(padx=(0, 5), expand=True)
        # ------------ Entrée des secondes :
        self.labelframe_entree_secondes = tk.LabelFrame(self.entrees_frame, text="s", border=0, labelanchor="e")
        self.labelframe_entree_secondes.pack(side="left", padx=(10, 20))
        self.seconds_entry = tk.Spinbox(self.labelframe_entree_secondes, width=38, from_=0, to=10800)
        self.seconds_entry.configure(validate="key", validatecommand=(self.seconds_entry.register(self.validate_numeric_input), "%P"))
        self.seconds_entry.bind(sequence='<Return>', func=lambda event: self.start_timer())
        self.seconds_entry.pack(padx=(0, 5), expand=True)
        self.clear_entrees()
        # ------------ Bouton pour effacer les entrées
        self.bouton_clear_entrees = tk.Button(self.entrees_frame, text="Effacer les entrées",
                                              activebackground=couleur_frame_minuteur_rouge,
                                              width=15,command=self.clear_entrees)
        self.bouton_clear_entrees.pack(side="right", padx=10, pady=20, expand=True)
        # ------------------------ Mise à jour de l'heure et gestion du thème
        self.update_time()
        self.gestion_theme_par_defaut()

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
        # ------------------------ Gestion des erreurs (**temporaire** !)
        if self.time_remaining >= temps_max:
            messagebox.showwarning("Avertissement", f"""\
    Le temps total de seconde du minuteur ne peut pas dépasser {int(temps_max / 60)} min !\n\
    Merci d'entrer une durée inférieure !""")
        elif self.time_remaining == 0:
            messagebox.showwarning(f"Avertissement", "Merci d'entrer une durée avant de lancer le minuteur")
        else:
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
            self.temps_restant_label.config(text=time_str, font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
            if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
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
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_rouge)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_rouge)
                else: pass
            elif percent_remaining <= 0.3:
                self.time_frame.config(bg=couleur_frame_minuteur_jaune)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_jaune)
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_jaune)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_jaune)
                else: pass
            else:
                self.time_frame.config(bg=couleur_frame_minuteur_verte)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_verte)
                if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
                    self.fenetre_deportee.config(bg=couleur_frame_minuteur_verte)
                    self.temps_restant_label_fenetre_deporte.config(bg=couleur_frame_minuteur_verte)
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
        self.time_remaining = 0  # Réinitialiser le temps restant
        # ------------------------ Configuration de l'état des entrées et des boutons
        self.bouton_start.config(state="normal")
        self.bouton_pause.config(state="disabled")
        self.bouton_stop.config(state="disabled")
        self.minutes_entry.config(state="normal")
        self.seconds_entry.config(state="normal")
        self.bouton_clear_entrees.config(state="normal")
        # ------------------------ Gestion affichage temps restant à effacer
        self.time_frame.config(bg=couleur_frame_minuteur_verte)
        self.temps_restant_label.config(text=f"{nom_application}", font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
        if hasattr(self, 'fenetre_deportee') and self.fenetre_deportee.winfo_exists():
            self.fenetre_deportee.config(background=couleur_frame_minuteur_verte)
            self.temps_restant_label_fenetre_deporte.config(text="Temps restant", font=("Arial", 35), bg=couleur_frame_minuteur_verte, fg="black")
        # ------------------------ Gestion du son :
        if parametres_fichier_json["value_sounds"] == True:
            jouer_sonnerie(True) # Jouer la sonnerie à la fin du timer
        else: pass
        if parametre_appel_bouton_ou_non == None:
            self.update_timer() # Arrêter la récursion de la fonction update_timer()
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
        if hasattr(self, 'espace_vide'): self.espace_vide.config(bg=theme_sombre)
        self.time_frame.config()
        self.frame_principale.config(bg=theme_sombre)
        self.boutons_frame.config(bg=theme_sombre)
        self.bouton_start.config(bg=theme_sombre, fg="white")
        self.bouton_pause.config(bg=theme_sombre, fg="white")
        self.bouton_stop.config(bg=theme_sombre, fg="white")
        self.bouton_clear_entrees.config(bg=theme_sombre, fg="white")
        self.entrees_frame.config(bg=theme_sombre)
        self.labelframe_entree_minutes.config(background=theme_sombre, fg="white")
        self.labelframe_entree_secondes.config(background=theme_sombre, fg="white")
        self.bouton_deporter_temps_restant.config(bg=theme_sombre, fg="white")
        self.titre_section_temps_entry.config(bg=theme_sombre, fg="white")

    def mettre_app_en_mode_light(self):
        self.config(bg="white")
        if hasattr(self, 'time_label'): self.time_label.config(bg="white", fg="black")
        if hasattr(self, 'espace_vide'): self.espace_vide.config(bg="white")
        self.time_frame.config()
        self.frame_principale.config(bg="white")
        self.boutons_frame.config(bg="white")
        self.bouton_start.config(bg="lightblue", fg="black")
        self.bouton_pause.config(bg="lightblue", fg="black")
        self.bouton_stop.config(bg="lightblue", fg="black")
        self.bouton_clear_entrees.config(bg="lightblue", fg="black")
        self.entrees_frame.config(bg="white")
        self.labelframe_entree_minutes.config(background="white", fg="black")
        self.labelframe_entree_secondes.config(background="white", fg="black")
        self.bouton_deporter_temps_restant.config(bg="lightblue", fg="black")
        self.titre_section_temps_entry.config(bg="white", fg="black")

    def open_parametres(self):
        def changement_du_theme(): self.gestion_theme_par_defaut()
        def gestion_restart_apres_modif_parametres(): self.restart()
        FenetreParametres(callback_theme=changement_du_theme, callback_restart=gestion_restart_apres_modif_parametres)

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

    def restart(self):
        if messagebox.askyesno(title="Redémarrer ?", message=f"Voulez vous vraiment redémarrer l'application {nom_application} ?"):
            self.destroy()
            subprocess.Popen([sys.executable] + sys.argv) # Redémarre l'application en exécutant à nouveau l'exécutable
        else: return

    def deselectionner_les_entry(self): self.focus_set()
    def clear_entrees(self):
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.insert(0, "0")
        self.deselectionner_les_entry()

    def validate_numeric_input(self, text):
        return text.isdigit() or text == ""

class FenetreInfoAffichageLienGitHub(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Information")
        self.geometry("340x170")
        self.config(background="white")
        # ------------------------ Configuration du style ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ------------------------ Affichage du texte
        self.texte_avant_le_lien = tk.Label(self, text="Lien vers le dépôt GitHub de GoTime :\n", font=("Arial", 12),
                                            bg="white", fg="black", justify='center')
        self.texte_avant_le_lien.pack(pady=(5, 0))
        # ------------------------ Afficher le lien
        self.lien_vers_le_github = ttk.Entry(self, width=32)
        self.lien_vers_le_github.insert(0, lien_du_github)
        self.lien_vers_le_github.pack(pady=(0, 5))
        # ------------------------ Affichage des deux boutons dans une frame
        self.frame_bouton_fenetre_info = tk.Frame(self, background="white", borderwidth=0)
        self.frame_bouton_fenetre_info.pack(pady=(10, 0))
        # Bouton pour quitter la fenetre
        self.bouton_quitter_fenetre = tk.Button(self.frame_bouton_fenetre_info, text="Quitter",
                                                activebackground=couleur_frame_minuteur_rouge, command=self.destroy)
        self.bouton_quitter_fenetre.pack(side=tk.LEFT, padx=(5, 5), expand=True)
        # Bouton pour copier le lien dans le presse papier
        self.bouton_copier_le_lien = tk.Button(self.frame_bouton_fenetre_info, text="Copier le lien", cursor="hand2",
                                               activebackground=couleur_frame_minuteur_jaune,command=self.copier_lien_et_update_bouton)
        self.bouton_copier_le_lien.pack(side=tk.RIGHT, padx=(5, 5), expand=True)
        self.couleur_original_bp_tkinter = self.bouton_copier_le_lien.cget("background")

    def copier_lien_et_update_bouton(self):
        self.copier_le_lien_dans_le_presse_papier()
        # ------------------------ Changer l'apparence du bouton après la copie
        self.bouton_copier_le_lien.config(text="Lien Copié !", activebackground=couleur_frame_minuteur_verte, background=couleur_frame_minuteur_verte)
        try:
            from PIL import Image, ImageTk
            # ------------------------ convertir l'image svg en format compatible tk
            checkmark = Image.open(chemin_image_checkmark)
            checkmark = checkmark.resize((20, 20), Image.ANTIALIAS)
            checkmark = ImageTk.PhotoImage(checkmark)
            self.bouton_copier_le_lien.config(image=checkmark, compound=tk.LEFT, command=None)
            self.bouton_copier_le_lien.image = checkmark
            self.after(2000, self.modifier_bouton_apres_deux_secondes_copie)
        except FileNotFoundError: pass

    def modifier_bouton_apres_deux_secondes_copie(self):
        self.bouton_copier_le_lien.configure(image="", text="Copier le lien", compound=tk.CENTER, background=self.couleur_original_bp_tkinter,
                                          activebackground=couleur_frame_minuteur_jaune, command=self.copier_lien_et_update_bouton)
        
    def copier_le_lien_dans_le_presse_papier(self):
        self.clipboard_clear()
        self.clipboard_append(lien_du_github)
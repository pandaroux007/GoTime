import tkinter as tk
# from tkinter import ttk
from datetime import datetime
import platform
import webbrowser
from tkinter import messagebox
import darkdetect
from json import dump, load
import os
from sys import exit

repertoire_courant = os.path.dirname(os.path.abspath(__file__))
nom_fichier_sauvegarde_config = "settings.json"
nom_image_application = "icone_gotime.ico"
chemin_fichier_parametres = os.path.join(repertoire_courant, nom_fichier_sauvegarde_config)
chemin_image_application = os.path.join(repertoire_courant, nom_image_application)
lien_du_github = "https://github.com/RP7-CODE/GoTime"
nom_application = "GoTime"
type_application = "DESKTOP"

def load_config():
    try:
        with open(chemin_fichier_parametres, 'r') as file:
            config = load(file)
        return config
    except FileNotFoundError:
        messagebox.showerror(title=f"ERROR {nom_application}", message=f"Le fichier de paramètre de {nom_application} n'a pas été trouvé pour lecture.")
        return None; exit()
    
def save_config(config):
    try:
        with open(chemin_fichier_parametres, 'w') as file:
            dump(config, file, indent=4)
    except FileNotFoundError:
        messagebox.showerror(title=f"ERROR {nom_application}", message=f"Le fichier de paramètre de {nom_application} n'a pas été trouvé pour écriture.")
        return None; exit()

parametres_fichier_json = load_config()
'''
if parametres_fichier_json == None:
    messagebox.showerror(title=f"ERROR {nom_application}", message="Hmm...something seems to have gone wrong 🤕️.")
    exit()
'''
systeme_exploitation = platform.system()
theme_sombre_couleur_hexa = "#242424"
taille_de_la_fenetre = "1080x720"
couleur_frame_minuteur_verte = "#73FF14"
couleur_frame_minuteur_jaune = "#F4EF12"
couleur_frame_minuteur_rouge = "#F84615"
temps_max_supporte_par_le_minuteur = 3600*3 # 10800

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Variables pour les paramètre du minuteur
        self.paused = False
        self.time_remaining = None
        self.valeur_state_bouton_start = None
        # ------------------------ Paramètrage de la fenêtre.
        self.title(f"{nom_application} - Application {type_application} - {systeme_exploitation}")
        self.geometry(taille_de_la_fenetre)
        self.minsize(1000, 680)
        self.config(background=theme_sombre_couleur_hexa)
        if systeme_exploitation == 'Windows': # à tester sur un windows !
            self.iconbitmap(chemin_image_application)
        else:
            pass
        # ------------------------ Barre de menu
        barre_de_menu = tk.Menu(self)
        # ------------------------ création d'un premier menu 'fenêtre'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="Settings", command=self.open_parametres)
        fenetre_menu.add_command(label=f"Close {nom_application}", command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ création d'un second menu 'Aide'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="Open source", command=self.open_github)
        fenetre_menu.add_command(label="Show source", command=self.show_github)
        barre_de_menu.add_cascade(label="Aide", menu=fenetre_menu)
        # ------------------------ création d'un troisième menu 'commandes'
        commandes_menu = tk.Menu(barre_de_menu, tearoff=0)
        commandes_menu.add_command(label="Start", command=self.start_timer)
        commandes_menu.add_command(label="Pause", command=self.pause_timer)
        commandes_menu.add_command(label="Stop", command=self.stop_timer)
        commandes_menu.add_command(label="Clear entry", command=self.clear_entrees)
        barre_de_menu.add_cascade(label="Commandes", menu=commandes_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        self.time_label = tk.Label(self, text="", font=("Arial", 24), bg="#242424", fg="white")
        self.time_label.pack(pady=20)
        # ------------------------ Création de la frame principale :
        self.frame_principale = tk.Frame(self, width=900)
        self.frame_principale.pack(padx=20, pady=(0, 20))
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self.frame_principale, bg=couleur_frame_minuteur_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.temps_restant_label = tk.Label(self.time_frame, text=f"{nom_application}", font=("Arial", 24), bg=couleur_frame_minuteur_verte, fg="black")
        self.temps_restant_label.pack(pady=20)
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self.frame_principale, bg=theme_sombre_couleur_hexa, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="START",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="normal", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.start_timer)
        self.valeur_state_bouton_start = False
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE",
                                      activebackground=couleur_frame_minuteur_verte,
                                      state="disabled", width=30, height=2,
                                      justify="center", relief="groove",
                                      command=self.pause_timer)
        self.bouton_stop = tk.Button(self.boutons_frame, text="STOP",
                                     activebackground=couleur_frame_minuteur_verte,
                                     state="disabled", width=30, height=2,
                                     justify="center", relief="groove",
                                     command=self.stop_timer)
        self.bouton_start.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_pause.pack(side="left", padx=10, pady=10, expand=True)
        self.bouton_stop.pack(side="left", padx=10, pady=10, expand=True)
        # ------------------------ Entrées pour la gestion du temps du minuteur (minutes et secondes)
        # ------------ Entrée des minutes :
        self.entrees_frame = tk.Frame(self.frame_principale, bg=theme_sombre_couleur_hexa)
        self.entrees_frame.pack(padx=20, pady=(0, 20))
        self.minutes_entry = tk.Entry(self.entrees_frame, width=40)
        self.minutes_entry.insert(0, "0")
        self.minutes_entry.bind(sequence='<Return>', func=self.start_timer)
        self.minutes_entry.pack(side="left", padx=(10, 10), expand=True)
        # ------------ Entrée des secondes :
        self.seconds_entry = tk.Entry(self.entrees_frame, width=40)
        self.seconds_entry.insert(0, "0")
        self.seconds_entry.bind(sequence='<Return>', func=self.start_timer)
        self.seconds_entry.pack(side="left", padx=(10, 20), expand=True)
        # ------------ Boutons pour effacer les entrées
        self.bouton_clear_entrees = tk.Button(self.entrees_frame, text="Effacer les entrées", activebackground=couleur_frame_minuteur_jaune,width=15,command=self.clear_entrees)
        self.bouton_clear_entrees.pack(side="left", padx=10, pady=20, expand=True)
        # ------------------------ Mise à jour de l'heure, gestion du thème et activation de la gestion des entrées
        self.update_time()
        self.gestion_theme_par_defaut()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Met à jour toutes les secondes

    def start_timer(self):
        minutes = int(self.minutes_entry.get())
        seconds = int(self.seconds_entry.get())
        self.total_seconds = minutes * 60 + seconds
        self.time_remaining = self.total_seconds
        if self.time_remaining >= temps_max_supporte_par_le_minuteur:
            messagebox.showwarning(f"WARNING {nom_application} !", f"""\
Le temps total de seconde du minuteur ne peut pas dépasser \
{temps_max_supporte_par_le_minuteur}s !\nTemps entré : {self.time_remaining}s\n\
Merci d'entrer un temps de durée inferieur !""")
        elif self.time_remaining == 0:
            messagebox.showwarning(f"WARNING {nom_application} !", "Merci d'entrer un temps avant de lancer le minuteur")
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
            # Calcul des pourcentages
            total_time = self.total_seconds
            time_left = self.time_remaining
            percent_remaining = time_left / total_time
            # Changement de couleur en fonction du pourcentage restant
            if percent_remaining <= 0.2:
                self.time_frame.config(bg=couleur_frame_minuteur_rouge)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_rouge)
            elif percent_remaining <= 0.3:
                self.time_frame.config(bg=couleur_frame_minuteur_jaune)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_jaune)
            else:
                self.time_frame.config(bg=couleur_frame_minuteur_verte)
                self.temps_restant_label.config(bg=couleur_frame_minuteur_verte)
            self.after(1000, self.update_timer)
        elif self.paused:
            pass  # Pause le minuteur sans décrémenter le temps
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
        if parametre_appel_bouton_ou_non == None:
            self.update_timer()  # Arrêter la récursion de la fonction update_timer()
        else:
            pass

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
            messagebox.showerror(f"ERREUR {nom_application}", "La sélection automatique du thème de l'application a échoué... L'application va automatiquement se lancer en mode sombre.")
            self.mettre_app_en_mode_dark()

    def mettre_app_en_mode_dark(self):
        self.config(bg=theme_sombre_couleur_hexa)
        self.time_label.config(bg=theme_sombre_couleur_hexa, fg="white")
        self.time_frame.config()
        self.frame_principale.config(bg=theme_sombre_couleur_hexa)
        self.boutons_frame.config(bg=theme_sombre_couleur_hexa)
        self.bouton_start.config(bg=theme_sombre_couleur_hexa, fg="white")
        self.bouton_pause.config(bg=theme_sombre_couleur_hexa, fg="white")
        self.bouton_stop.config(bg=theme_sombre_couleur_hexa, fg="white")
        self.entrees_frame.config(bg=theme_sombre_couleur_hexa)

    def mettre_app_en_mode_light(self):
        self.config(bg="white")
        self.time_label.config(bg="white", fg="black")
        self.time_frame.config()
        self.frame_principale.config(bg="white")
        self.boutons_frame.config(bg="white")
        self.bouton_start.config(bg="lightblue", fg="black")
        self.bouton_pause.config(bg="lightblue", fg="black")
        self.bouton_stop.config(bg="lightblue", fg="black")
        self.entrees_frame.config(bg="white")

    def open_parametres(self):
        self.parametre_radiobutton_value = tk.StringVar()
        self.parametre_radiobutton_value.set(parametres_fichier_json["value_theme"])
        self.fenetre_parametres = tk.Toplevel()
        self.fenetre_parametres.title(f"{nom_application} - Paramètres")
        self.fenetre_parametres.geometry("600x400")
        self.fenetre_parametres.maxsize(600, 400)
        self.fenetre_parametres.minsize(600, 400)
        # ------------------------ Créer le titre de la page de paramètres
        label_titre_parametres = tk.Label(self.fenetre_parametres, text=f"{nom_application} - Paramètres", font=("Arial", 24))
        label_titre_parametres.pack(pady=10)
        # ------------------------ Frame pour regrouper les radiobutton entre eux
        selection_theme = tk.Frame(self.fenetre_parametres)
        selection_theme.pack(pady=20)
        selection_parametre_theme_os_default = tk.Radiobutton(selection_theme, text=f"{nom_application} mode Default", value="DEFAULT", variable=self.parametre_radiobutton_value)
        selection_parametre_theme_os_dark = tk.Radiobutton(selection_theme, text=f"{nom_application} mode Dark", value="DARK", variable=self.parametre_radiobutton_value)
        selection_parametre_theme_os_light = tk.Radiobutton(selection_theme, text=f"{nom_application} mode Light", value="LIGHT", variable=self.parametre_radiobutton_value)
        selection_parametre_theme_os_default.pack(anchor='w')
        selection_parametre_theme_os_dark.pack(anchor='w')
        selection_parametre_theme_os_light.pack(anchor='w')
        # ------------------------ Frame pour regrouper les boutons entre eux
        frame_boutons_parametres = tk.Frame(self.fenetre_parametres, width=200, height=400)
        bouton_validation_parametre = tk.Button(frame_boutons_parametres, text="Appliquer les paramètres et quitter", command=self.apply_parametres)
        bouton_validation_parametre.pack(fill="x", padx=20)
        bouton_validation_parametre = tk.Button(frame_boutons_parametres, text="Annuler", command=self.fenetre_parametres.destroy)
        bouton_validation_parametre.pack(fill="x", padx=20)
        frame_boutons_parametres.pack(fill="x", padx=20)

    def apply_parametres(self):
        # Gestion du thème depuis les paramètres
        selected_theme = self.parametre_radiobutton_value.get()
        if selected_theme != parametres_fichier_json["value_theme"]:
            parametres_fichier_json["value_theme"] = selected_theme
            save_config(parametres_fichier_json)
            self.gestion_theme_par_defaut()  # Met à jour le thème en temps réel
        self.fenetre_parametres.destroy()

    def show_github(self):
        messagebox.showinfo(f"Source {nom_application}", f"Lien du GitHub du projet :\n{lien_du_github}")

    def open_github(self):
        webbrowser.open_new(lien_du_github)

    def clear_entrees(self):
        self.minutes_entry.delete(0, tk.END)
        self.seconds_entry.delete(0, tk.END)
        self.minutes_entry.insert(0, "0")
        self.seconds_entry.insert(0, "0")

if __name__ == "__main__":
    root = Application()
    root.mainloop()
import tkinter as tk
from datetime import datetime, timedelta
import platform
import webbrowser
from tkinter import messagebox

systeme_exploitation = platform.system()
lien_du_github = "https://github.com/RP7-CODE/GoTime"
nom_application = "GoTime"
type_application = "DESKTOP"
theme_sombre_couleur_hexa = "#242424"
taille_de_la_fenetre = "1080x720"
couleur_frame_minuteur_verte = "#73FF14"
# couleur_frame_minuteur_jaune = ""
# couleur_frame_minuteur_rouge = ""

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        # ------------------------ Paramètrage de la fenêtre.
        self.title(f"{nom_application} - Application {type_application} - {systeme_exploitation}")
        self.geometry(taille_de_la_fenetre)
        self.minsize(1000, 680)
        self.config(background=theme_sombre_couleur_hexa)
        # ------------------------ Barre de menu
        barre_de_menu = tk.Menu(self)
        # ------------------------ création d'un premier menu 'fenêtre'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="close page", command=self.quit)
        fenetre_menu.add_command(label="Plein écran", command=self.quit)
        fenetre_menu.add_command(label="Taille MIN", command=self.quit)
        barre_de_menu.add_cascade(label="Fenêtre", menu=fenetre_menu)
        # ------------------------ création d'un second menu 'Aide'
        fenetre_menu = tk.Menu(barre_de_menu, tearoff=0)
        fenetre_menu.add_command(label="Open source", command=self.open_github)
        fenetre_menu.add_command(label="Show source", command=self.show_github)
        barre_de_menu.add_cascade(label="Aide", menu=fenetre_menu)
        # ------------------------ Ajout de la barre de menu à la fenêtre
        self.config(menu=barre_de_menu)
        # ------------------------ Affichage de l'heure en haut de la fenêtre
        self.time_label = tk.Label(self, text="", font=("Arial", 24), bg="#242424", fg="white")
        self.time_label.pack(pady=20)
        # ------------------------ Création de la frame de couleur et affichage d'un texte dedans (ici le temps restant)
        self.time_frame = tk.Frame(self, bg=couleur_frame_minuteur_verte, height=80)
        self.time_frame.pack(fill="x", padx=20, pady=(0, 20))
        # ------------------------ Boutons pour la gestion du minuteur
        self.boutons_frame = tk.Frame(self, bg=theme_sombre_couleur_hexa, height=80)
        self.boutons_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.bouton_start = tk.Button(self.boutons_frame, text="START")
        self.bouton_pause = tk.Button(self.boutons_frame, text="PAUSE")
        self.bouton_stop = tk.Button(self.boutons_frame, text="STOP")
        self.bouton_start.pack(side="left", padx=10)
        self.bouton_pause.pack(side="left", padx=10)
        self.bouton_stop.pack(side="left", padx=10)
        # ------------------------ Mise à jour de l'heure
        self.update_time()

    def update_time(self):
        current_time = datetime.now().strftime("%H:%M:%S")
        self.time_label.config(text=current_time)
        self.after(1000, self.update_time)  # Met à jour toutes les secondes

    def show_github(self):
        messagebox.showinfo(f"Source {nom_application}", f"Lien du GitHub du projet :\n{lien_du_github}")
        print(f"Ouverture du github de {nom_application} dans une nouvelle fenêtre de navigateur !")

    def open_github(self):
        print("Ouverture de la fenêtre d'information pour afficher le lien du github !")
        webbrowser.open_new(lien_du_github)

    def fenetre_en_plein_ecran(self):
        self.attributes("-fullscreen", True)

    def fenetre_en_plein_ecran(self):
        self.attributes("-fullscreen", False)

if __name__ == "__main__":
    root = Application()
    root.mainloop()
import tkinter as tk
from tkinter import ttk
# fichiers programmes
from Definitions import *

class FenetreInfoAffichageLienGitHub(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.title("Information")
        self.geometry("340x170")
        self.resizable(False, False)
        self.config(background="white")
        self.wm_iconbitmap()
        self.logo = tk.PhotoImage(file=chemin_image_application)
        self.iconphoto(False, self.logo)
        self.bind("<1>", lambda event: event.widget.focus_set())
        # ------------------------ Configuration du style ttk
        self.style = ttk.Style()
        self.style.theme_use('clam')
        # ------------------------ Affichage du texte
        self.texte_avant_le_lien = tk.Label(self, text="Lien vers le dépôt GitHub de GoTime :\n", font=("Arial", 12),
                                            bg="white", fg="black", justify='center')
        self.texte_avant_le_lien.pack(pady=(5, 0))
        # ------------------------ Afficher le lien
        self.lien_vers_le_github = ttk.Entry(self, width=38)
        self.lien_vers_le_github.insert(0, lien_du_github)
        self.lien_vers_le_github.pack(pady=(0, 5))
        # ------------------------ Affichage des deux boutons dans une frame
        self.frame_bouton_fenetre_info = tk.Frame(self, background="white", borderwidth=0, width=38)
        self.frame_bouton_fenetre_info.pack(pady=(10, 0))
        # Bouton pour quitter la fenetre
        self.bouton_quitter_fenetre = tk.Button(self.frame_bouton_fenetre_info, text="Quitter",
                                                activebackground=couleur_frame_minuteur_rouge, command=self.destroy)
        self.bouton_quitter_fenetre.pack(side=tk.LEFT, padx=(0, 5), expand=True)
        # Bouton pour copier le lien dans le presse papier
        self.bouton_copier_le_lien = tk.Button(self.frame_bouton_fenetre_info, text="Copier le lien", cursor="hand2",
                                               activebackground=couleur_frame_minuteur_jaune, command=self.copier_lien_et_update_bouton)
        self.bouton_copier_le_lien.pack(side=tk.RIGHT, padx=(5, 0), expand=True)
        self.couleur_original_bp_copier_le_lien = self.bouton_copier_le_lien.cget("background")

    def copier_lien_et_update_bouton(self):
        self.copier_le_lien_dans_le_presse_papier()
        # ------------------------ Changer l'apparence du bouton après la copie
        self.bouton_copier_le_lien.config(text="Lien Copié !", activebackground=couleur_frame_minuteur_verte, background=couleur_frame_minuteur_verte)
        try:
            from PIL import Image, ImageTk
            # ------------------------ convertir l'image svg en format compatible tk
            checkmark = Image.open(chemin_image_checkmark)
            checkmark = checkmark.resize((24, 18))
            checkmark = ImageTk.PhotoImage(checkmark)
            self.bouton_copier_le_lien.config(image=checkmark, compound=tk.LEFT, command=None)
            self.bouton_copier_le_lien.image = checkmark
            self.after(2000, self.modifier_bouton_apres_deux_secondes_copie)
        except FileNotFoundError: pass

    def modifier_bouton_apres_deux_secondes_copie(self):
        self.bouton_copier_le_lien.configure(image="", text="Copier le lien", compound=tk.CENTER, background=self.couleur_original_bp_copier_le_lien,
                                          activebackground=couleur_frame_minuteur_jaune, command=self.copier_lien_et_update_bouton)
        
    def copier_le_lien_dans_le_presse_papier(self): # ne semble pas fonctionner sous windows ? Peut-être cette fonction gère t-elle un pressepapier interne à tkinter ?
        self.clipboard_clear()
        self.clipboard_append(lien_du_github)
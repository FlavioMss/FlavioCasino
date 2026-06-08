"""
ui/mines_ui.py
--------------
Interface graphique du jeu Mines.
Affiche une grille 5x5 de boutons cliquables.

COMMENT MODIFIER :
- Couleurs des cases : COULEUR_CASE_*, COULEUR_MINE, COULEUR_GEMME
- Pour changer la taille des boutons : width/height dans creer_grille_boutons()
"""

import tkinter as tk
from tkinter import messagebox

import player
import utils
from games import mines  # La logique du jeu

# Couleurs des cases (facile à modifier !)
COULEUR_CASE_NORMALE = "#0f3460"      # Case non révélée
COULEUR_CASE_GEMME = "#4ecca3"        # Case avec gemme (safe)
COULEUR_MINE = "#e94560"              # Case avec mine
COULEUR_CASE_INACTIVE = "#555555"     # Toutes les cases après fin de partie


class FenetreMines:
    """Interface graphique du jeu Mines."""

    def __init__(self, fenetre, callback_mise_a_jour_argent):
        self.fenetre = fenetre
        self.callback_argent = callback_mise_a_jour_argent

        # État du jeu
        self.grille = []               # Liste des mines (True/False)
        self.cases_revelees = 0        # Nombre de cases révélées sans mine
        self.mise_actuelle = 0
        self.nombre_mines = 3          # Nombre de mines par défaut
        self.partie_en_cours = False
        self.boutons_cases = []        # Liste des boutons de la grille

        # Configuration de la fenêtre
        self.fenetre.title("Casino - Mines")
        self.fenetre.geometry("520x650")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du jeu Mines."""

        # Titre
        tk.Label(self.fenetre, text="💣 MINES",
                 font=utils.POLICE_TITRE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND).pack(pady=10)

        # Solde
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND
        )
        self.label_argent.pack()

        # ----- PARAMÈTRES -----
        cadre_params = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_params.pack(pady=10)

        # Mise
        tk.Label(cadre_params, text="Mise :", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND).grid(row=0, column=0, padx=5)

        self.champ_mise = tk.Entry(cadre_params, font=utils.POLICE_NORMALE, width=8,
                                   bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
                                   insertbackground=utils.COULEUR_TEXTE)
        self.champ_mise.grid(row=0, column=1, padx=5)
        self.champ_mise.insert(0, "100")

        # Nombre de mines
        tk.Label(cadre_params, text="Mines :", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND).grid(row=0, column=2, padx=5)

        self.spin_mines = tk.Spinbox(
            cadre_params, from_=1, to=24, width=5,
            font=utils.POLICE_NORMALE, bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
            buttonbackground=utils.COULEUR_BOUTON
        )
        self.spin_mines.grid(row=0, column=3, padx=5)
        self.spin_mines.delete(0, "end")
        self.spin_mines.insert(0, "3")  # 3 mines par défaut

        # ----- INFO PARTIE EN COURS -----
        cadre_info = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_info.pack(pady=5)

        self.label_cases_revelees = tk.Label(
            cadre_info, text="Cases révélées : 0",
            font=utils.POLICE_NORMALE, fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_cases_revelees.pack(side="left", padx=15)

        self.label_multiplicateur = tk.Label(
            cadre_info, text="Multiplicateur : x1.00",
            font=utils.POLICE_NORMALE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND
        )
        self.label_multiplicateur.pack(side="left", padx=15)

        self.label_gain_potentiel = tk.Label(
            cadre_info, text="Gain potentiel : 0 €",
            font=utils.POLICE_NORMALE, fg=utils.COULEUR_SUCCÈS, bg=utils.COULEUR_FOND
        )
        self.label_gain_potentiel.pack(side="left", padx=15)

        # ----- GRILLE 5x5 -----
        self.cadre_grille = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        self.cadre_grille.pack(pady=10)
        self.creer_grille_boutons()

        # ----- RÉSULTAT -----
        self.label_resultat = tk.Label(
            self.fenetre, text="Démarrez une partie !",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_resultat.pack(pady=5)

        # ----- BOUTONS D'ACTION -----
        cadre_boutons = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_boutons.pack(pady=10)

        self.bouton_demarrer = tk.Button(
            cadre_boutons, text="▶ DÉMARRER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_ACCENT, fg=utils.COULEUR_TEXTE,
            width=14, height=2, cursor="hand2", command=self.demarrer_partie
        )
        self.bouton_demarrer.pack(side="left", padx=5)

        self.bouton_retirer = tk.Button(
            cadre_boutons, text="💰 RETIRER",
            font=utils.POLICE_GRANDE, bg="#2ecc71", fg=utils.COULEUR_TEXTE,
            width=12, height=2, cursor="hand2", command=self.retirer_gains,
            state="disabled"
        )
        self.bouton_retirer.pack(side="left", padx=5)

    def creer_grille_boutons(self):
        """Crée les 25 boutons de la grille 5x5."""

        # Effacer les anciens boutons s'il y en a
        for widget in self.cadre_grille.winfo_children():
            widget.destroy()

        self.boutons_cases = []

        # Créer 5 lignes de 5 boutons
        for ligne in range(mines.TAILLE_GRILLE):
            for colonne in range(mines.TAILLE_GRILLE):
                # Calculer l'index de cette case (0 à 24)
                index = mines.position_vers_index(ligne, colonne)

                # Créer le bouton pour cette case
                bouton = tk.Button(
                    self.cadre_grille,
                    text="",
                    font=("Arial", 20),
                    bg=COULEUR_CASE_NORMALE,
                    fg=utils.COULEUR_TEXTE,
                    width=3,
                    height=1,
                    cursor="hand2",
                    state="disabled",
                    # lambda avec index=index pour capturer la valeur actuelle
                    command=lambda i=index: self.cliquer_case(i)
                )
                bouton.grid(row=ligne, column=colonne, padx=3, pady=3)
                self.boutons_cases.append(bouton)

    def demarrer_partie(self):
        """Démarre une nouvelle partie de Mines."""

        # Récupérer et valider la mise
        valide, resultat = utils.mise_est_valide(self.champ_mise.get(), player.get_argent())
        if not valide:
            messagebox.showerror("Mise invalide", resultat)
            return

        # Récupérer le nombre de mines
        try:
            nb_mines = int(self.spin_mines.get())
        except ValueError:
            messagebox.showerror("Erreur", "Nombre de mines invalide !")
            return

        if nb_mines < mines.MINES_MINIMUM or nb_mines > mines.MINES_MAXIMUM:
            messagebox.showerror("Erreur", f"Les mines doivent être entre {mines.MINES_MINIMUM} et {mines.MINES_MAXIMUM} !")
            return

        self.mise_actuelle = resultat
        self.nombre_mines = nb_mines
        self.cases_revelees = 0
        self.partie_en_cours = True

        # Déduire la mise
        player.modifier_argent(-self.mise_actuelle)
        self.label_argent.config(text=f"Solde : {utils.formater_argent(player.get_argent())}")

        # Créer la grille avec les mines
        self.grille = mines.creer_grille(self.nombre_mines)

        # Activer les boutons des cases
        for bouton in self.boutons_cases:
            bouton.config(state="normal", bg=COULEUR_CASE_NORMALE, text="")

        # Activer Retirer, désactiver Démarrer
        self.bouton_demarrer.config(state="disabled")
        self.bouton_retirer.config(state="normal")
        self.champ_mise.config(state="disabled")
        self.spin_mines.config(state="disabled")

        # Mettre à jour l'affichage
        self.mettre_a_jour_info()
        self.label_resultat.config(text=f"Évitez les {self.nombre_mines} mines !", fg=utils.COULEUR_TEXTE)

    def cliquer_case(self, index):
        """
        Le joueur clique sur une case.
        Vérifie si c'est une mine ou une case safe.
        """

        if not self.partie_en_cours:
            return

        # Vérifier si cette case a une mine
        a_mine = self.grille[index]

        if a_mine:
            # 💥 MINE ! Le joueur perd tout
            self.boutons_cases[index].config(text="💣", bg=COULEUR_MINE)
            self.fin_partie_perdue()
        else:
            # ✅ Case safe !
            self.cases_revelees += 1
            self.boutons_cases[index].config(text="💎", bg=COULEUR_CASE_GEMME, state="disabled")
            self.mettre_a_jour_info()
            self.label_resultat.config(
                text=f"Case safe ! Continuez ou retirez vos gains.",
                fg=utils.COULEUR_SUCCÈS
            )

    def mettre_a_jour_info(self):
        """Met à jour les labels d'information."""

        multiplicateur = mines.calculer_multiplicateur(self.cases_revelees, self.nombre_mines)
        gain_potentiel = mines.calculer_gain_retrait(self.mise_actuelle, self.cases_revelees, self.nombre_mines)

        self.label_cases_revelees.config(text=f"Cases révélées : {self.cases_revelees}")
        self.label_multiplicateur.config(text=f"Multiplicateur : x{multiplicateur}")
        self.label_gain_potentiel.config(text=f"Gain potentiel : {utils.formater_argent(gain_potentiel)}")

    def retirer_gains(self):
        """Le joueur retire ses gains."""

        if not self.partie_en_cours:
            return

        gain = mines.calculer_gain_retrait(self.mise_actuelle, self.cases_revelees, self.nombre_mines)
        player.modifier_argent(gain)
        player.enregistrer_resultat(True)

        profit = gain - self.mise_actuelle
        self.label_resultat.config(
            text=f"✅ Vous retirez {utils.formater_argent(gain)} (profit : +{utils.formater_argent(profit)})",
            fg=utils.COULEUR_SUCCÈS
        )

        self.fin_partie()

    def fin_partie_perdue(self):
        """Affiche toutes les mines et termine la partie en défaite."""

        player.enregistrer_resultat(False)

        # Révéler toutes les mines
        for index in range(len(self.grille)):
            if self.grille[index]:  # Si mine
                self.boutons_cases[index].config(text="💣", bg=COULEUR_MINE)

        self.label_resultat.config(
            text=f"💥 BOOM ! Vous perdez {utils.formater_argent(self.mise_actuelle)}",
            fg=utils.COULEUR_ECHEC
        )

        self.fin_partie()

    def fin_partie(self):
        """Termine la partie et remet les boutons en état initial."""

        self.partie_en_cours = False

        # Désactiver toutes les cases
        for bouton in self.boutons_cases:
            bouton.config(state="disabled")

        # Réactiver Démarrer, désactiver Retirer
        self.bouton_demarrer.config(state="normal")
        self.bouton_retirer.config(state="disabled")
        self.champ_mise.config(state="normal")
        self.spin_mines.config(state="normal")

        # Mettre à jour l'argent
        self.label_argent.config(text=f"Solde : {utils.formater_argent(player.get_argent())}")
        self.callback_argent()

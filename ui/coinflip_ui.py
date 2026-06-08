"""
ui/coinflip_ui.py
-----------------
Interface graphique du jeu Pile ou Face.
Simple et très lisible.

COMMENT MODIFIER :
- Pour changer les couleurs des boutons Pile/Face : chercher "PILE" et "FACE"
- Pour changer l'animation : modifier la fonction animer_piece()
"""

import tkinter as tk
from tkinter import messagebox

import player
import utils
from games import coinflip  # La logique du jeu


class FenetreCoinFlip:
    """Interface graphique du jeu Pile ou Face."""

    def __init__(self, fenetre, callback_mise_a_jour_argent):
        """
        Initialise la fenêtre du jeu.

        Paramètres :
        - fenetre : la fenêtre Tkinter
        - callback_mise_a_jour_argent : fonction à appeler pour mettre à jour le menu
        """

        self.fenetre = fenetre
        self.callback_argent = callback_mise_a_jour_argent

        # Variables du jeu
        self.choix_joueur = None  # "PILE" ou "FACE"

        # Configuration de la fenêtre
        self.fenetre.title("Casino - Pile ou Face")
        self.fenetre.geometry("400x500")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        # Créer l'interface
        self.creer_interface()

    def creer_interface(self):
        """Crée tous les éléments de l'interface."""

        # Titre
        tk.Label(
            self.fenetre,
            text="🪙 PILE OU FACE",
            font=utils.POLICE_TITRE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        ).pack(pady=15)

        # Affichage de l'argent
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        self.label_argent.pack()

        # Grand emoji pièce (affiche le résultat)
        self.label_piece = tk.Label(
            self.fenetre,
            text="🪙",
            font=("Arial", 60),
            bg=utils.COULEUR_FOND
        )
        self.label_piece.pack(pady=15)

        # Message résultat
        self.label_resultat = tk.Label(
            self.fenetre,
            text="Choisissez et misez !",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_TEXTE,
            bg=utils.COULEUR_FOND
        )
        self.label_resultat.pack()

        # ----- CHOIX PILE ou FACE -----
        tk.Label(
            self.fenetre,
            text="Votre choix :",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            bg=utils.COULEUR_FOND
        ).pack(pady=(15, 5))

        # Cadre pour les deux boutons de choix
        cadre_choix = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_choix.pack()

        self.bouton_pile = tk.Button(
            cadre_choix,
            text="PILE",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=8,
            height=2,
            cursor="hand2",
            command=lambda: self.selectionner_choix("PILE")
        )
        self.bouton_pile.pack(side="left", padx=10)

        self.bouton_face = tk.Button(
            cadre_choix,
            text="FACE",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=8,
            height=2,
            cursor="hand2",
            command=lambda: self.selectionner_choix("FACE")
        )
        self.bouton_face.pack(side="left", padx=10)

        # ----- MISE -----
        tk.Label(
            self.fenetre,
            text="Votre mise :",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            bg=utils.COULEUR_FOND
        ).pack(pady=(15, 5))

        self.champ_mise = tk.Entry(
            self.fenetre,
            font=utils.POLICE_NORMALE,
            width=15,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            insertbackground=utils.COULEUR_TEXTE
        )
        self.champ_mise.pack()
        self.champ_mise.insert(0, "100")  # Valeur par défaut

        # Bouton Jouer
        self.bouton_jouer = tk.Button(
            self.fenetre,
            text="LANCER LA PIÈCE",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_ACCENT,
            fg=utils.COULEUR_TEXTE,
            width=20,
            height=2,
            cursor="hand2",
            command=self.jouer
        )
        self.bouton_jouer.pack(pady=20)

    def selectionner_choix(self, choix):
        """
        Enregistre le choix du joueur (PILE ou FACE).
        Met en évidence le bouton sélectionné.
        """

        self.choix_joueur = choix

        # Mettre en évidence le bouton choisi
        if choix == "PILE":
            self.bouton_pile.config(bg=utils.COULEUR_ACCENT)
            self.bouton_face.config(bg=utils.COULEUR_BOUTON)
        else:
            self.bouton_face.config(bg=utils.COULEUR_ACCENT)
            self.bouton_pile.config(bg=utils.COULEUR_BOUTON)

        self.label_resultat.config(
            text=f"Vous avez choisi : {choix}",
            fg=utils.COULEUR_TEXTE
        )

    def jouer(self):
        """Lance la partie de Pile ou Face."""

        # Vérifier que le joueur a fait un choix
        if self.choix_joueur is None:
            messagebox.showwarning("Attention", "Choisissez PILE ou FACE d'abord !")
            return

        # Vérifier la mise
        valide, resultat = utils.mise_est_valide(self.champ_mise.get(), player.get_argent())
        if not valide:
            messagebox.showerror("Mise invalide", resultat)
            return

        mise = resultat

        # Déduire la mise
        player.modifier_argent(-mise)

        # Lancer la pièce
        resultat_piece = coinflip.lancer_piece()

        # Vérifier si gagné
        victoire = coinflip.verifier_resultat(self.choix_joueur, resultat_piece)

        # Calculer le gain
        gain = coinflip.calculer_gain(mise, victoire)

        # Mettre à jour l'argent si victoire
        if victoire:
            player.modifier_argent(gain)

        # Enregistrer le résultat
        player.enregistrer_resultat(victoire)

        # Afficher le résultat
        self.afficher_resultat(resultat_piece, victoire, mise, gain)

    def afficher_resultat(self, resultat_piece, victoire, mise, gain):
        """Affiche le résultat de la partie."""

        # Afficher PILE ou FACE avec emoji
        if resultat_piece == "PILE":
            self.label_piece.config(text="🟡")  # Côté or = PILE
        else:
            self.label_piece.config(text="⚪")  # Côté argent = FACE

        if victoire:
            profit = gain - mise
            self.label_resultat.config(
                text=f"✅ {resultat_piece} ! Vous gagnez +{utils.formater_argent(profit)} !",
                fg=utils.COULEUR_SUCCÈS
            )
        else:
            self.label_resultat.config(
                text=f"❌ {resultat_piece} ! Vous perdez {utils.formater_argent(mise)} !",
                fg=utils.COULEUR_ECHEC
            )

        # Mettre à jour l'affichage de l'argent
        self.label_argent.config(
            text=f"Solde : {utils.formater_argent(player.get_argent())}"
        )

        # Mettre à jour le menu principal
        self.callback_argent()

        # Réinitialiser le choix pour la prochaine partie
        self.choix_joueur = None
        self.bouton_pile.config(bg=utils.COULEUR_BOUTON)
        self.bouton_face.config(bg=utils.COULEUR_BOUTON)

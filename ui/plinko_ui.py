"""
ui/plinko_ui.py
---------------
Interface graphique du jeu Plinko.
Affiche une animation simple de la balle qui tombe.

COMMENT MODIFIER :
- Couleurs : COULEUR_* en haut du fichier
- Vitesse d'animation : DELAI_ANIMATION_MS
- Taille du canvas : LARGEUR_CANVAS / HAUTEUR_CANVAS
"""

import tkinter as tk
from tkinter import messagebox

import player
import utils
from games import plinko  # La logique du jeu

# ============================================================
# CONFIGURATION DE L'ANIMATION
# ============================================================

DELAI_ANIMATION_MS = 120     # Millisecondes entre chaque étape d'animation (plus grand = plus lent)
LARGEUR_CANVAS = 420         # Largeur du canvas (zone de dessin)
HAUTEUR_CANVAS = 300         # Hauteur du canvas

# Couleurs
COULEUR_FOND_CANVAS = "#0d1b2a"
COULEUR_CLOU = "#ffffff"
COULEUR_BALLE = "#f5a623"    # Or
COULEUR_CASE_NORMALE = "#0f3460"
COULEUR_CASE_ACTIVE = "#e94560"  # Case où atterrit la balle


class FenetrePlinko:
    """Interface graphique du jeu Plinko."""

    def __init__(self, fenetre, callback_mise_a_jour_argent):
        self.fenetre = fenetre
        self.callback_argent = callback_mise_a_jour_argent

        # État du jeu
        self.animation_en_cours = False
        self.chemin_balle = []       # Liste des directions ('G' ou 'D')
        self.etape_animation = 0     # Étape actuelle de l'animation

        # Configuration de la fenêtre
        self.fenetre.title("Casino - Plinko")
        self.fenetre.geometry("450x620")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        self.creer_interface()
        self.dessiner_grille()

    def creer_interface(self):
        """Crée l'interface Plinko."""

        # Titre
        tk.Label(self.fenetre, text="⚪ PLINKO",
                 font=utils.POLICE_TITRE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND).pack(pady=10)

        # Solde
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND
        )
        self.label_argent.pack()

        # Canvas pour l'animation
        self.canvas = tk.Canvas(
            self.fenetre, width=LARGEUR_CANVAS, height=HAUTEUR_CANVAS,
            bg=COULEUR_FOND_CANVAS, highlightthickness=1,
            highlightbackground=utils.COULEUR_ACCENT
        )
        self.canvas.pack(pady=10)

        # Affichage des multiplicateurs
        self.label_multiplicateurs = tk.Label(
            self.fenetre,
            text=self.formater_multiplicateurs(),
            font=("Arial", 10),
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        self.label_multiplicateurs.pack()

        # Message résultat
        self.label_resultat = tk.Label(
            self.fenetre, text="Entrez votre mise et lancez !",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_resultat.pack(pady=5)

        # Mise + Bouton
        cadre_bas = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_bas.pack(pady=10)

        tk.Label(cadre_bas, text="Mise :", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND).pack(side="left")

        self.champ_mise = tk.Entry(cadre_bas, font=utils.POLICE_NORMALE, width=10,
                                   bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
                                   insertbackground=utils.COULEUR_TEXTE)
        self.champ_mise.pack(side="left", padx=5)
        self.champ_mise.insert(0, "100")

        self.bouton_jouer = tk.Button(
            cadre_bas, text="⚪ LANCER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_ACCENT, fg=utils.COULEUR_TEXTE,
            width=12, height=2, cursor="hand2", command=self.jouer
        )
        self.bouton_jouer.pack(side="left", padx=10)

    def formater_multiplicateurs(self):
        """Retourne une chaîne de texte avec tous les multiplicateurs."""
        textes = []
        for multi in plinko.MULTIPLICATEURS:
            textes.append(f"x{multi}")
        return "  |  ".join(textes)

    def dessiner_grille(self, position_balle=None, etape=None):
        """
        Dessine la grille de clous et la balle (si fournie).

        Paramètres :
        - position_balle : position horizontale actuelle (0 à N)
        - etape : rangée actuelle (pour positionner la balle verticalement)
        """

        # Effacer le canvas
        self.canvas.delete("all")

        # Calculer les positions des clous
        nb_rangees = plinko.NOMBRE_RANGEES
        marge_haut = 30
        marge_gauche = 40
        espacement_horizontal = (LARGEUR_CANVAS - 2 * marge_gauche) / (nb_rangees + 1)
        espacement_vertical = (HAUTEUR_CANVAS - marge_haut - 50) / (nb_rangees + 1)

        # Dessiner les clous
        for rangee in range(nb_rangees):
            nombre_clous_dans_rangee = rangee + 2  # La rangée 0 a 2 clous, la rangée 1 a 3, etc.

            # Centrer les clous horizontalement
            largeur_rangee = (nombre_clous_dans_rangee - 1) * espacement_horizontal
            x_debut = (LARGEUR_CANVAS - largeur_rangee) / 2

            y = marge_haut + (rangee + 1) * espacement_vertical

            for clou_index in range(nombre_clous_dans_rangee):
                x = x_debut + clou_index * espacement_horizontal

                # Dessiner le clou (petit cercle)
                rayon_clou = 4
                self.canvas.create_oval(
                    x - rayon_clou, y - rayon_clou,
                    x + rayon_clou, y + rayon_clou,
                    fill=COULEUR_CLOU, outline=""
                )

        # Dessiner les cases en bas
        nb_cases = nb_rangees + 1
        largeur_case = (LARGEUR_CANVAS - 2 * marge_gauche) / nb_cases
        y_bas = HAUTEUR_CANVAS - 35

        for i in range(nb_cases):
            x_case = marge_gauche + i * largeur_case
            couleur = COULEUR_CASE_ACTIVE if (position_balle is not None and etape is not None and etape >= nb_rangees and i == position_balle) else COULEUR_CASE_NORMALE

            self.canvas.create_rectangle(
                x_case + 2, y_bas,
                x_case + largeur_case - 2, HAUTEUR_CANVAS - 5,
                fill=couleur, outline=utils.COULEUR_FOND
            )

        # Dessiner la balle si en animation
        if position_balle is not None and etape is not None and etape < nb_rangees:
            # Calculer la position X de la balle
            nombre_clous_dans_rangee = etape + 2
            largeur_rangee = (nombre_clous_dans_rangee - 1) * espacement_horizontal
            x_debut_rangee = (LARGEUR_CANVAS - largeur_rangee) / 2

            # La balle est entre deux clous
            x_balle = x_debut_rangee + position_balle * espacement_horizontal
            y_balle = marge_haut + (etape + 1) * espacement_vertical - espacement_vertical / 2

            rayon_balle = 8
            self.canvas.create_oval(
                x_balle - rayon_balle, y_balle - rayon_balle,
                x_balle + rayon_balle, y_balle + rayon_balle,
                fill=COULEUR_BALLE, outline=""
            )

    def jouer(self):
        """Lance une partie de Plinko."""

        if self.animation_en_cours:
            return

        # Vérifier la mise
        valide, resultat = utils.mise_est_valide(self.champ_mise.get(), player.get_argent())
        if not valide:
            messagebox.showerror("Mise invalide", resultat)
            return

        mise = resultat

        # Jouer la partie (calculer le résultat avant l'animation)
        resultat_partie = plinko.jouer_plinko(mise)

        # Déduire la mise
        player.modifier_argent(-mise)
        self.label_argent.config(text=f"Solde : {utils.formater_argent(player.get_argent())}")

        # Désactiver le bouton pendant l'animation
        self.bouton_jouer.config(state="disabled")
        self.champ_mise.config(state="disabled")

        # Lancer l'animation
        self.chemin_balle = resultat_partie['chemin']
        self.etape_animation = 0
        self.animation_en_cours = True
        self.mise_pour_animation = mise
        self.resultat_pour_animation = resultat_partie

        self.label_resultat.config(text="⚪ La balle tombe...", fg=utils.COULEUR_TEXTE)

        # Démarrer l'animation
        self.animer_balle(position_courante=0)

    def animer_balle(self, position_courante):
        """
        Anime la balle étape par étape.
        Appelée récursivement avec un délai pour créer l'animation.
        """

        # Dessiner la balle à l'étape courante
        self.dessiner_grille(position_balle=position_courante, etape=self.etape_animation)

        # Passer à l'étape suivante
        if self.etape_animation < plinko.NOMBRE_RANGEES:
            # Calculer la prochaine position
            direction = self.chemin_balle[self.etape_animation]
            if direction == "D":
                prochaine_position = position_courante + 1
            else:
                prochaine_position = position_courante

            self.etape_animation += 1

            # Rappeler cette fonction après un délai
            self.fenetre.after(
                DELAI_ANIMATION_MS,
                lambda: self.animer_balle(prochaine_position)
            )
        else:
            # Animation terminée : afficher le résultat
            self.fin_animation()

    def fin_animation(self):
        """Appelée quand l'animation est terminée. Affiche le résultat."""

        self.animation_en_cours = False
        resultat = self.resultat_pour_animation
        mise = self.mise_pour_animation

        # Attribuer le gain
        player.modifier_argent(resultat['gain'])
        player.enregistrer_resultat(resultat['victoire'])

        # Afficher le résultat
        if resultat['victoire']:
            profit = resultat['gain'] - mise
            self.label_resultat.config(
                text=f"✅ x{resultat['multiplicateur']} ! Gain : +{utils.formater_argent(profit)}",
                fg=utils.COULEUR_SUCCÈS
            )
        else:
            perte = mise - resultat['gain']
            self.label_resultat.config(
                text=f"❌ x{resultat['multiplicateur']} | Perte : -{utils.formater_argent(perte)}",
                fg=utils.COULEUR_ECHEC
            )

        # Mettre à jour l'argent
        self.label_argent.config(text=f"Solde : {utils.formater_argent(player.get_argent())}")
        self.callback_argent()

        # Réactiver les boutons
        self.bouton_jouer.config(state="normal")
        self.champ_mise.config(state="normal")

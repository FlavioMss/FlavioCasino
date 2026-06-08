"""
ui/dice_ui.py
-------------
Interface graphique du jeu de Dés (Over/Under).
Le joueur choisit une valeur cible et parie AU-DESSUS ou EN-DESSOUS.
"""

import tkinter as tk
from tkinter import messagebox

import player
import utils
from games import dice  # La logique du jeu


class FenetreDice:
    """Interface graphique du jeu de Dés."""

    def __init__(self, fenetre, callback_mise_a_jour_argent):
        self.fenetre = fenetre
        self.callback_argent = callback_mise_a_jour_argent

        # État du jeu
        self.pari_au_dessus = True  # True = AU DESSUS, False = EN DESSOUS
        self.valeur_cible = 50      # Valeur cible par défaut

        # Configuration de la fenêtre
        self.fenetre.title("Casino - Jeu de Dés")
        self.fenetre.geometry("450x580")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du jeu de dés."""

        # Titre
        tk.Label(self.fenetre, text="🎲 JEU DE DÉS",
                 font=utils.POLICE_TITRE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND).pack(pady=10)

        # Solde
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND
        )
        self.label_argent.pack()

        # Grand affichage du résultat du dé
        self.label_resultat_de = tk.Label(
            self.fenetre, text="?",
            font=("Arial", 72, "bold"), fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_resultat_de.pack(pady=10)

        # Message résultat
        self.label_message = tk.Label(
            self.fenetre, text="Choisissez votre pari et misez !",
            font=utils.POLICE_GRANDE, fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_message.pack()

        # ----- VALEUR CIBLE -----
        tk.Label(self.fenetre, text="Valeur cible (5 - 95) :",
                 font=utils.POLICE_NORMALE, fg=utils.COULEUR_TEXTE_SECONDAIRE, bg=utils.COULEUR_FOND).pack(pady=(15, 2))

        # Slider pour la valeur cible
        self.slider_cible = tk.Scale(
            self.fenetre,
            from_=dice.CIBLE_MINIMUM, to=dice.CIBLE_MAXIMUM,
            orient="horizontal", length=300,
            bg=utils.COULEUR_FOND, fg=utils.COULEUR_TEXTE,
            troughcolor=utils.COULEUR_BOUTON,
            highlightthickness=0,
            command=self.maj_affichage_cible  # Appelé à chaque mouvement du slider
        )
        self.slider_cible.set(50)  # Position par défaut : 50
        self.slider_cible.pack()

        # ----- AFFICHAGE PROBABILITÉ ET MULTIPLICATEUR -----
        cadre_info = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_info.pack(pady=5)

        self.label_probabilite = tk.Label(
            cadre_info, text="Probabilité : 50.0%",
            font=utils.POLICE_NORMALE, fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND
        )
        self.label_probabilite.pack(side="left", padx=15)

        self.label_multiplicateur = tk.Label(
            cadre_info, text="Multiplicateur : x1.94",
            font=utils.POLICE_NORMALE, fg=utils.COULEUR_OR, bg=utils.COULEUR_FOND
        )
        self.label_multiplicateur.pack(side="left", padx=15)

        # ----- CHOIX AU DESSUS / EN DESSOUS -----
        tk.Label(self.fenetre, text="Votre pari :",
                 font=utils.POLICE_NORMALE, fg=utils.COULEUR_TEXTE_SECONDAIRE, bg=utils.COULEUR_FOND).pack(pady=(10, 5))

        cadre_pari = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_pari.pack()

        self.bouton_dessus = tk.Button(
            cadre_pari, text="⬆ AU-DESSUS",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_ACCENT, fg=utils.COULEUR_TEXTE,
            width=13, height=2, cursor="hand2",
            command=lambda: self.selectionner_pari(True)
        )
        self.bouton_dessus.pack(side="left", padx=5)

        self.bouton_dessous = tk.Button(
            cadre_pari, text="⬇ EN-DESSOUS",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
            width=13, height=2, cursor="hand2",
            command=lambda: self.selectionner_pari(False)
        )
        self.bouton_dessous.pack(side="left", padx=5)

        # ----- MISE -----
        cadre_mise = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_mise.pack(pady=10)

        tk.Label(cadre_mise, text="Mise :", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND).pack(side="left")

        self.champ_mise = tk.Entry(cadre_mise, font=utils.POLICE_NORMALE, width=10,
                                   bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
                                   insertbackground=utils.COULEUR_TEXTE)
        self.champ_mise.pack(side="left", padx=5)
        self.champ_mise.insert(0, "100")

        # Bouton Jouer
        tk.Button(
            self.fenetre, text="🎲 LANCER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_ACCENT, fg=utils.COULEUR_TEXTE,
            width=18, height=2, cursor="hand2", command=self.jouer
        ).pack(pady=10)

        # Mettre à jour l'affichage initial
        self.maj_affichage_cible(50)

    def selectionner_pari(self, au_dessus):
        """Sélectionne le type de pari : au-dessus ou en-dessous."""
        self.pari_au_dessus = au_dessus

        if au_dessus:
            self.bouton_dessus.config(bg=utils.COULEUR_ACCENT)
            self.bouton_dessous.config(bg=utils.COULEUR_BOUTON)
        else:
            self.bouton_dessus.config(bg=utils.COULEUR_BOUTON)
            self.bouton_dessous.config(bg=utils.COULEUR_ACCENT)

        # Mettre à jour la probabilité et le multiplicateur
        self.maj_affichage_cible(self.slider_cible.get())

    def maj_affichage_cible(self, valeur):
        """
        Met à jour les affichages de probabilité et multiplicateur
        quand le slider ou le pari change.
        """
        valeur_cible = int(valeur)
        self.valeur_cible = valeur_cible

        # Calculer probabilité et multiplicateur
        proba = dice.calculer_probabilite(valeur_cible, self.pari_au_dessus)
        multi = dice.calculer_multiplicateur(valeur_cible, self.pari_au_dessus)

        self.label_probabilite.config(text=f"Probabilité : {proba}%")
        self.label_multiplicateur.config(text=f"Multiplicateur : x{multi}")

    def jouer(self):
        """Lance le dé et détermine le résultat."""

        # Vérifier la mise
        valide, resultat = utils.mise_est_valide(self.champ_mise.get(), player.get_argent())
        if not valide:
            messagebox.showerror("Mise invalide", resultat)
            return

        mise = resultat

        # Lancer le dé
        resultat_de = dice.lancer_de()

        # Vérifier si gagné
        victoire = dice.verifier_resultat(resultat_de, self.valeur_cible, self.pari_au_dessus)

        # Déduire la mise
        player.modifier_argent(-mise)

        # Calculer et attribuer le gain
        if victoire:
            multiplicateur = dice.calculer_multiplicateur(self.valeur_cible, self.pari_au_dessus)
            gain = utils.calculer_gain(mise, multiplicateur)
            player.modifier_argent(gain)
            profit = gain - mise
            self.label_message.config(
                text=f"✅ {resultat_de} ! Vous gagnez +{utils.formater_argent(profit)} !",
                fg=utils.COULEUR_SUCCÈS
            )
        else:
            self.label_message.config(
                text=f"❌ {resultat_de} ! Vous perdez {utils.formater_argent(mise)} !",
                fg=utils.COULEUR_ECHEC
            )

        # Afficher le résultat du dé avec couleur
        couleur_de = utils.COULEUR_SUCCÈS if victoire else utils.COULEUR_ECHEC
        self.label_resultat_de.config(text=str(resultat_de), fg=couleur_de)

        # Enregistrer le résultat
        player.enregistrer_resultat(victoire)

        # Mettre à jour l'argent
        self.label_argent.config(text=f"Solde : {utils.formater_argent(player.get_argent())}")
        self.callback_argent()

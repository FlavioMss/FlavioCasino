import tkinter as tk
from tkinter import messagebox

import player
import utils
from games import blackjack  # La logique du jeu


class FenetreBlackjack:
    """Interface graphique du jeu Blackjack."""

    def __init__(self, fenetre, callback_mise_a_jour_argent):
        self.fenetre = fenetre
        self.callback_argent = callback_mise_a_jour_argent

        # État du jeu
        self.deck = []
        self.main_joueur = []
        self.main_dealer = []
        self.mise_actuelle = 0
        self.partie_en_cours = False

        # Configuration de la fenêtre
        self.fenetre.title("Casino - Blackjack")
        self.fenetre.geometry("550x650")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        self.creer_interface()

    def creer_interface(self):
        """Crée l'interface du Blackjack."""

        # Titre
        tk.Label(
            self.fenetre,
            text="🃏 BLACKJACK",
            font=utils.POLICE_TITRE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        ).pack(pady=10)

        # Solde
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        self.label_argent.pack()

        # ----- CARTES DU DEALER -----
        tk.Label(self.fenetre, text="— DEALER —", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE_SECONDAIRE, bg=utils.COULEUR_FOND).pack(pady=(10, 2))

        self.label_cartes_dealer = tk.Label(
            self.fenetre,
            text="",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE,
            bg=utils.COULEUR_FOND,
            wraplength=500
        )
        self.label_cartes_dealer.pack()

        self.label_score_dealer = tk.Label(
            self.fenetre,
            text="Score : ?",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            bg=utils.COULEUR_FOND
        )
        self.label_score_dealer.pack()

        # ----- MESSAGE CENTRAL -----
        self.label_message = tk.Label(
            self.fenetre,
            text="Entrez votre mise et cliquez sur Démarrer",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_TEXTE,
            bg=utils.COULEUR_FOND,
            wraplength=500
        )
        self.label_message.pack(pady=15)

        # ----- CARTES DU JOUEUR -----
        tk.Label(self.fenetre, text="— VOUS —", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE_SECONDAIRE, bg=utils.COULEUR_FOND).pack(pady=(5, 2))

        self.label_cartes_joueur = tk.Label(
            self.fenetre,
            text="",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE,
            bg=utils.COULEUR_FOND,
            wraplength=500
        )
        self.label_cartes_joueur.pack()

        self.label_score_joueur = tk.Label(
            self.fenetre,
            text="Score : ?",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            bg=utils.COULEUR_FOND
        )
        self.label_score_joueur.pack()

        # ----- MISE -----
        cadre_mise = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_mise.pack(pady=15)

        tk.Label(cadre_mise, text="Mise : ", font=utils.POLICE_NORMALE,
                 fg=utils.COULEUR_TEXTE, bg=utils.COULEUR_FOND).pack(side="left")

        self.champ_mise = tk.Entry(cadre_mise, font=utils.POLICE_NORMALE, width=10,
                                   bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
                                   insertbackground=utils.COULEUR_TEXTE)
        self.champ_mise.pack(side="left")
        self.champ_mise.insert(0, "100")

        # ----- BOUTONS D'ACTION -----
        cadre_boutons = tk.Frame(self.fenetre, bg=utils.COULEUR_FOND)
        cadre_boutons.pack(pady=10)

        self.bouton_demarrer = tk.Button(
            cadre_boutons, text="▶ DÉMARRER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_ACCENT, fg=utils.COULEUR_TEXTE,
            width=12, height=2, cursor="hand2", command=self.demarrer_partie
        )
        self.bouton_demarrer.pack(side="left", padx=5)

        self.bouton_tirer = tk.Button(
            cadre_boutons, text="TIRER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
            width=10, height=2, cursor="hand2", command=self.tirer_carte,
            state="disabled"  # Désactivé au départ
        )
        self.bouton_tirer.pack(side="left", padx=5)

        self.bouton_rester = tk.Button(
            cadre_boutons, text="RESTER",
            font=utils.POLICE_GRANDE, bg=utils.COULEUR_BOUTON, fg=utils.COULEUR_TEXTE,
            width=10, height=2, cursor="hand2", command=self.rester,
            state="disabled"
        )
        self.bouton_rester.pack(side="left", padx=5)

    def demarrer_partie(self):
        """Démarre une nouvelle partie de Blackjack."""

        # Vérifier la mise
        valide, resultat = utils.mise_est_valide(self.champ_mise.get(), player.get_argent())
        if not valide:
            messagebox.showerror("Mise invalide", resultat)
            return

        self.mise_actuelle = resultat

        # Déduire la mise
        player.modifier_argent(-self.mise_actuelle)
        self.mettre_a_jour_label_argent()

        # Créer un nouveau deck et distribuer les cartes
        self.deck = blackjack.creer_deck()
        self.main_joueur = []
        self.main_dealer = []

        # Distribuer 2 cartes à chacun (alternance joueur/dealer)
        self.main_joueur.append(self.deck.pop(0))
        self.main_dealer.append(self.deck.pop(0))
        self.main_joueur.append(self.deck.pop(0))
        self.main_dealer.append(self.deck.pop(0))

        self.partie_en_cours = True

        # Activer les boutons de jeu, désactiver Démarrer
        self.bouton_demarrer.config(state="disabled")
        self.bouton_tirer.config(state="normal")
        self.bouton_rester.config(state="normal")
        self.champ_mise.config(state="disabled")

        # Afficher les cartes (une carte du dealer masquée)
        self.afficher_cartes(cacher_dealer=True)

        # Vérifier si Blackjack immédiat
        if blackjack.est_blackjack(self.main_joueur):
            self.terminer_partie()

    def tirer_carte(self):
        """Le joueur tire une carte."""

        nouvelle_carte = self.deck.pop(0)
        self.main_joueur.append(nouvelle_carte)

        self.afficher_cartes(cacher_dealer=True)

        # Vérifier si le joueur a dépassé 21
        score = blackjack.calculer_score(self.main_joueur)
        if score > 21:
            self.label_message.config(text="💥 Bust ! Vous dépassez 21 !", fg=utils.COULEUR_ECHEC)
            self.terminer_partie()
        elif score == 21:
            # Score parfait : forcer le stand
            self.rester()

    def rester(self):
        """Le joueur reste : le dealer joue."""
        self.terminer_partie()

    def terminer_partie(self):
        """Le dealer joue et on détermine le résultat."""

        self.partie_en_cours = False

        # Le dealer joue ses cartes
        self.main_dealer = blackjack.jouer_dealer(self.deck, self.main_dealer)

        # Afficher toutes les cartes du dealer
        self.afficher_cartes(cacher_dealer=False)

        # Déterminer le résultat
        resultat = blackjack.determiner_resultat(self.main_joueur, self.main_dealer)

        # Calculer le gain selon le résultat
        if resultat == "blackjack":
            gain = self.mise_actuelle * blackjack.MULTIPLICATEUR_BLACKJACK
            player.modifier_argent(gain)
            player.enregistrer_resultat(True)
            self.label_message.config(
                text=f"🎉 BLACKJACK ! Vous gagnez {utils.formater_argent(gain)} !",
                fg=utils.COULEUR_OR
            )

        elif resultat == "victoire":
            gain = self.mise_actuelle * blackjack.MULTIPLICATEUR_VICTOIRE
            player.modifier_argent(gain)
            player.enregistrer_resultat(True)
            profit = gain - self.mise_actuelle
            self.label_message.config(
                text=f"✅ Victoire ! +{utils.formater_argent(profit)}",
                fg=utils.COULEUR_SUCCÈS
            )

        elif resultat == "defaite":
            player.enregistrer_resultat(False)
            self.label_message.config(
                text=f"❌ Défaite ! -{utils.formater_argent(self.mise_actuelle)}",
                fg=utils.COULEUR_ECHEC
            )

        elif resultat == "egalite":
            # Égalité : on rembourse la mise
            player.modifier_argent(self.mise_actuelle)
            self.label_message.config(text="🤝 Égalité ! Mise remboursée.", fg=utils.COULEUR_TEXTE)

        # Mettre à jour l'affichage
        self.mettre_a_jour_label_argent()
        self.callback_argent()

        # Réactiver les boutons
        self.bouton_demarrer.config(state="normal")
        self.bouton_tirer.config(state="disabled")
        self.bouton_rester.config(state="disabled")
        self.champ_mise.config(state="normal")

    def afficher_cartes(self, cacher_dealer):
        """
        Affiche les cartes du joueur et du dealer.

        Paramètre :
        - cacher_dealer : si True, masque la 2ème carte du dealer
        """

        # Afficher les cartes du joueur
        texte_joueur = "  |  ".join([blackjack.afficher_carte(c) for c in self.main_joueur])
        self.label_cartes_joueur.config(text=texte_joueur)
        score_joueur = blackjack.calculer_score(self.main_joueur)
        self.label_score_joueur.config(text=f"Score : {score_joueur}")

        # Afficher les cartes du dealer
        if cacher_dealer and len(self.main_dealer) >= 2:
            # Montrer seulement la première carte
            texte_dealer = blackjack.afficher_carte(self.main_dealer[0]) + "  |  [CACHÉ]"
            self.label_cartes_dealer.config(text=texte_dealer)
            self.label_score_dealer.config(text="Score : ?")
        else:
            texte_dealer = "  |  ".join([blackjack.afficher_carte(c) for c in self.main_dealer])
            self.label_cartes_dealer.config(text=texte_dealer)
            score_dealer = blackjack.calculer_score(self.main_dealer)
            self.label_score_dealer.config(text=f"Score : {score_dealer}")

    def mettre_a_jour_label_argent(self):
        """Met à jour l'affichage du solde."""
        self.label_argent.config(
            text=f"Solde : {utils.formater_argent(player.get_argent())}"
        )

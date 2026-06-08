import tkinter as tk
from tkinter import messagebox

import player
import utils

from ui import blackjack_ui
from ui import coinflip_ui
from ui import mines_ui
from ui import dice_ui
from ui import plinko_ui

class FenetreConnexion:
    def __init__(self, fenetre_principale):
        self.fenetre = fenetre_principale
        self.fenetre.title("FlavioCasino - Connexion")
        self.fenetre.geometry("400x300")
        self.fenetre.configure(bg=utils.COULEUR_FOND)
        self.fenetre.resizable(False, False)

        self.centrer_fenetre(400, 300)

        self.creer_interface()

    def centrer_fenetre(self, largeur, hauteur):
        largeur_ecran = self.fenetre.winfo_screenwidth()
        hauteur_ecran = self.fenetre.winfo_screenheight()
        x = (largeur_ecran - largeur) // 2
        y = (hauteur_ecran - hauteur) // 2
        self.fenetre.geometry(f"{largeur}x{hauteur}+{x}+{y}")

    def creer_interface(self):
        label_titre = tk.Label(
            self.fenetre,
            text="FlavioCasino",
            font=utils.POLICE_TITRE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        label_titre.pack(pady=20)

        label_pseudo = tk.Label(
            self.fenetre,
            text="Entrez votre pseudo :",
            font=utils.POLICE_NORMALE,
            fg=utils.COULEUR_TEXTE,
            bg=utils.COULEUR_FOND
        )
        label_pseudo.pack()

        self.champ_pseudo = tk.Entry(
            self.fenetre,
            font=utils.POLICE_NORMALE,
            width=25,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            insertbackground=utils.COULEUR_TEXTE
        )
        self.champ_pseudo.pack(pady=10)
        self.champ_pseudo.focus()

        bouton_connexion = tk.Button(
            self.fenetre,
            text="Se connecter",
            font=utils.POLICE_NORMALE,
            bg=utils.COULEUR_ACCENT,
            fg=utils.COULEUR_TEXTE,
            width=20,
            cursor="hand2",
            command=self.se_connecter
        )
        bouton_connexion.pack(pady=5)

        bouton_creer = tk.Button(
            self.fenetre,
            text="Créer un compte",
            font=utils.POLICE_NORMALE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=20,
            cursor="hand2",
            command=self.creer_compte
        )
        bouton_creer.pack(pady=5)

        self.champ_pseudo.bind("<Return>", lambda event: self.se_connecter())

    def se_connecter(self):
        pseudo = self.champ_pseudo.get().strip()
        if pseudo == "":
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo !")
            return

        succes = player.connecter_joueur(pseudo)

        if succes:
            self.ouvrir_menu_principal()
        else:
            messagebox.showerror(
                "Joueur introuvable",
                f"Le joueur '{pseudo}' n'existe pas.\nCréez un compte !"
            )

    def creer_compte(self):
        pseudo = self.champ_pseudo.get().strip()
        if pseudo == "":
            messagebox.showerror("Erreur", "Veuillez entrer un pseudo !")
            return
        
        if len(pseudo) < 2:
            messagebox.showerror("Erreur", "Le pseudo doit faire au moins 2 caractères !")
            return

        if len(pseudo) > 20:
            messagebox.showerror("Erreur", "Le pseudo ne peut pas dépasser 20 caractères !")
            return

        succes = player.creer_et_connecter_joueur(pseudo)

        if succes:
            messagebox.showinfo(
                "Compte créé !",
                f"Bienvenue {pseudo} !\nVous commencez avec {utils.formater_argent(1000)} !"
            )
            self.ouvrir_menu_principal()
        else:
            messagebox.showerror(
                "Pseudo déjà pris",
                f"Le pseudo '{pseudo}' est déjà utilisé.\nChoisissez-en un autre !"
            )

    def ouvrir_menu_principal(self):

        for widget in self.fenetre.winfo_children():
            widget.destroy()

        MenuPrincipal(self.fenetre)

class MenuPrincipal:
    def __init__(self, fenetre_principale):

        self.fenetre = fenetre_principale
        self.fenetre.title("FlavioCasino"" - Menu Principal")
        self.fenetre.geometry("500x600")
        self.fenetre.configure(bg=utils.COULEUR_FOND)

        self.creer_interface()

    def creer_interface(self):

        label_titre = tk.Label(
            self.fenetre,
            text="FlavioCasino",
            font=utils.POLICE_TITRE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        label_titre.pack(pady=15)

        pseudo = player.pseudo_joueur_connecte
        self.label_argent = tk.Label(
            self.fenetre,
            text=f"Joueur : {pseudo}  |  Solde : {utils.formater_argent(player.get_argent())}",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        )
        self.label_argent.pack(pady=5)

        tk.Label(self.fenetre, text="─" * 40, fg=utils.COULEUR_ACCENT, bg=utils.COULEUR_FOND).pack()

        tk.Label(
            self.fenetre,
            text="CHOISISSEZ UN JEU",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            bg=utils.COULEUR_FOND
        ).pack(pady=10)

        bouton_blackjack = tk.Button(
            self.fenetre,
            text="🃏  BLACKJACK",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=25,
            height=2,
            cursor="hand2",
            command=self.ouvrir_blackjack
        )
        bouton_blackjack.pack(pady=5)

        bouton_coinflip = tk.Button(
            self.fenetre,
            text="🪙  PILE OU FACE",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=25,
            height=2,
            cursor="hand2",
            command=self.ouvrir_coinflip
        )
        bouton_coinflip.pack(pady=5)

        bouton_mines = tk.Button(
            self.fenetre,
            text="💣  MINES",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=25,
            height=2,
            cursor="hand2",
            command=self.ouvrir_mines
        )
        bouton_mines.pack(pady=5)

        bouton_dice = tk.Button(
            self.fenetre,
            text="🎲  JEU DE DÉS",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=25,
            height=2,
            cursor="hand2",
            command=self.ouvrir_dice
        )
        bouton_dice.pack(pady=5)

        bouton_plinko = tk.Button(
            self.fenetre,
            text="⚪  PLINKO",
            font=utils.POLICE_GRANDE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            width=25,
            height=2,
            cursor="hand2",
            command=self.ouvrir_plinko
        )
        bouton_plinko.pack(pady=5)

        tk.Label(self.fenetre, text="─" * 40, fg=utils.COULEUR_ACCENT, bg=utils.COULEUR_FOND).pack(pady=5)

        bouton_stats = tk.Button(
            self.fenetre,
            text="📊  Mes statistiques",
            font=utils.POLICE_NORMALE,
            bg=utils.COULEUR_FOND_SECONDAIRE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            width=25,
            cursor="hand2",
            command=self.afficher_statistiques
        )
        bouton_stats.pack(pady=3)

        bouton_deconnexion = tk.Button(
            self.fenetre,
            text="🚪  Se déconnecter",
            font=utils.POLICE_NORMALE,
            bg=utils.COULEUR_FOND_SECONDAIRE,
            fg=utils.COULEUR_TEXTE_SECONDAIRE,
            width=25,
            cursor="hand2",
            command=self.se_deconnecter
        )
        bouton_deconnexion.pack(pady=3)

    def mettre_a_jour_argent(self):
        pseudo = player.pseudo_joueur_connecte
        self.label_argent.config(
            text=f"Joueur : {pseudo}  |  Solde : {utils.formater_argent(player.get_argent())}"
        )

    def ouvrir_blackjack(self):
        fenetre_jeu = tk.Toplevel(self.fenetre)
        blackjack_ui.FenetreBlackjack(fenetre_jeu, self.mettre_a_jour_argent)

    def ouvrir_coinflip(self):
        fenetre_jeu = tk.Toplevel(self.fenetre)
        coinflip_ui.FenetreCoinFlip(fenetre_jeu, self.mettre_a_jour_argent)

    def ouvrir_mines(self):
        fenetre_jeu = tk.Toplevel(self.fenetre)
        mines_ui.FenetreMines(fenetre_jeu, self.mettre_a_jour_argent)

    def ouvrir_dice(self):
        fenetre_jeu = tk.Toplevel(self.fenetre)
        dice_ui.FenetreDice(fenetre_jeu, self.mettre_a_jour_argent)

    def ouvrir_plinko(self):
        fenetre_jeu = tk.Toplevel(self.fenetre)
        plinko_ui.FenetrePlinko(fenetre_jeu, self.mettre_a_jour_argent)

    def afficher_statistiques(self):

        stats = player.get_stats()

        if stats is None:
            messagebox.showerror("Erreur", "Impossible de récupérer les statistiques.")
            return

        fenetre_stats = tk.Toplevel(self.fenetre)
        fenetre_stats.title("Mes Statistiques")
        fenetre_stats.geometry("300x350")
        fenetre_stats.configure(bg=utils.COULEUR_FOND)
        fenetre_stats.resizable(False, False)

        tk.Label(
            fenetre_stats,
            text="📊 MES STATISTIQUES",
            font=utils.POLICE_TITRE,
            fg=utils.COULEUR_OR,
            bg=utils.COULEUR_FOND
        ).pack(pady=20)

        infos = [
            ("Pseudo", stats['pseudo']),
            ("Solde actuel", utils.formater_argent(stats['argent'])),
            ("Parties jouées", str(stats['parties_jouees'])),
            ("Victoires", str(stats['victoires'])),
            ("Défaites", str(stats['defaites'])),
        ]

        for nom, valeur in infos:
            ligne = tk.Frame(fenetre_stats, bg=utils.COULEUR_FOND)
            ligne.pack(fill="x", padx=30, pady=3)

            tk.Label(
                ligne,
                text=nom + " :",
                font=utils.POLICE_NORMALE,
                fg=utils.COULEUR_TEXTE_SECONDAIRE,
                bg=utils.COULEUR_FOND,
                width=16,
                anchor="w"
            ).pack(side="left")

            tk.Label(
                ligne,
                text=valeur,
                font=utils.POLICE_NORMALE,
                fg=utils.COULEUR_TEXTE,
                bg=utils.COULEUR_FOND,
                anchor="w"
            ).pack(side="left")

        if stats['parties_jouees'] > 0:
            taux = (stats['victoires'] / stats['parties_jouees']) * 100
            taux_texte = f"{round(taux, 1)}%"
        else:
            taux_texte = "N/A"

        tk.Label(
            fenetre_stats,
            text=f"Taux de victoire : {taux_texte}",
            font=utils.POLICE_GRANDE,
            fg=utils.COULEUR_SUCCÈS,
            bg=utils.COULEUR_FOND
        ).pack(pady=15)

        tk.Button(
            fenetre_stats,
            text="Fermer",
            font=utils.POLICE_NORMALE,
            bg=utils.COULEUR_BOUTON,
            fg=utils.COULEUR_TEXTE,
            command=fenetre_stats.destroy
        ).pack()

    def se_deconnecter(self):
        reponse = messagebox.askyesno(
            "Se déconnecter",
            "Voulez-vous vraiment vous déconnecter ?"
        )

        if reponse:
            player.deconnecter_joueur()

            for widget in self.fenetre.winfo_children():
                widget.destroy()

            FenetreConnexion(self.fenetre)
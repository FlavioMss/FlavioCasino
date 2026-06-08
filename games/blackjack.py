"""
games/blackjack.py
------------------
Ce fichier contient UNIQUEMENT la LOGIQUE du Blackjack.
Pas d'interface graphique ici, seulement les règles du jeu.

RÈGLES IMPLÉMENTÉES :
- Un deck de 52 cartes
- Le joueur tire des cartes ou s'arrête
- Le dealer tire jusqu'à 17
- L'As vaut 11 ou 1 selon le contexte
- Blackjack = 21 avec 2 cartes

COMMENT MODIFIER :
- Pour changer les règles du dealer : modifier jouer_dealer()
- Pour changer la valeur des cartes : modifier VALEURS_CARTES
- Pour changer le multiplicateur de gain : modifier MULTIPLICATEUR_VICTOIRE
"""

import random  # Pour mélanger et tirer des cartes

# ============================================================
# CONFIGURATION - Facile à modifier !
# ============================================================

# Le dealer tire des cartes jusqu'à atteindre ce score minimum
SCORE_MINIMUM_DEALER = 17

# Multiplicateur de gain en cas de victoire (mise x2 = profit de 100%)
MULTIPLICATEUR_VICTOIRE = 2.0

# Multiplicateur en cas de Blackjack (21 avec 2 cartes)
MULTIPLICATEUR_BLACKJACK = 2.5


# ============================================================
# LES CARTES
# ============================================================

# Les 4 couleurs (suites) du jeu
COULEURS_CARTES = ["♠ Pique", "♥ Cœur", "♦ Carreau", "♣ Trèfle"]

# Les noms des cartes
NOMS_CARTES = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]

# La valeur de chaque carte
# L'As (A) est traité spécialement dans calculer_score()
VALEURS_CARTES = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6,
    "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10,   # Valet = 10
    "Q": 10,   # Dame = 10
    "K": 10,   # Roi = 10
    "A": 11    # As = 11 par défaut (peut devenir 1)
}


# ============================================================
# FONCTION : Créer un nouveau deck de 52 cartes
# ============================================================

def creer_deck():
    """
    Crée et mélange un deck de 52 cartes.
    Retourne une liste de cartes (chaque carte = dictionnaire).

    Exemple de carte : {'nom': 'A', 'couleur': '♠ Pique', 'valeur': 11}
    """

    deck = []  # Liste vide qui va contenir toutes les cartes

    # Pour chaque couleur...
    for couleur in COULEURS_CARTES:
        # ...et pour chaque nom de carte...
        for nom in NOMS_CARTES:
            # ...créer une carte et l'ajouter au deck
            carte = {
                'nom': nom,
                'couleur': couleur,
                'valeur': VALEURS_CARTES[nom]
            }
            deck.append(carte)

    # Mélanger le deck aléatoirement
    random.shuffle(deck)

    return deck


# ============================================================
# FONCTION : Calculer le score d'une main
# ============================================================

def calculer_score(main):
    """
    Calcule le score total d'une main de cartes.
    Gère automatiquement l'As (11 ou 1 selon le contexte).

    Paramètre :
    - main : liste de cartes (dictionnaires)

    Retourne : le score total (nombre entier)
    """

    score_total = 0
    nombre_as = 0  # Compter les As pour les gérer séparément

    # Additionner la valeur de chaque carte
    for carte in main:
        score_total = score_total + carte['valeur']

        # Compter les As
        if carte['nom'] == "A":
            nombre_as = nombre_as + 1

    # Si on dépasse 21 et qu'on a des As, les passer de 11 à 1
    while score_total > 21 and nombre_as > 0:
        score_total = score_total - 10  # Réduire l'As de 11 à 1 (différence = 10)
        nombre_as = nombre_as - 1

    return score_total


# ============================================================
# FONCTION : Afficher une carte sous forme de texte
# ============================================================

def afficher_carte(carte):
    """
    Retourne une représentation textuelle d'une carte.
    Exemple : "A ♠ Pique"

    Paramètre :
    - carte : dictionnaire représentant une carte
    """
    return carte['nom'] + " " + carte['couleur']


# ============================================================
# FONCTION : Vérifier si c'est un Blackjack
# ============================================================

def est_blackjack(main):
    """
    Vérifie si une main est un Blackjack (21 avec exactement 2 cartes).

    Paramètre :
    - main : liste de cartes

    Retourne : True si Blackjack, False sinon
    """

    # Il faut exactement 2 cartes et un score de 21
    if len(main) == 2 and calculer_score(main) == 21:
        return True

    return False


# ============================================================
# FONCTION : Jouer le tour du dealer
# ============================================================

def jouer_dealer(deck, main_dealer):
    """
    Le dealer tire des cartes selon les règles :
    - Il tire tant que son score est inférieur à SCORE_MINIMUM_DEALER
    - Il s'arrête quand il atteint ou dépasse SCORE_MINIMUM_DEALER

    Paramètres :
    - deck : le deck de cartes (liste)
    - main_dealer : les cartes actuelles du dealer (liste)

    Retourne : la main finale du dealer
    """

    # Le dealer tire tant qu'il a moins de 17 (ou autre valeur configurée)
    while calculer_score(main_dealer) < SCORE_MINIMUM_DEALER:
        # Prendre la première carte du deck
        nouvelle_carte = deck.pop(0)
        main_dealer.append(nouvelle_carte)

    return main_dealer


# ============================================================
# FONCTION : Déterminer le résultat de la partie
# ============================================================

def determiner_resultat(main_joueur, main_dealer):
    """
    Compare les mains du joueur et du dealer pour déterminer qui gagne.

    Retourne une chaîne de caractères :
    - "blackjack" : le joueur a un Blackjack
    - "victoire"  : le joueur gagne
    - "defaite"   : le joueur perd
    - "egalite"   : match nul

    Paramètres :
    - main_joueur : cartes du joueur
    - main_dealer : cartes du dealer
    """

    score_joueur = calculer_score(main_joueur)
    score_dealer = calculer_score(main_dealer)

    # Vérifier si le joueur a dépassé 21 (bust)
    if score_joueur > 21:
        return "defaite"

    # Vérifier si le joueur a un Blackjack
    if est_blackjack(main_joueur) and not est_blackjack(main_dealer):
        return "blackjack"

    # Vérifier si le dealer a dépassé 21
    if score_dealer > 21:
        return "victoire"

    # Comparer les scores
    if score_joueur > score_dealer:
        return "victoire"
    elif score_joueur < score_dealer:
        return "defaite"
    else:
        return "egalite"

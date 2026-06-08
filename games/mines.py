"""
games/mines.py
--------------
Ce fichier contient la logique du jeu Mines.
Le joueur clique sur des cases en évitant les mines.

RÈGLES :
- Grille 5x5 = 25 cases
- Le joueur choisit un nombre de mines (entre 1 et 24)
- Chaque case révélée sans mine augmente le multiplicateur
- Si le joueur touche une mine : il perd tout
- Le joueur peut "retirer" ses gains à tout moment

COMMENT MODIFIER :
- Pour changer la taille de la grille : TAILLE_GRILLE
- Pour changer les multiplicateurs : calculer_multiplicateur()
"""

import random  # Pour placer les mines aléatoirement

# ============================================================
# CONFIGURATION - Facile à modifier !
# ============================================================

TAILLE_GRILLE = 5           # Grille 5x5 (modifier aussi l'interface si changé)
NOMBRE_CASES_TOTAL = TAILLE_GRILLE * TAILLE_GRILLE  # = 25 cases

# Mines minimum et maximum autorisées
MINES_MINIMUM = 1
MINES_MAXIMUM = NOMBRE_CASES_TOTAL - 1  # Au moins une case safe


# ============================================================
# FONCTION : Créer la grille avec les mines
# ============================================================

def creer_grille(nombre_mines):
    """
    Crée une grille 5x5 et place les mines aléatoirement.
    Retourne une liste de 25 cases (True = mine, False = safe).

    La grille est une liste plate (pas une liste de listes) pour simplifier.
    Index 0 = case (0,0), index 1 = case (0,1), etc.

    Paramètre :
    - nombre_mines : combien de mines à placer
    """

    # Créer une liste de 25 cases sans mines
    grille = [False] * NOMBRE_CASES_TOTAL  # False = pas de mine

    # Choisir des positions aléatoires pour les mines
    positions_mines = random.sample(range(NOMBRE_CASES_TOTAL), nombre_mines)

    # Placer les mines aux positions choisies
    for position in positions_mines:
        grille[position] = True  # True = mine

    return grille


# ============================================================
# FONCTION : Convertir ligne/colonne en index
# ============================================================

def position_vers_index(ligne, colonne):
    """
    Convertit une position (ligne, colonne) en index dans la liste.
    Exemple : ligne=1, colonne=2 -> index=7 (pour une grille 5x5)

    Paramètres :
    - ligne : numéro de ligne (0 à 4)
    - colonne : numéro de colonne (0 à 4)
    """
    return ligne * TAILLE_GRILLE + colonne


# ============================================================
# FONCTION : Vérifier si une case a une mine
# ============================================================

def case_a_mine(grille, ligne, colonne):
    """
    Vérifie si la case à la position (ligne, colonne) a une mine.

    Retourne : True si mine, False si safe
    """
    index = position_vers_index(ligne, colonne)
    return grille[index]


# ============================================================
# FONCTION : Calculer le multiplicateur
# ============================================================

def calculer_multiplicateur(cases_revelees, nombre_mines):
    """
    Calcule le multiplicateur de gain selon le nombre de cases révélées
    et le nombre de mines.

    Paramètres :
    - cases_revelees : combien de cases ont été révélées
    - nombre_mines : combien de mines dans la grille

    Retourne : le multiplicateur (ex: 1.5, 2.0, 3.5...)
    """

    if cases_revelees == 0:
        return 1.0  # Pas encore joué

    # Calculer le nombre de cases sans mines
    cases_safe = NOMBRE_CASES_TOTAL - nombre_mines

    # Bonus de danger : plus il y a de mines, plus c'est risqué
    bonus_danger = 1.0 + (nombre_mines / NOMBRE_CASES_TOTAL)

    # Multiplicateur augmente avec chaque case révélée
    multiplicateur = 1.0
    for i in range(cases_revelees):
        cases_restantes = cases_safe - i
        # Probabilité de survivre à cette case
        probabilite_survie = cases_restantes / (NOMBRE_CASES_TOTAL - i)
        # Augmenter le multiplicateur inversement à la probabilité
        multiplicateur = multiplicateur * (1.0 / probabilite_survie) * 0.97  # 3% house edge

    return round(multiplicateur, 2)


# ============================================================
# FONCTION : Calculer le gain si retrait
# ============================================================

def calculer_gain_retrait(mise, cases_revelees, nombre_mines):
    """
    Calcule le gain si le joueur décide de retirer ses gains maintenant.)
    
    - mise : le montant misé
    - cases_revelees : nombre de cases révélées sans mine
    - nombre_mines : nombre de mines dans la grille

    Retourne : le montant que le joueur reçoit
    """

    multiplicateur = calculer_multiplicateur(cases_revelees, nombre_mines)
    gain = mise * multiplicateur
    return round(gain, 2)

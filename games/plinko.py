"""
games/plinko.py
---------------
Ce fichier contient la logique du jeu Plinko.
Une balle tombe et rebondit aléatoirement pour atterrir dans un casier.

RÈGLES :
- La balle tombe sur 8 rangées de clous
- À chaque clou, la balle va à gauche ou à droite
- La position finale détermine le multiplicateur
- Les cases du milieu sont les moins rentables
- Les cases extrêmes sont les plus rentables

COMMENT MODIFIER :
- Nombre de rangées : NOMBRE_RANGEES
- Multiplicateurs : MULTIPLICATEURS
"""

import random  # Pour simuler les rebonds

# ============================================================
# CONFIGURATION - Facile à modifier !
# ============================================================

# Nombre de rangées de clous (8 = 9 cases possibles en bas)
NOMBRE_RANGEES = 8

# Multiplicateurs pour chaque case (de gauche à droite)
# Avec 8 rangées, il y a 9 cases (0 à 8)
# Les extrêmes ont de gros multiplicateurs, le centre est faible
MULTIPLICATEURS = [10.0, 3.0, 1.5, 0.5, 0.2, 0.5, 1.5, 3.0, 10.0]

# Probabilité d'aller à droite à chaque clou (0.5 = 50%)
PROBABILITE_DROITE = 0.5


# ============================================================
# FONCTION : Simuler la chute de la balle
# ============================================================

def simuler_chute():
    """
    Simule la chute de la balle à travers les rangées de clous.
    Retourne :
    - le chemin de la balle (liste de 'G' et 'D')
    - la position finale (0 à NOMBRE_RANGEES)
    """

    position = 0        # Position horizontale (commence à 0)
    chemin = []         # Liste des directions prises

    # À chaque rangée, la balle va à gauche ou à droite
    for rangee in range(NOMBRE_RANGEES):
        nombre_aleatoire = random.random()

        if nombre_aleatoire < PROBABILITE_DROITE:
            # Aller à droite : position augmente
            position = position + 1
            chemin.append("D")  # D = Droite
        else:
            # Aller à gauche : position ne change pas
            chemin.append("G")  # G = Gauche

    return chemin, position


# ============================================================
# FONCTION : Obtenir le multiplicateur pour une position
# ============================================================

def get_multiplicateur(position):
    """
    Retourne le multiplicateur pour une position finale donnée.

    Paramètre :
    - position : position finale (0 à NOMBRE_RANGEES)

    Retourne : le multiplicateur (float)
    """

    # Vérifier que la position est valide
    if position < 0 or position >= len(MULTIPLICATEURS):
        return 0.0

    return MULTIPLICATEURS[position]


# ============================================================
# FONCTION : Calculer le gain
# ============================================================

def calculer_gain(mise, position):
    """
    Calcule le gain selon la position finale de la balle.

    Paramètres :
    - mise : le montant misé
    - position : position finale (0 à 8)

    Retourne : le montant gagné
    """

    multiplicateur = get_multiplicateur(position)
    gain = mise * multiplicateur
    return round(gain, 2)


# ============================================================
# FONCTION : Jouer une partie complète de Plinko
# ============================================================

def jouer_plinko(mise):
    """
    Joue une partie complète de Plinko.

    Paramètre :
    - mise : le montant misé

    Retourne un dictionnaire avec :
    - chemin : liste de directions ('G' ou 'D')
    - position : position finale
    - multiplicateur : le multiplicateur obtenu
    - gain : le montant gagné
    - victoire : True si gain > mise
    """

    # Simuler la chute
    chemin, position = simuler_chute()

    # Calculer le gain
    multiplicateur = get_multiplicateur(position)
    gain = calculer_gain(mise, position)

    # Déterminer si c'est une victoire (si le joueur récupère plus que sa mise)
    victoire = gain > mise

    resultat = {
        'chemin': chemin,
        'position': position,
        'multiplicateur': multiplicateur,
        'gain': gain,
        'victoire': victoire
    }

    return resultat

"""
games/coinflip.py
-----------------
Ce fichier contient la logique du jeu Pile ou Face.
C'est le jeu le plus simple du casino !

RÈGLES :
- Le joueur choisit Pile ou Face
- On lance la pièce (50/50)
- Si correct : le joueur gagne la mise x MULTIPLICATEUR_VICTOIRE
- Si incorrect : le joueur perd sa mise

COMMENT MODIFIER :
- Pour changer les gains : modifier MULTIPLICATEUR_VICTOIRE
- Pour changer les probabilités : modifier PROBABILITE_PILE (entre 0 et 1)
"""

import random  # Pour simuler le lancer de pièce

# ============================================================
# CONFIGURATION - Facile à modifier !
# ============================================================

# Multiplicateur en cas de victoire (2.0 = on récupère le double)
MULTIPLICATEUR_VICTOIRE = 2.0

# Probabilité d'obtenir PILE (0.5 = 50%, 0.6 = 60%, etc.)
# Garder à 0.5 pour un jeu équitable
PROBABILITE_PILE = 0.5

# Noms des deux côtés de la pièce
NOM_PILE = "PILE"
NOM_FACE = "FACE"


# ============================================================
# FONCTION : Lancer la pièce
# ============================================================

def lancer_piece():
    """
    Simule le lancer d'une pièce.
    Retourne "PILE" ou "FACE" aléatoirement.

    La probabilité d'obtenir PILE est définie par PROBABILITE_PILE.
    """

    # random.random() retourne un nombre entre 0.0 et 1.0
    nombre_aleatoire = random.random()

    if nombre_aleatoire < PROBABILITE_PILE:
        return NOM_PILE
    else:
        return NOM_FACE


# ============================================================
# FONCTION : Vérifier si le joueur a gagné
# ============================================================

def verifier_resultat(choix_joueur, resultat_piece):
    """
    Compare le choix du joueur avec le résultat du lancer.

    Paramètres :
    - choix_joueur : "PILE" ou "FACE"
    - resultat_piece : "PILE" ou "FACE"

    Retourne : True si le joueur a gagné, False sinon
    """

    if choix_joueur == resultat_piece:
        return True  # Le joueur a deviné correctement
    else:
        return False  # Le joueur s'est trompé


# ============================================================
# FONCTION : Calculer le gain
# ============================================================

def calculer_gain(mise, victoire):
    """
    Calcule le gain ou la perte après la partie.

    Si victoire : retourne la mise multipliée par MULTIPLICATEUR_VICTOIRE
    Si défaite : retourne 0 (le joueur perd sa mise)

    Paramètres :
    - mise : le montant misé
    - victoire : True si gagné, False sinon

    Retourne : le montant que le joueur REÇOIT (0 si perdu)
    """

    if victoire:
        gain = mise * MULTIPLICATEUR_VICTOIRE
        return gain
    else:
        return 0  # Perd la mise

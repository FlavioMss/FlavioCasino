"""
games/dice.py
-------------
Ce fichier contient la logique du jeu de Dés (Over/Under).

RÈGLES :
- Un nombre aléatoire entre 0 et 100 est généré
- Le joueur choisit une valeur cible (ex: 70)
- Le joueur parie que le résultat sera AU-DESSUS ou EN-DESSOUS
- Le multiplicateur est calculé selon les probabilités

Exemple :
- Parier AU-DESSUS de 70 = 30% de chances -> multiplicateur élevé
- Parier EN-DESSOUS de 70 = 70% de chances -> multiplicateur faible

COMMENT MODIFIER :
- Plage des nombres : VALEUR_MINIMUM / VALEUR_MAXIMUM
- Commission du casino : COMMISSION_CASINO (réduire pour des meilleurs gains)
"""

import random  # Pour générer le nombre aléatoire

# ============================================================
# CONFIGURATION - Facile à modifier !
# ============================================================

VALEUR_MINIMUM = 0      # Valeur minimale du dé (inclus)
VALEUR_MAXIMUM = 100    # Valeur maximale du dé (inclus)

# Commission du casino (en %) : 3% = on donne 97% de la valeur théorique
# Réduire pour des meilleurs gains pour le joueur
COMMISSION_CASINO = 3.0

# Valeurs cibles minimales et maximales autorisées
# On ne peut pas parier en dessous de 5 ou au dessus de 95
CIBLE_MINIMUM = 5
CIBLE_MAXIMUM = 95


# ============================================================
# FONCTION : Lancer le dé
# ============================================================

def lancer_de():
    """
    Génère un nombre aléatoire entre VALEUR_MINIMUM et VALEUR_MAXIMUM.
    Retourne ce nombre.
    """
    resultat = random.randint(VALEUR_MINIMUM, VALEUR_MAXIMUM)
    return resultat


# ============================================================
# FONCTION : Calculer le multiplicateur
# ============================================================

def calculer_multiplicateur(valeur_cible, pari_au_dessus):
    """
    Calcule le multiplicateur de gain selon la cible et le pari.

    Plus la probabilité est faible, plus le multiplicateur est élevé.

    Formule :
    multiplicateur = (100 / probabilité_en_%) * (1 - commission)

    Paramètres :
    - valeur_cible : le nombre cible choisi par le joueur (ex: 70)
    - pari_au_dessus : True si "au dessus", False si "en dessous"

    Retourne : le multiplicateur (float)
    """

    total_valeurs = VALEUR_MAXIMUM - VALEUR_MINIMUM + 1  # = 101 valeurs (0 à 100)

    if pari_au_dessus:
        # Compter les valeurs STRICTEMENT au-dessus de la cible
        valeurs_gagnantes = VALEUR_MAXIMUM - valeur_cible
    else:
        # Compter les valeurs STRICTEMENT en-dessous de la cible
        valeurs_gagnantes = valeur_cible - VALEUR_MINIMUM

    # Éviter la division par zéro
    if valeurs_gagnantes <= 0:
        return 0.0

    # Calculer la probabilité (entre 0 et 100)
    probabilite = (valeurs_gagnantes / total_valeurs) * 100

    # Calculer le multiplicateur théorique
    multiplicateur_theorique = 100 / probabilite

    # Appliquer la commission du casino
    facteur_commission = 1 - (COMMISSION_CASINO / 100)
    multiplicateur_final = multiplicateur_theorique * facteur_commission

    return round(multiplicateur_final, 2)


# ============================================================
# FONCTION : Calculer la probabilité en %
# ============================================================

def calculer_probabilite(valeur_cible, pari_au_dessus):
    """
    Calcule et retourne la probabilité de gagner en pourcentage.
    Utilisé pour afficher "Vous avez X% de chances de gagner".

    Paramètres :
    - valeur_cible : le nombre cible
    - pari_au_dessus : True si "au dessus", False si "en dessous"

    Retourne : probabilité en % (float entre 0 et 100)
    """

    total_valeurs = VALEUR_MAXIMUM - VALEUR_MINIMUM + 1

    if pari_au_dessus:
        valeurs_gagnantes = VALEUR_MAXIMUM - valeur_cible
    else:
        valeurs_gagnantes = valeur_cible - VALEUR_MINIMUM

    probabilite = (valeurs_gagnantes / total_valeurs) * 100
    return round(probabilite, 1)


# ============================================================
# FONCTION : Vérifier si le joueur a gagné
# ============================================================

def verifier_resultat(resultat_de, valeur_cible, pari_au_dessus):
    """
    Vérifie si le joueur a gagné selon le résultat du dé.

    Paramètres :
    - resultat_de : le nombre sorti (0 à 100)
    - valeur_cible : la cible du joueur
    - pari_au_dessus : True = pari au dessus, False = pari en dessous

    Retourne : True si gagné, False si perdu
    """

    if pari_au_dessus:
        # Le joueur gagne si le résultat est STRICTEMENT AU-DESSUS de la cible
        return resultat_de > valeur_cible
    else:
        # Le joueur gagne si le résultat est STRICTEMENT EN-DESSOUS de la cible
        return resultat_de < valeur_cible

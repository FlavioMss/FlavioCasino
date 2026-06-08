SYMBOLE_DEVISE = "€"

def formater_argent(montant):
    montant_arrondi = round(montant, 2)

    if montant_arrondi == int(montant_arrondi):
        texte = str(int(montant_arrondi))
    else:
        texte = str(montant_arrondi)

    return texte + " " + SYMBOLE_DEVISE

def mise_est_valide(texte_mise, argent_disponible):
    if texte_mise.strip() == "":
        return False, "Veuillez entrer une mise !"

    try:
        montant = float(texte_mise)
    except ValueError:
        return False, "La mise doit être un nombre !"

    if montant <= 0:
        return False, "La mise doit être supérieure à 0 !"

    if montant < 1:
        return False, "La mise minimum est 1 €"

    if montant > argent_disponible:
        return False, "Vous n'avez pas assez d'argent !"

    return True, montant

def calculer_gain(mise, multiplicateur):

    gain = mise * multiplicateur
    gain_arrondi = round(gain, 2)
    return gain_arrondi

COULEUR_FOND = "#1a1a2e"          # Fond principal (bleu très foncé)
COULEUR_FOND_SECONDAIRE = "#16213e"  # Fond secondaire
COULEUR_ACCENT = "#e94560"         # Couleur d'accent (rouge)
COULEUR_TEXTE = "#ffffff"          # Texte principal (blanc)
COULEUR_TEXTE_SECONDAIRE = "#aaaaaa"  # Texte secondaire (gris)
COULEUR_SUCCÈS = "#4ecca3"         # Vert pour les victoires
COULEUR_ECHEC = "#e94560"          # Rouge pour les défaites
COULEUR_OR = "#f5a623"             # Or pour l'argent
COULEUR_BOUTON = "#0f3460"         # Fond des boutons
COULEUR_BOUTON_HOVER = "#e94560"   # Bouton survolé

# Taille de la police
POLICE_TITRE = ("Arial", 20, "bold")
POLICE_NORMALE = ("Arial", 12)
POLICE_GRANDE = ("Arial", 14)
POLICE_PETITE = ("Arial", 10)

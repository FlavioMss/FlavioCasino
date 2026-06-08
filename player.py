import database  
pseudo_joueur_connecte = None   
argent_joueur_connecte = 0      


def connecter_joueur(pseudo):
    global pseudo_joueur_connecte, argent_joueur_connecte

    joueur = database.recuperer_joueur(pseudo)

    if joueur is None:
        return False

    pseudo_joueur_connecte = joueur['pseudo']
    argent_joueur_connecte = joueur['argent']

    return True


def creer_et_connecter_joueur(pseudo):
    global pseudo_joueur_connecte, argent_joueur_connecte

   
    succes = database.creer_joueur(pseudo)

    if not succes:
        return False
    
    connecter_joueur(pseudo)

    return True

def get_argent():

    return argent_joueur_connecte

def modifier_argent(montant):

    global argent_joueur_connecte

    argent_joueur_connecte = argent_joueur_connecte + montant

    if argent_joueur_connecte < 0:
        argent_joueur_connecte = 0

    database.mettre_a_jour_argent(pseudo_joueur_connecte, argent_joueur_connecte)

def enregistrer_resultat(victoire):

    database.enregistrer_resultat(pseudo_joueur_connecte, victoire)


def get_stats():
    return database.recuperer_joueur(pseudo_joueur_connecte)

def deconnecter_joueur():
    global pseudo_joueur_connecte, argent_joueur_connecte

    pseudo_joueur_connecte = None
    argent_joueur_connecte = 0

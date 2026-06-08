
import sqlite3
import os
CHEMIN_BASE_DE_DONNEES = "database/casino.db"

ARGENT_DE_DEPART = 1000

def initialiser_base_de_donnees():
    if not os.path.exists("database"):
        os.makedirs("database")

    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)

    curseur = connexion.cursor()

    curseur.execute("""
        CREATE TABLE IF NOT EXISTS joueurs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pseudo TEXT NOT NULL UNIQUE,
            argent REAL NOT NULL,
            parties_jouees INTEGER NOT NULL DEFAULT 0,
            victoires INTEGER NOT NULL DEFAULT 0,
            defaites INTEGER NOT NULL DEFAULT 0
        )
    """)

    connexion.commit()

    connexion.close()

    print("Base de données initialisée avec succès !")

def creer_joueur(pseudo):
    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    curseur = connexion.cursor()

    try:
        curseur.execute("""
            INSERT INTO joueurs (pseudo, argent, parties_jouees, victoires, defaites)
            VALUES (?, ?, 0, 0, 0)
        """, (pseudo, ARGENT_DE_DEPART))

        connexion.commit()
        connexion.close()
        return True

    except sqlite3.IntegrityError:
        connexion.close()
        return False

def recuperer_joueur(pseudo):
    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT id, pseudo, argent, parties_jouees, victoires, defaites
        FROM joueurs
        WHERE pseudo = ?
    """, (pseudo,))

    ligne = curseur.fetchone()
    connexion.close()

    if ligne is None:
        return None

    joueur = {
        'id': ligne[0],
        'pseudo': ligne[1],
        'argent': ligne[2],
        'parties_jouees': ligne[3],
        'victoires': ligne[4],
        'defaites': ligne[5]
    }

    return joueur

def mettre_a_jour_argent(pseudo, nouvel_argent):
    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    curseur = connexion.cursor()

    curseur.execute("""
        UPDATE joueurs
        SET argent = ?
        WHERE pseudo = ?
    """, (nouvel_argent, pseudo))

    connexion.commit()
    connexion.close()

def enregistrer_resultat(pseudo, victoire):
    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    curseur = connexion.cursor()

    if victoire:
        curseur.execute("""
            UPDATE joueurs
            SET parties_jouees = parties_jouees + 1,
                victoires = victoires + 1
            WHERE pseudo = ?
        """, (pseudo,))
    else:
        curseur.execute("""
            UPDATE joueurs
            SET parties_jouees = parties_jouees + 1,
                defaites = defaites + 1
            WHERE pseudo = ?
        """, (pseudo,))

    connexion.commit()
    connexion.close()

def recuperer_tous_les_joueurs():
    connexion = sqlite3.connect(CHEMIN_BASE_DE_DONNEES)
    curseur = connexion.cursor()

    curseur.execute("""
        SELECT pseudo, argent, parties_jouees, victoires, defaites
        FROM joueurs
        ORDER BY argent DESC
    """)

    toutes_les_lignes = curseur.fetchall()
    connexion.close()

    liste_joueurs = []
    for ligne in toutes_les_lignes:
        joueur = {
            'pseudo': ligne[0],
            'argent': ligne[1],
            'parties_jouees': ligne[2],
            'victoires': ligne[3],
            'defaites': ligne[4]
        }
        liste_joueurs.append(joueur)

    return liste_joueurs
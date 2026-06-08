import tkinter as tk

import database
from ui import menu


def lancer_application():

    print("=== Démarrage du Casino Python ===")
    print("Initialisation de la base de données...")
    database.initialiser_base_de_donnees()

    print("Création de la fenêtre principale...")
    fenetre_principale = tk.Tk()

    menu.FenetreConnexion(fenetre_principale)

    print("Application lancée ! En attente des actions utilisateur...")
    fenetre_principale.mainloop()

    print("=== Casino Python fermé ===")

if __name__ == "__main__":
    lancer_application()

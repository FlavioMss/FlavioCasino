[README.md](https://github.com/user-attachments/files/28693632/README.md)
# 🎰 Casino Python

Projet de casino en Python avec interface graphique Tkinter et base de données SQLite.  
Développé dans un objectif **pédagogique** : code simple, commenté, facile à modifier et à présenter.

---

## 🎮 Jeux disponibles

| Jeu | Description |
|-----|-------------|
| 🃏 **Blackjack** | Joueur contre dealer — cartes visuelles, tirer / rester |
| 🪙 **Pile ou Face** | Pari simple 50/50 avec multiplicateur x2 |
| 💣 **Mines** | Grille 5×5, évitez les mines, retirez vos gains quand vous voulez |
| 🎲 **Jeu de Dés** | Over / Under — slider de 0 à 100, cotes calculées en temps réel |
| ⚪ **Plinko** | Balle animée, multiplicateurs de x0.2 à x10 |

---

## 📁 Structure du projet

```
casino_project/
│
├── main.py              ← Point d'entrée — lancer ce fichier
├── database.py          ← Toutes les requêtes SQLite
├── player.py            ← État du joueur en session
├── utils.py             ← Couleurs, formatage, validation des mises
│
├── games/
│   ├── blackjack.py     ← Logique : deck, scores, As, règles dealer
│   ├── coinflip.py      ← Logique : lancer de pièce, probabilités
│   ├── mines.py         ← Logique : grille, multiplicateurs progressifs
│   ├── dice.py          ← Logique : over/under, calcul des cotes
│   └── plinko.py        ← Logique : simulation de chute, multiplicateurs
│
├── ui/
│   ├── menu.py          ← Écran de connexion + menu principal + stats
│   ├── blackjack_ui.py  ← Interface cartes visuelles, tirer / rester
│   ├── coinflip_ui.py   ← Interface pile / face
│   ├── mines_ui.py      ← Grille 5×5 cliquable + bouton retrait
│   ├── dice_ui.py       ← Slider cible + choix dessus / dessous
│   └── plinko_ui.py     ← Animation balle sur Canvas Tkinter
│
└── database/
    └── casino.db        ← Base SQLite (créée automatiquement au premier lancement)
```

---

## 🚀 Installation et lancement

### Prérequis

- **Python 3.8 ou supérieur**
- Tkinter (inclus par défaut avec Python sur Windows et macOS)
- Aucune dépendance externe à installer

> Sur **Linux**, si Tkinter n'est pas présent :
> ```bash
> sudo apt install python3-tk
> ```

### Vérifier que Python est installé

```bash
python --version
# ou
python3 --version
```

Si Python n'est pas installé, téléchargez-le sur [python.org](https://www.python.org/downloads/).  
Cochez bien **"Add Python to PATH"** lors de l'installation sur Windows.

### Cloner le projet

```bash
git clone https://github.com/votre-utilisateur/casino-python.git
cd casino-python
```

### Lancer le casino

```bash
python main.py
```

> La base de données `database/casino.db` est créée automatiquement au premier lancement.  
> Aucune autre commande n't est nécessaire.

---

## 🗄️ Accéder à la base de données

La base de données est un fichier **SQLite** : `database/casino.db`.  
Il existe plusieurs façons de la consulter et de la modifier.

---

### Option 1 — Interface graphique : DB Browser for SQLite ⭐ (recommandé)

C'est l'outil le plus simple pour visualiser et modifier la base sans écrire de SQL.

1. Téléchargez **DB Browser for SQLite** : [sqlitebrowser.org](https://sqlitebrowser.org/dl/)
2. Installez-le et ouvrez-le
3. Cliquez sur **"Ouvrir une base de données"**
4. Naviguez jusqu'à `casino_project/database/casino.db`

Vous pouvez alors :
- **Parcourir les données** → onglet "Parcourir les données", sélectionnez la table `joueurs`
- **Modifier une valeur** → double-cliquez sur une cellule, modifiez, cliquez "Écrire les modifications"
- **Exécuter du SQL** → onglet "Exécuter le SQL"

![DB Browser Screenshot](https://sqlitebrowser.org/images/screenshot.png)

---

### Option 2 — Terminal SQLite (ligne de commande)

SQLite est intégré dans Python, donc pas besoin d'installer quoi que ce soit.

#### Ouvrir la base depuis Python

```bash
cd casino_project
python3 -c "import sqlite3; conn = sqlite3.connect('database/casino.db'); conn.execute('.help')"
```

#### Ou utiliser l'outil sqlite3 s'il est installé sur votre système

```bash
sqlite3 database/casino.db
```

Une fois dans le shell SQLite (invite `sqlite>`), voici les commandes utiles :

```sql
-- Afficher toutes les tables
.tables

-- Afficher la structure de la table joueurs
.schema joueurs

-- Afficher tous les joueurs
SELECT * FROM joueurs;

-- Afficher les joueurs triés par argent (classement)
SELECT pseudo, argent, victoires, defaites
FROM joueurs
ORDER BY argent DESC;

-- Quitter
.quit
```

---

### Option 3 — Script Python intégré

Vous pouvez interroger la base directement depuis Python sans outil externe :

```bash
cd casino_project
python3
```

```python
import sqlite3

# Connexion à la base
conn = sqlite3.connect("database/casino.db")
cur  = conn.cursor()

# Voir tous les joueurs
cur.execute("SELECT * FROM joueurs")
for ligne in cur.fetchall():
    print(ligne)

conn.close()
```

---

## 🛠️ Commandes SQL utiles

Voici les requêtes SQL les plus courantes pour administrer le casino.  
Elles peuvent être exécutées dans DB Browser, dans le terminal sqlite3, ou via Python.

### Consulter les données

```sql
-- Tous les joueurs
SELECT * FROM joueurs;

-- Classement par richesse
SELECT pseudo, argent FROM joueurs ORDER BY argent DESC;

-- Joueurs avec le meilleur taux de victoire
SELECT pseudo, victoires, parties_jouees,
       ROUND(CAST(victoires AS REAL) / parties_jouees * 100, 1) AS taux_victoire
FROM joueurs
WHERE parties_jouees > 0
ORDER BY taux_victoire DESC;
```

### Modifier un joueur

```sql
-- Donner de l'argent à un joueur
UPDATE joueurs SET argent = 5000 WHERE pseudo = 'Alice';

-- Remettre à zéro les stats d'un joueur
UPDATE joueurs
SET parties_jouees = 0, victoires = 0, defaites = 0
WHERE pseudo = 'Alice';

-- Remettre l'argent de départ à tout le monde
UPDATE joueurs SET argent = 1000;
```

### Ajouter / supprimer des joueurs

```sql
-- Ajouter un joueur manuellement
INSERT INTO joueurs (pseudo, argent, parties_jouees, victoires, defaites)
VALUES ('NouveauJoueur', 1000, 0, 0, 0);

-- Supprimer un joueur
DELETE FROM joueurs WHERE pseudo = 'Alice';

-- Supprimer TOUS les joueurs (remettre à zéro)
DELETE FROM joueurs;
```

### Inspecter la structure

```sql
-- Structure de la table
PRAGMA table_info(joueurs);

-- Nombre total de joueurs
SELECT COUNT(*) FROM joueurs;

-- Argent total en circulation
SELECT SUM(argent) FROM joueurs;
```

---

## ⚙️ Modifier les règles du jeu

Toutes les constantes importantes sont en haut de chaque fichier, faciles à trouver.

| Ce que vous voulez changer | Fichier à modifier | Variable |
|---|---|---|
| Argent de départ | `database.py` | `ARGENT_DE_DEPART` |
| Gain Blackjack | `games/blackjack.py` | `MULTIPLICATEUR_BLACKJACK` |
| Gain Pile ou Face | `games/coinflip.py` | `MULTIPLICATEUR_VICTOIRE` |
| Nombre de rangées Plinko | `games/plinko.py` | `NOMBRE_RANGEES` |
| Multiplicateurs Plinko | `games/plinko.py` | `MULTIPLICATEURS` |
| Commission casino (dés) | `games/dice.py` | `COMMISSION_CASINO` |
| Taille de la grille Mines | `games/mines.py` | `TAILLE_GRILLE` |
| Vitesse animation Plinko | `ui/plinko_ui.py` | `DELAI_ANIMATION_MS` |
| Couleurs de l'interface | `utils.py` | `COULEUR_*` |

---

## 🧱 Technologies utilisées

- **Python 3** — langage principal
- **Tkinter** — interface graphique (inclus dans Python)
- **SQLite** — base de données (inclus dans Python)

Aucune installation de bibliothèque externe requise.

---

## 📄 Licence

Projet libre — utilisez, modifiez et partagez librement.

# **Tournament Manager v1.0.0**

Organisez votre tournoi d'échecs avec Tournament Manager ! (Gestion des paires suivant le système suisse)

Cette application vous offre la possibilité de:
- Gérer une liste de participants ainsi que leurs classements
- Créer un tournoi suivant vos propres critères d'organisation (Type de jeu, nombre de tour, nombre de joueurs)
- Afficher les résultats simplement et rapidement

Toutes les données seront enregistrées au format .JSON afin de sauvegarder votre progression du tournoi !
 
## **Prérequis**

Ce projet est développé avec la version de Python 3.9, il est par conséquent recommandé d'installer cette version avant de continuer.


## **Initialisation de l'environnement**

### 1. Cloner la branche Main vers un répertoire local

- Créer un dossier sur votre ordinateur pour y disposer les fichiers présents sous GitHub

- Ouvrir un terminal (Ex: Windows PowerShell) et se positionner dans le dossier en question avec la commande cd, par exemple:

```
cd d:
cd -- "D:\mon_dossier"
```

### 2. Créer un environnement virtuel et installer les librairies à l'aide du fichier requirements.txt

- Créer l'environnement:


`python -m venv tournament`

- Activer l'nvironnement (L'environnement est activé une fois son nom affiché dans le terminal) : 

    - Windows:

    `tournament/Scripts/Activate.ps1` 

    - Inux et MacOS:  

    `source tournament/bin/activate`

- Installer les librairies : 

`pip install -r requirements.txt`


## **Lancement du projet**

### 1. Lancer le programme main.py sous l'environnement virtuel, dans le terminal:

`py main.py`

### 2. Patienter jusqu'à l'affichage du menu d'accueil

- 1 participants :
```
    1. Afficher la liste des participants
    2. Ajouter un participant
    3. Mettre à jour le classement
```
- 2 Tournois :
```
    1. Afficher la liste des tournois
    2. Créer un tournoi
    3. Continuer un tournoi
```
Lorsqu'un tournoi vient d'être créé, il est nécessaire de sélectionner "Continuer un tournoi" afin de charger ce dernier.

- 2.2 Gestion du tournoi :
```
    1. Résumé du tournoi
    2. Afficher la liste des joueurs
    3. Ajouter un joeur
    4. Supprimer un joueur
    5. Afficher le round en cours
    6. Round suivant
    7. Saisir le résultat d'un match
    8. Classement du tournoi
    9. Cloturer le tournoi
    10. Modifier le tournoi
```
Dans le cas où votre tournoi ne posséderait pas encore de joueurs, seules les sélections 1, 2, 3, 4 et 10 seront visibles.(Don't panic!)

- 3 Reporting :
```
    1. Liste des participants par ordre alphabétique 
    2. Liste des participants par classement 
    3. Liste de tous les tournois
    4. Liste des joueurs d'un tournoi par ordre alphabétique
    5. Liste des joueurs d'un tournoi par classement
    6. Liste de tous les tours / matchs d'un tournoi
    7. Afficher le classement d'un tournoi
```

Pour revenir au menu précédant ou quitter l'application:
`999`

## **Enregistrement des fichiers :**

les données sont stockées au format JSON à la racine du projet:

- actors.json : L'intégralité des participants
- tournaments.json : L'intégralité des tournois


## **Flake8-HTML Report :**

Flake8 est paramétré suivant les critères suivants :
```
exclude = .gitignore, actors.json, tournament.json, requierements.txt, .git, venv, tournament, __pycache__, __init__.py
max-line-length = 119
format = html
htmldir = flake-report
```

Ces critères sont disponibles dans le fichier ".flake8" à la racine du projet.

### Exécution
- Ouvrir un terminal (Ex: Windows PowerShell) et se positionner à la racine du projet à l'aide de la commande "cd".

- Dans le terminal:
    `flake8`

- Le reporting HTML sera disponible dans le dossier "flake-report" au nom de "index.html"


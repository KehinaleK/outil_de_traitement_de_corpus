from pathlib import Path
import csv

"""
Ce programme permet de récupérer l'ensemble des contenus des fichiers texte obtenus avec retrieval.py
et de les stocker dans les colonnes d'un fichier csv. Ce fichier csv est stocké dans le dossier data/train.
"""


def tableau(dossier):
    """
    Création d'un tableau à 2 colonnes.
    Paramètre : 
    dossier(Path): nom du dossier contenant nos fichiers texte.
    """

    liste_textes = []
    liste_personnages = []

    listes_fichiers = sorted(dossier.glob("*.txt"))
    print(listes_fichiers)

    for fichier in listes_fichiers:
        texte = fichier.name
        index = texte.find("(")
        personnage = texte[:index].replace("%27","'")
        liste_personnages.append(personnage)

    for fichier in listes_fichiers:
        with open(fichier, "r", encoding="utf8") as f:
            texte = f.read()
            liste_textes.append(texte.strip())
    

    with open("../data/train/donnees.csv", "w") as fichier:
        structure = csv.writer(fichier, delimiter=',', quotechar='"', 
                               quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["nom", "texte"])
        for nom, texte in zip(liste_personnages, liste_textes):
            structure.writerow([nom, texte])


tableau(dossier=Path("../urls"))




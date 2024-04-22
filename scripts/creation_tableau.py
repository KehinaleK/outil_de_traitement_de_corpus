from pathlib import Path
import csv

def tableau(dossier):
    

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
    

    with open("../data/clean/donnees.csv", "w") as fichier:
        structure = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["nom", "texte"])
        for nom, texte in zip(liste_personnages, liste_textes):
            structure.writerow([nom, texte])


tableau(dossier=Path("../urls"))
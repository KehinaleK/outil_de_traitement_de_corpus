# OUTIL DE TRAITEMENT DE CORPUS

Ce dépôt contient l'ensemble des fichiers utilisés pour le cours d'outil de traitement de corpus. La tâche choisie est une tâche de question/réponse dont le corpus d'entraînement concerne les personnages (héros uniquement !) de l'univers DC Comics. Les données ont été obtenues à partir des pages individuelles des personnages sur le site [DC Database]((https://dc.fandom.com/wiki/DC_Comics_Database)). La dataset est également disponible sur [Hugging Face.](https://huggingface.co/datasets/Kkarmin/dc_comics_qa) Le journal vous offre une description plus détaillée du projet et de ses différentes étapes. 

## STRUCTURE DU DÉPÔT 

### dataset_card.yml

Le document `dataset_card.yml` contient la carte de présentation de la dataset et respecte la structure proposée par le site HuggingFace.

### README.md

Le fichier `README` offre tous les pré-requis et commandes nécessaires au lancement des programmes contenus dans le dépôt.

### journal.md

Le fichier `journal.md` contient une explication détaillée des scripts, des étapes du projet et des données recueillies. 

### Dossier data/

Le dossier `data` contient trois sous dossiers :
- raw :
    Contient l'ensemble des fichiers txt obtenus à partir du scrapping.
- clean :
    Contient le document tabulaire regroupant l'ensemble des contenus des fichiers txt et l'annotation manuelle des questions/réponses. Ce document (`donnees.csv`) sera celui utilisé pour l'entraînement.
- stats :
    Contient deux fichiers tabulaires basés sur celui de data/clean. Le premier est enrichi à l'aide d'une analyse morpho-syntaxique (`donnees_analysees.csv`) et le second est enrichi de colonnes supplémentaires utilisées pour les enquêtes statistiques (`donnees_stats.csv`).

### Dossier figures/

Le dossier `figures` contient l'ensemble des graphiques réalisés dans le cadre de l'enquête statistique au sujet des données du corpus.

### Dossier img/

Le dossier `img` contient l'ensemble des images utilisées pour l'illustration de la composition du corpus expliquée dans le journal.

### Dossier scripts/

Le dossier `scripts` contient l'ensemble des scripts utilisés pour l'analyse morpho-syntaxique (`analyse.py`) et statistique (`statistiques.py` et `datastructures.py`) du corpus.

### Dossier src/

Le dossier `src` contient l'ensemble des scripts utilisés pour l'extraction et l'obtention du corpus. `retrieval.py` contient la logique de scrapping. `creation_tableau.py` permet d'obtenir le fichier d'entrainement tabulaire et `split.py` divise le corpus pour l'entraînement. 


## README

Veillez à avoir une version de python compatible avec les différentes librairies utilisées. 

### DOSSIER SRC : COMPOSITION DU CORPUS

#### RETRIEVAL.PY

Le script `retrieval.py` ne prend aucun argument et permet d'obtenir des fichiers `txt` contenant nos 'contextes' dans le dossier `data/raw`.

La commande à utiliser est la suivante : 

```python3 retrieval.py```

Prérequis : 

Veillez à avoir les libraires Bs4 (Beautiful Soup) et requests pour le bon fonctionnement du programme. Veillez également à prévoir un temps de traitement très long (4h à 5h dépendamment des essais réalisés.)

#### CREATION_TABLEAU.PY

Le script `creation_tableau.py` permet d'obtenir une représentation tabulaire des contextes obtenus précedemment. 

La commande à utiliser est la suivante : 

```python3 creation_tableau.py ../data/raw```

Prérequis :

Veillez à avoir la libraire csv bien installée. Veillez également à avoir un corpus de fichiers texte dans le dossier `data/raw` obtenus avec `retrieval.py` pour bien obtenir votre fichier de sortie. 

### DOSSIER SCRIPTS : ANALYSE LINGUISTIQUE ET STATISTIQUES DU CORPUS

#### STATISTIQUES.PY

Le programme `statistiques.py` permet d'obtenir différentes représentations graphiques de données conernant notre corpus.

Le programme dispose du gestionnaire d'argument suivant : 

```
parser = argparse.ArgumentParser(description="Choix des graphiques devant être crées")
parser.add_argument('type', choices=['question_type', 'question_type_yes_no', 'reponse_type', 'taille', 'fréquence'], help= "Choix du graphique désiré")
args = parser.parse_args()
```
- `question_type` permet d'obtenir le nombre de questions par type (en fonction des mots interrogatifs).
    
    Exemple : ```python3 statistiques.py --type question_type```

 - `question_type_yes_no` permet d'obtenir le nombre de questions par type (en fonction des questions yes/no ou ouvertes).
    
    Exemple : ```python3 statistiques.py --type question_type_yes_no```

 - `reponse_type` permet d'obtenir le nombre de reponses par type.
    
    Exemple : ```python3 statistiques.py --type reponse_type```

 - `taille` permet d'obtenir le nombre moyen de mots par colonne (contexte, question, réponse).
    
    Exemple : ```python3 statistiques.py --type taille```

 - `fréquence` permet d'obtenir les mots les plus fréquents de chaque colonne (contexte, question, réponse).
    
    Exemple : ```python3 statistiques.py --type fréquence```

- `corrélation` permet d'obtenir les correlation et p-values entre les longueurs des variables contextes/question, contextes/réponses et questions/réponses.

    Exemple : ```python3 statistiques.py --type correlation```


Prérequis :

Veuillez à avoir le fichier `datastructures.py` avec la classe suivante : 

```
@dataclass
class Hero: 
    name: str
    context: str
    question: str
    answer: str
    where: bool
    when: bool
    who: bool
    what: bool
    how: bool
    why: bool
    how_many: bool
    yes_no: bool
    complete: bool
    partial: bool
    short: bool
    complement_info: bool
    copy: bool
    open_question: bool

```
Veillez à importer la classe. Veillez également à avoir les libraires pandas, matplotlib, datastructures, argparse et wordcloud installées.
Veillez également à avoir le fichier `donnees_stats.csv` rempli et conforme.

#### ANALYSE.PY

Le programme `analyse.py` permet d'obtenir un nouveau fichier csv (dans le dossier `stats` du dossier `data`) contenant les contextes, questions et réponses analysés morpho-syntaxiquement.

La commande à utiliser est : 

```python3 analyse.py```

Prérequis :

Veillez à avoir les librairies pandas, spacy et csv installées. Veillez également à bien avoir un fichier `donnees.csv` pouvant être analysé.

#### SPLIT.PY 

Le programme `split.py` permet de diviser notre corpus en des ensemble d'entrainement, test et validation. 

La commande à utiliser est : 

```python3 split.py```

Prérequis :
Veillez à avoir les librairies nltk et scikitlearn bien installées. Veillez également à bien avoir un fichier `donnees.csv` pouvant être split.




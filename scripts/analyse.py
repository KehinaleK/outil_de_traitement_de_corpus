import pandas as pd # Pour obtenir la dataframe de donnees.csv
import datasets # Pour obtenir la dataset
from datasets import Dataset # Pour obtenir la dataset
import spacy # Pour analyser les textes
import csv # Pour créer un fichier csv

"""
Ce programme permet d'analyser morpho-syntaxiquement les contextes, questions et réponses de notre corpus.
Les trois colonnes sont analysées sont ensuite stockées dans une fichier donnees_analysees.csv.
"""

def extraction_donnees():
    """
    Cette fonction permet d'attribuer de créer des listes des contenus de chacune de nos colonnes.

    Returns:
    liste_textes(List(str)): liste des contextes.
    liste_questions(List(str)): liste des questions.
    liste_reponses(List(str)): liste des réponses.
    """
    corpus_dataframe = pd.read_csv('../data/train/donnees.csv', header=0)
    dataset = Dataset.from_pandas(corpus_dataframe)
    
    liste_textes = []
    liste_questions = []
    liste_reponses = []

    for index, ligne in corpus_dataframe.iterrows():
        cellule_texte = ligne.context
        liste_textes.append(cellule_texte)
        cellule_question = ligne.question
        liste_questions.append(cellule_question)
        celulle_reponse = ligne.answer
        liste_reponses.append(celulle_reponse)

    return liste_textes, liste_questions, liste_reponses


def analyse(liste_textes, liste_questions, liste_reponses):
    """
    Cette fonction permet d'analyser chaque élément de nos listes contextes, questions et réponses.
    Nous récupérons chaque forme, pos et lemme pour tous les éléments.
    Ces analyses sont sauvegardées dans une fichier csv nommé donnees_analysees.csv

    Paramètres :
    liste_textes(List(str)): liste des contextes.
    liste_questions(List(str)): liste des questions.
    liste_reponses(List(str)): liste des réponses.

    """

    nlp = spacy.load("en_core_web_sm")

    textes_analyses = []
    for texte in liste_textes:
        texte_analyse =  []
        doc = nlp(texte)
        for token in doc:
            forme = token.text
            pos = token.pos_
            lemme = token.lemma_
            texte_analyse.append((forme,pos,lemme))
        textes_analyses.append(texte_analyse)

    questions_analysees = []
    for question in liste_questions:
        question_analyse = []
        doc = nlp(question)
        for token in doc:
            forme = token.text
            pos = token.pos_
            lemme = token.lemma_
            question_analyse.append((forme,pos,lemme))
        questions_analysees.append(question_analyse)

    reponses_analysees = []
    for reponse in liste_reponses:
        reponse_analyse = []
        doc = nlp(reponse)
        for token in doc:
            forme = token.text
            pos = token.pos_
            lemme = token.lemma_
            reponse_analyse.append((forme,pos,lemme))
        reponses_analysees.append(reponse_analyse)

    # Création du fichier
    with open("../data/stats/donnees_analysees.csv", "w") as fichier:
        structure = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["texte_analyse", "question_analyse", "reponse_analyse"])
        for texte, question, reponse in zip(textes_analyses, questions_analysees, reponses_analysees):
            structure.writerow([texte, question, reponse])
             

def main():

    liste_textes, liste_questions, liste_reponses = extraction_donnees()
    analyse(liste_textes, liste_questions, liste_reponses)

main()
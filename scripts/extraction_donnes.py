import pandas as pd
import datasets
from datasets import Dataset
import spacy
import csv

def extraction_donnees():

    corpus_dataframe = pd.read_csv('../data/clean/donnees.csv', header=0)
    dataset = Dataset.from_pandas(corpus_dataframe)
    
    liste_textes = []
    liste_questions = []
    liste_reponses = []

    for index, ligne in corpus_dataframe.iterrows():
        cellule_texte = ligne.texte
        liste_textes.append(cellule_texte)
        cellule_question = ligne.question
        liste_questions.append(cellule_question)
        celulle_reponse = ligne.reponse
        liste_reponses.append(celulle_reponse)

    print(liste_reponses)
    return liste_textes, liste_questions, liste_reponses


def analyse(liste_textes, liste_questions, liste_reponses):

    nlp = spacy.load("en_core_web_sm")

    textes_analyses = []
    for texte in liste_textes:
        doc = nlp(texte)
        for token in doc:
            forme = token.text
            pos = token.pos
            lemme = token.lemma
            textes_analyses.append((forme,pos,lemme))

    questions_analysees = []
    for question in liste_questions:
        print(question)
        doc = nlp(question)
        for token in doc:
            forme = token.text
            pos = token.pos
            lemme = token.lemma
            questions_analysees.append((forme,pos,lemme))

    reponses_analysees = []
    for reponse in liste_reponses:
        doc = nlp(reponse)
        for token in doc:
            forme = token.text
            pos = token.pos
            lemme = token.lemma
            reponses_analysees.append((forme,pos,lemme))


    with open("../data/clean/donnees_analysees.csv", "w") as fichier:
        structure = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["texte_analyse", "question_analyse", "reponse_analyse"])
        for texte, question, reponse in zip(textes_analyses, questions_analysees, reponses_analysees):
            structure.writerow([texte, question, reponse])
             

def main():

    liste_textes, liste_questions, liste_reponses = extraction_donnees()
    analyse(liste_textes, liste_questions, liste_reponses)

main()
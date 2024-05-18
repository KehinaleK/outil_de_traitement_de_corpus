import pandas as pd
import datasets
from datasets import Dataset
import spacy
import csv

def extraction_donnees():

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

    #print(textes_analyses)
    with open("../data/stats/donnees_analysees.csv", "w") as fichier:
        structure = csv.writer(fichier, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        structure.writerow(["texte_analyse", "question_analyse", "reponse_analyse"])
        for texte, question, reponse in zip(textes_analyses, questions_analysees, reponses_analysees):
            structure.writerow([texte, question, reponse])
             

def main():

    liste_textes, liste_questions, liste_reponses = extraction_donnees()
    analyse(liste_textes, liste_questions, liste_reponses)

main()
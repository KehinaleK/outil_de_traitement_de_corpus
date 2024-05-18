import pandas as pd
import matplotlib.pyplot as plt
import datastructures
import argparse
from wordcloud import WordCloud
from scipy.stats import pearsonr


def get_table():

    
    tableau = pd.read_csv("../data/stats/donnees_stats.csv")
    colonnes = tableau[["name", "context", "question", "answer", "where", "when", "who", "what", "how", "why", "how_many", "yes/no", 
                        "complete", "partial", "short", "complement_info", "copy", "open_question"]]
    return colonnes

def get_heros(colonnes):

     
    lignes_necessaires = colonnes[0:231]
    liste_heros = []
    for index, ligne in lignes_necessaires.iterrows():
        name = ligne["name"]
        context = ligne["context"]
        question = ligne["question"]
        answer = ligne["answer"]
        where = ligne["where"]
        when = ligne["when"]
        who = ligne["who"]
        what = ligne["what"]
        how = ligne["how"]
        why = ligne["why"]
        how_many = ligne["how_many"]
        yes_no = ligne["yes/no"]
        complete = ligne["complete"]
        partial = ligne["partial"]
        short = ligne["short"]
        complement_info = ligne["complement_info"]
        copy = ligne["copy"]
        open_question = ligne["open_question"]
        hero = datastructures.Hero(name = name, context = context, question = question, 
                                   answer = answer, where = where, when = when, who = who, 
                                   what = what, how = how, why = why, how_many = how_many,
                                   yes_no = yes_no, complete = complete, partial = partial,
                                   short = short, complement_info = complement_info, copy = copy, open_question = open_question)
         
        liste_heros.append(hero)
   
    return liste_heros

def types_questions(liste_heros):

    nbr_where = 0
    nbr_when = 0
    nbr_who = 0
    nbr_what = 0
    nbr_how = 0
    nbr_why = 0
    nbr_how_many = 0
    nbr_yes_no = 0
    nbr_open = 0
    
    for hero in liste_heros:     
      
        if hero.where == 1:
            nbr_where += 1
        if hero.when ==1: 
            nbr_when += 1   
        if hero.who == 1:
            nbr_who += 1
        if hero.what == 1:
            nbr_what += 1
        if hero.how == 1:
            nbr_how += 1
        if hero.why == 1:
            nbr_why += 1 
        if hero.how_many == 1: 
            nbr_how_many += 1
        if hero.yes_no == 1: 
            nbr_yes_no += 1
        if hero.open_question == 1: 
            nbr_open += 1

    return nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many, nbr_yes_no, nbr_open


def type_reponses(liste_heros):

    nbr_complete = 0
    nbr_partial = 0
    nbr_short = 0
    nbr_complement_info = 0
    nbr_copy = 0
    
    for hero in liste_heros:     
      
        if hero.complete == 1:
            nbr_complete += 1
        if hero.partial ==1: 
            nbr_partial += 1   
        if hero.short == 1:
            nbr_short += 1
        if hero.complement_info == 1:
            nbr_complement_info += 1
        if hero.copy == 1:
            nbr_copy += 1

    return nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy


def tailles(liste_heros):

    nbr_lignes = 0
    taille_contexte = 0
    taille_question = 0
    taille_reponse = 0
    mots_contexte = []
    mots_question = []
    mots_reponse = []
    taille_contextes = []
    taille_questions = []
    tailles_reponses = []

    for hero in liste_heros: 
        nbr_lignes += 1
        liste_contexte = (hero.context).split(" ")
        liste_question = (hero.question).split(" ")
        liste_reponse = (hero.answer).split(" ")

        taille_contexte += len(liste_contexte)
        taille_question += len(liste_question)
        taille_reponse += len(liste_reponse)

        taille_contextes.append(len(liste_contexte))
        taille_questions.append(len(liste_question))
        tailles_reponses.append(len(liste_reponse))

        mots_contexte.extend(liste_contexte)
        mots_question.extend(liste_question)
        mots_reponse.extend(liste_reponse)

    moyenne_contexte = taille_contexte/nbr_lignes
    moyenne_question = taille_question/nbr_lignes
    moyenne_reponse = taille_reponse/nbr_lignes
    
    ratio_reponse_question = moyenne_reponse/moyenne_question
    ratio_question_reponse = moyenne_question/moyenne_reponse


    return moyenne_contexte, moyenne_question, moyenne_reponse, ratio_question_reponse, ratio_reponse_question, mots_contexte, mots_question, mots_reponse, taille_contextes, taille_questions, tailles_reponses

def plot_taille(moyenne_contexte, moyenne_question, moyenne_reponse):
     
    bar_width = 0.25
    indices = range(len([moyenne_contexte, moyenne_question, moyenne_reponse]))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, [moyenne_contexte, moyenne_question, moyenne_reponse], 
            color=['pink', 'mediumpurple', 'lightskyblue'], width=bar_width, edgecolor='grey')
    plt.xlabel('Colonne', fontweight='bold', fontsize=15)

    plt.ylabel('Nombre moyen de mots', fontweight='bold', fontsize=15)
    plt.ylim(0,80)
    plt.title('Nombre moyen de mots en fonction de la colonne')
    plt.xticks(indices, ['Contexte', 'Questions', 'Réponses'], rotation=30)
    plt.show()



def plot_frequence(colonne, titre):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(colonne))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(titre, fontweight='bold', fontsize=15)
    plt.axis('off')
    plt.show()


def plot_types_questions(nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many):
    
    bar_width = 0.25
    indices = range(len([nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many]))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, [nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many], 
            color=['tomato', 'pink', 'mediumpurple', 'lightskyblue', 'lightgreen', 'gold', 'coral'], width=bar_width, edgecolor='grey')
    plt.xlabel('Type de question', fontweight='bold', fontsize=15)

    plt.ylabel('Nombre de questions', fontweight='bold', fontsize=15)
    plt.ylim(0,80)
    plt.title('Nombre de questions en fonction de leurs types')
    plt.xticks(indices, ['Where', 'When', 'Who', 'What', 'How', 'Why', 'How many'], rotation=30)
    plt.show()

def plot_types_questions_yes_no(nbr_yes_no, nbr_open):
    
    bar_width = 0.25
    indices = range(len([nbr_yes_no, nbr_open]))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, [nbr_yes_no, nbr_open], 
            color=['mediumpurple', 'lightskyblue'], width=bar_width, edgecolor='grey')
    plt.xlabel('Type de question', fontweight='bold', fontsize=15)

    plt.ylabel('Nombre de questions', fontweight='bold', fontsize=15)
    plt.ylim(0,100)
    plt.title('Nombre de questions en fonction de leurs types')
    plt.xticks(indices, ['Yes/No', 'Open'], rotation=30)
    plt.show()


def plot_types_reponses(nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy):
    
    bar_width = 0.25
    indices = range(len([nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy]))

    plt.figure(figsize=(12, 6))
    plt.bar(indices, [nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy], 
            color=['pink', 'mediumpurple', 'lightskyblue', 'lightgreen', 'gold'], width=bar_width, edgecolor='grey')
    plt.xlabel('Type de réponses', fontweight='bold', fontsize=15)

    plt.ylabel('Nombre de réponses', fontweight='bold', fontsize=15)
    plt.ylim(0,230)
    plt.title('Nombre de réponses en fonction de leurs types')
    plt.xticks(indices, ['Reprise complète', 'Reprise partielle', 'Réponse courte', 'Réponses avec info(s) supplémentaire(s)', 'Copie du contexte'], rotation=30)
    plt.show()


def main():

    parser = argparse.ArgumentParser(description="Choix des graphiques devant être crées")
    parser.add_argument('type', choices=['question_type', 'question_type_yes_no', 'reponse_type', 'taille', 'fréquence', 'correlation'], help= "Choix du graphique désiré")
    args = parser.parse_args()

    colonnes = get_table()
    liste_heros = get_heros(colonnes)

    if args.type == "question_type":
        nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many, nbr_yes_no, nbr_open = types_questions(liste_heros)
        print(f"where = {nbr_where}, when = {nbr_when}, who = {nbr_who}, what = {nbr_what}, how = {nbr_how}, why = {nbr_why}, how many = {nbr_how_many}")
        plot_types_questions(nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many)
    elif args.type == "question_type_yes_no":
        nbr_where, nbr_when, nbr_who, nbr_what, nbr_how, nbr_why, nbr_how_many, nbr_yes_no, nbr_open = types_questions(liste_heros)
        print(f"yes no = {nbr_yes_no}, open = {nbr_open}")
        plot_types_questions_yes_no(nbr_yes_no, nbr_open)
    elif args.type == "reponse_type":
        nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy = type_reponses(liste_heros)
        print(f"complete = {nbr_complete}, partial = {nbr_partial}, short = {nbr_short}, complement info = {nbr_complement_info}, copy = {nbr_copy}")
        plot_types_reponses(nbr_complete, nbr_partial, nbr_short, nbr_complement_info, nbr_copy)
    elif args.type == "taille":
        moyenne_contexte, moyenne_question, moyenne_reponse, ratio_question_reponse, ratio_reponse_question, mots_contexte, mots_question, mots_reponse, taille_contextes, taille_questions, taille_reponses  = tailles(liste_heros)
        print(f"contexte = {moyenne_contexte}, question = {moyenne_question}, reponse = {moyenne_reponse}, ratio question réponse = {ratio_question_reponse}, ratio réponse question = {ratio_reponse_question}")
        plot_taille(moyenne_contexte, moyenne_question, moyenne_reponse)
    elif args.type == "fréquence":
        moyenne_contexte, moyenne_question, moyenne_reponse, ratio_question_reponse, ratio_reponse_question, mots_contexte, mots_question, mots_reponse, taille_contextes, taille_questions, taille_reponses  = tailles(liste_heros)
        plot_frequence(mots_contexte, "Mots les plus fréquents des contextes")
        plot_frequence(mots_question, "Mots les plus fréquents des questions")
        plot_frequence(mots_reponse, "Mots les plus fréquents des réponses")
    elif args.type == "correlation":
        moyenne_contexte, moyenne_question, moyenne_reponse, ratio_question_reponse, ratio_reponse_question, mots_contexte, mots_question, mots_reponse, taille_contextes, taille_questions, taille_reponses = tailles(liste_heros)
        longueurs_contextes = [context for context in taille_contextes]
        longueurs_questions = [question for question in taille_questions]
        longueurs_reponses = [reponse for reponse in taille_reponses]

        print(len(longueurs_questions))
        print(len(longueurs_contextes))
        print(len(longueurs_reponses))


        corr_contexte_question, p_value_contexte_question = pearsonr(longueurs_contextes, longueurs_questions)
        corr_contexte_reponse, p_value_contexte_reponse = pearsonr(longueurs_contextes, longueurs_reponses)
        corr_question_reponse, p_value_question_reponse = pearsonr(longueurs_questions, longueurs_reponses)
        print(f"Coeff context-question = {corr_contexte_question}, p-value = {p_value_contexte_question}")
        print(f"Coeff context-reponse = {corr_contexte_reponse}, p-value = {p_value_contexte_reponse}")
        print(f"Coeff question-reponse = {corr_question_reponse}, p-value = {p_value_question_reponse}")




if __name__ == "__main__":
    main()
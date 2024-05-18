from dataclasses import dataclass # Pour utiliser les dataclasses

"""
Le classe Hero contient l'ensemble des instances utilisées pour décrire
nos liges et les types de questions/réponses. Cette classe est utilisée 
pour l'analyse statistique de nos données dans le script statistiques.py. 
"""

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

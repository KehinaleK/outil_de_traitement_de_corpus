import pandas as pd # Pour obtenir la dataframe du fichier
from sklearn.model_selection import train_test_split # Pour split le corpus ! 
import nltk  # Pour isoler les stop words
from nltk.corpus import stopwords # Peut être retiré 
nltk.download('stopwords')


def entrainement():
    """
    Cette fonction permet de diviser notre corpus en un ensemble d'entraînement (70%),
    un ensemble de test (15%) et de validation (15%). 
    """

    # english_stop_words = stopwords.words('english')
    # Peut être ajouté pour l'entrainement mais éventuellement
    # retirer des mots interrogatifs ! 

    corpus_dataframe = pd.read_csv('../data/clean/donnees.csv', header=0, usecols=[1,2,3], names=['context','question','answer'])
    train_set, validation_test_set = train_test_split(corpus_dataframe, test_size=0.3, random_state=42)
    validation_set, test_set =  train_test_split(validation_test_set, test_size=0.5, random_state=42)

    print(train_set)
    print(validation_set)
    print(test_set)
    
entrainement()
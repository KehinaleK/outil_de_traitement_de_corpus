import pandas as pd
from sklearn.model_selection import train_test_split
import nltk 
from nltk.corpus import stopwords
nltk.download('stopwords')


def entrainement():


    french_stop_words = stopwords.words('french')
    french_stop_words.remove("pas")
    

    corpus_dataframe = pd.read_csv('../data/train/donnees.csv', header=0, usecols=[1,2,3], names=['context','question','answer'])
    train_set, validation_test_set = train_test_split(corpus_dataframe, test_size=0.3, random_state=42)
    validation_set, test_set =  train_test_split(validation_test_set, test_size=0.5, random_state=42)

    print(train_set)
    print(validation_set)
    print(test_set)
    
entrainement()
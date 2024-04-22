from bs4 import BeautifulSoup
import requests

# Le site choisi est https://dc.fandom.com/wiki/DC_Comics_Database.
# Cette page est une page d'accueil, la page desirée se trouve ailleurs sur le site (contient la liste de toutes les pages de tous les personnages).
# Nous commençons par obtenir le content de la page d'accueil. 




def get_homepage():

    homepage_url = 'https://dc.fandom.com/wiki/DC_Comics_Database'
    homepage = requests.get(homepage_url)
    # Retourne un objet "réponse", genre "200" (on espère)
    page_donnees = BeautifulSoup(homepage.content, 'lxml')

    return page_donnees # On retourne le contenu de la page d'acceuil

# On va maintenant pouvoir aller chercher la page qui nous intéresse
# Cette page se trouve en haut de la page d'acceuil 

def get_page_donnees(page_donnees):

    balise_page_donnees = page_donnees.find('a', href = "https://dc.fandom.com/wiki/Category:Good_Characters")
    lien_page_donnees = balise_page_donnees['href']
    reponse_page_donnnes = requests.get(lien_page_donnees)
    content = BeautifulSoup(reponse_page_donnnes.content, 'lxml')

    print(content)
    return content # On return le contenu de la page qui va nous servir pour le scraping
    
def extraction_texte():
    test_url = 'https://dc.fandom.com/wiki/Batman_(Bruce_Wayne)'
    page = requests.get(test_url)
    page_content = BeautifulSoup(page.content, 'lxml')

    texte = page_content.find('div', class_='mw-parser-output')

    for table in texte.find_all('table', class_='navbox'):
        table.extract()
    for quote in texte.find_all('div', class_='quote'):
        quote.extract()
    for sommaire in texte.find_all('div', id='toc'):
        sommaire.extract()
    for aside in texte.find_all('aside'):
        aside.extract()

    texte_full = []
    for element in texte.find_all(['p', 'h1', 'h2', 'h3', 'li']):  
        if element.name == 'h2' and element.get('id') == 'Notes-Header':
            break
        texte_full.append(element.text.strip())

    texte_propre = ' '.join(texte_full)

    with open("test.txt", "w", encoding="utf8") as fichier:
        fichier.write(texte_propre)

extraction_texte()

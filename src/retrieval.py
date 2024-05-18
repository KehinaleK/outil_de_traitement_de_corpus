from bs4 import BeautifulSoup
import requests

""" 
Ce programme permet d'effectuer un web-scrapping permettant de parcourir l'ensemble des pages individuelles
de personnages de la section "Heroes" du site DC-Databse. Le lien de départ utilisé pour le scrapping est :
https://dc.fandom.com/wiki/DC_Comics_Database'
Ce programme permet d'extraire une courte description des personnages répondant à certaines conditions
et de les stocker dans le dossier "urls" sous format de fichiers txt individuels. 
"""

### POUR LE DÉBUT DU SCRAPPING ###
def get_homepage():
    """
    Retourne le contenu de la page d'accueil du site. 
    """

    homepage_url = 'https://dc.fandom.com/wiki/DC_Comics_Database'
    homepage = requests.get(homepage_url)
    # Retourne un objet "réponse", "200" (on espère).
    page_donnees = BeautifulSoup(homepage.content, 'lxml')

    return page_donnees # Nous retournons le contenu de la page d'acceuil

def get_url_initial(page_donnees):
    """
    Retourne le lien de la première page de la catégorie "heroes".
    """

    balise_page_donnees = page_donnees.find('a', 
                        href = "https://dc.fandom.com/wiki/Category:Good_Characters")
    url_page_initiale = balise_page_donnees['href']

    return url_page_initiale


### POUR LE DÉROULEMENT DU SCRAPPING ###
def get_content_page(url):
    """
    Permet de récupérer le contenu d'une page listant des personnages.

    Paramètre :
    url (str) : URL de la page web concernée.

    Returns :
    content (BeautifulSoup) : contenu de la page web concernée.
    """
    reponse_page_donnnes = requests.get(url)
    content = BeautifulSoup(reponse_page_donnnes.content, 'lxml')
    return content # On return le contenu de la page !

def get_liens_page(content):
    """
    Permet de récupérer une liste de tous les liens menant à
    des pages individuelles de personnages.

    Paramètre :
    content (BeautifulSoup): contenu de la page web concernée.

    Returns :
    liste_liens (List[str]): liste de tous les liens menant à 
    des pahes individuelles de personnages.
    """
    liste_liens = []
    for element in content.descendants:
        if element.name == "div":
            if 'category-page__member-left' in element.get("class", []):
                lien = element.find("a")
                if lien is not None:
                    lien_lien = lien.get("href")
                    liste_liens.append(lien_lien)
    
    return liste_liens

def extraction_texte(liste_liens):
    """
    Permet d'extraire le contenu textuel désiré de chaque page individuelle.
    Sauvegarde chaque contenu dans un fichier txt nommé d'après le personnage concerrné. 

    Paramètre : 
    liste_liens (List[str]): liste de tous les liens menant à 
    des pahes individuelles de personnages.

    Return :
    compteur(int): nombre de liens parcourus.
    """

    compteur = 0
    for lien in liste_liens:
        compteur += 1 
        racine = lien[6:]
        url = f"https://dc.fandom.com{lien}"
        page = requests.get(url)
        page_content = BeautifulSoup(page.content, 'lxml')

        texte = page_content.find('div', class_='mw-parser-output')

        for table in texte.find_all('table', class_='navbox'):
            table.extract()
        for quote in texte.find_all('div', class_='quote'):
            quote.extract()
        for aside in texte.find_all('aside'):
            aside.extract()

        sommaire = texte.find("div", id="toc") 
        if sommaire: # Je trouve le sommaire
            description = sommaire.find_previous_sibling() # je prend l'élément d'avant
            if description.name == 'p': # Si cet élément est un paragraphe alors j'ai ma description
                description_texte = description.get_text()
            else: # Sinon, je continue à remonter jusqu'à trouver le paragraphe
                while description.name != 'p':
                    description = description.find_previous_sibling()

                description_texte = description.get_text()

            description_mot = description_texte.split(" ")
            if len(description_mot) > 50:
                print(f"Ajout : {racine}")
                with open(f"../bin/{racine}.txt", "w", encoding="utf8") as fichier:
                    fichier.write(description_texte)
            else:
                print(f"Trop court : {racine}")
        else:
            print(f"Pas de sommaire trouvé pour : {racine}")

    return compteur
        ## Je ne prends que les fichiers ayant un sommaire ou ayant une description supérieure (très environs) à 3 phrases.

def get_prochaine_page(content):
    """
    Cette fontion permet d'obtenir le lien de la prochaine page contenant les liens de pages individuelles de chaque personnage.
    
    Paramètre :
    content(Beautiful Soup): contenu de la page listant les liens.

    Returns :
    lien_next_page(str): lien de la prochaine page contenant des liens de personnages.
    None: si aucun bouton "NEXT" n'est trouvé.
    """

    for element in content.descendants:
        if element.name == "span" and element.text == "Next":
            for element in content.descendants:
                if element.name == "a":
                    if "category-page__pagination-next" in element.get("class", []):
                        lien_prochaine_page = element["href"]
                        print(lien_prochaine_page)
                        return lien_prochaine_page
            
        
    return None # Si il n'y a pas le bouton "Next" alors on retourne None pour finir la boucle du programme ! 

def main():

    homepage = get_homepage()
    url = get_url_initial(homepage)
    compteur_total = 0

    while url != None:
        content = get_content_page(url)
        liste_liens = get_liens_page(content)
        compteur = extraction_texte(liste_liens)
        compteur_total += compteur
        url = get_prochaine_page(content)
        print(f"Extraction des liens de la page {url} en cours !")
    print(compteur_total)

if __name__ == "__main__":
    main()



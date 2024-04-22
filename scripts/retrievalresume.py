from bs4 import BeautifulSoup
import requests

# Le site choisi est https://dc.fandom.com/wiki/DC_Comics_Database.
# Cette page est une page d'accueil, la page desirée se trouve ailleurs sur le site (contient la liste de toutes les pages de tous les personnages).
# Nous commençons par obtenir le content de la page d'accueil. 



### FONCTION POUR OBTENIR PAGE D'ACCUEIL ###
def get_homepage():

    homepage_url = 'https://dc.fandom.com/wiki/DC_Comics_Database'
    homepage = requests.get(homepage_url)
    # Retourne un objet "réponse", genre "200" (on espère)
    page_donnees = BeautifulSoup(homepage.content, 'lxml')

    return page_donnees # On retourne le contenu de la page d'acceuil

# On va maintenant pouvoir aller chercher la page qui nous intéresse
# Cette page se trouve en haut de la page d'acceuil 

### FONCTION POUR OBTENIR LA PAGE SUR LAQUELLE NOUS ALLONS COMMENCER LE SCRAPPING ###
def get_url_initial(page_donnees):

    balise_page_donnees = page_donnees.find('a', href = "https://dc.fandom.com/wiki/Category:Good_Characters")
    url_page_initiale = balise_page_donnees['href']

    return url_page_initiale


### FONCTION POUR OBTENIR LE CONTENU DE CHAQUE PAGE ###
def get_content_page(url):

    reponse_page_donnnes = requests.get(url)
    content = BeautifulSoup(reponse_page_donnnes.content, 'lxml')
    return content # On return le contenu de la page !

### FONCTION POUR OBTENIR TOUS LES LIENS DE CHAQUE PAGE ###
def get_liens_page(content):

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

    ## J'ai décidé d'uniquement prendre les descriptions en haut des pages wiki
    ## Autrement choisir une seule section était beaucoup trop arbitraire
    ## Et aurait demandé un traitement pour chaque lien
    ## Ces descriptions sont soit avant le sommaire ou après une citation
    ## Comme toutes les pages ont un sommaire (mais pas une citation), je me base dessus pour extraire la description.
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
                with open(f"../urls/{racine}.txt", "w", encoding="utf8") as fichier:
                    fichier.write(description_texte)
            else:
                print(f"Trop court : {racine}")
        else:
            print(f"Pas de sommaire trouvé pour : {racine}")

    return compteur
        ## Je ne prends que les fichiers ayant un sommaire ou ayant une description supérieure (très environs) à 3 phrases.

def get_prochaine_page(content):


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
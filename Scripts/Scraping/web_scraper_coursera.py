from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Firefox()  # Assurez-vous que le chemin de ChromeDriver est dans le PATH

# Ouvrir la page cible
driver.get("https://www.coursera.org")  # Remplacez par l'URL de la page contenant les cartes produit

# Attendre un peu que la page charge (ajuster le temps si nécessaire)
time.sleep(3)  # Attendre 3 secondes

# Effacer et entrer le texte
def flatten(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten(item))  # Recursive call for nested lists
        else:
            flat_list.append(item)
    return flat_list
def search_course(course_name:str):
    search_input = driver.find_element(By.ID, "search-autocomplete-input")
    search_input.clear()
    search_input.send_keys(course_name + Keys.ENTER)
    # Utiliser BeautifulSoup pour analyser le HTML de la page
    time.sleep(4)
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Trouver tous les éléments li contenant les informations sur les cours
    cours_list = soup.find_all('li', class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90')
    formateurs = []
    liens = []
    images = []
    ratings = []
    titres = []
    # Extraire les informations souhaitées
    for cours in cours_list:
        title = cours.find('h3', class_='cds-CommonCard-title css-6ecy9b')
        image = cours.find('img')
        rating = cours.find('span', class_='css-6ecy9b')
        organisme = cours.find('p', class_='css-vac8rf')
        link = cours.find('a', href=True)  # Trouver le lien (attribut href)
        titres.append(title.get_text() if title else 'Non trouvé')
        liens.append(link['href'] if link else 'Non trouvé')
        ratings.append(rating.get_text() if rating else 'Non trouvé')
        formateurs.append(organisme.get_text() if organisme else 'Non trouvé')
        images.append(image['src'] if image else 'Non trouvé')
        # Afficher les informations extraites
        
    return {
            'titres' : titres,
            'liens' : liens,
            'ratings' : ratings,
            'images' : images,
            'formateurs' : formateurs
        }  
def main():
    ids = []
    domaines = []
    sous_domaines = []
    nom_formations = []
    formateurs = []
    liens = []
    images = []
    ratings = []
    titres = []
    course = pd.read_csv("other_files/SEFORMER_FORMATIONS_PAS_DE_FORMATEURS.csv")
    i=0
    try:
        for _,cours in course.iterrows():
            #i=i+1
            id = cours['ID_FORMATION']
            domaine = cours['DOMAINE_CATGEGORIE']
            sous_domaine = cours['SOUS_DOMAINE_CATEGORIE']
            nom_formation = cours['FORMATION_COURS']
            name_to_search = nom_formation + ' ' + domaine + ' ' + sous_domaine 
            dict1 = search_course(course_name=name_to_search)
            print(dict1)
            for _ in range(len(dict1['liens'])):
                ids.append(id)
                domaines.append(domaine)
                sous_domaines.append(sous_domaine)
                nom_formations.append(nom_formation)
            liens.append(dict1['liens'])
            images.append(dict1['images'])
            ratings.append(dict1['ratings'])
            titres.append(dict1['titres'])
            formateurs.append(dict1['formateurs'])
    except:
        print("ntg")
    new_data = pd.DataFrame({
        'ID_FORMATION' : ids,
        'DOMAINE_CATGEGORIE' : domaines,
        'SOUS_DOMAINE_CATEGORIE' : sous_domaines,
        'FORMATION_COURS' : nom_formations,
        'FORMATEUR' : flatten(formateurs),
        'TITRE' : flatten(titres),
        'IMAGES' : flatten(images),
        'RATINGS' : flatten(ratings),
        'LIENS' : flatten(liens)
    })
    new_data.to_csv('reste_des_formations.csv', index=False)
main()


# Fermer le navigateur après l'extraction
driver.quit()

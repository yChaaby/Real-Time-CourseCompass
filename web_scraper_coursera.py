from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time

driver = webdriver.Firefox()  # Assurez-vous que le chemin de ChromeDriver est dans le PATH

# Ouvrir la page cible
driver.get("https://www.coursera.org/search?query=Direction%20de%20l%27entreprise%20Ressources%20humaines%20Pr%C3%A9venir%20et%20faire%20face%20aux%20agissements%20sexistes%20et%20au%20harc%C3%A8lement%20sexuel%20au%20travail")  # Remplacez par l'URL de la page contenant les cartes produit

# Attendre un peu que la page charge (ajuster le temps si nécessaire)
time.sleep(3)  # Attendre 3 secondes

# Utiliser BeautifulSoup pour analyser le HTML de la page
soup = BeautifulSoup(driver.page_source, 'html.parser')

# Trouver tous les éléments li contenant les informations sur les cours
cours_list = soup.find_all('li', class_='cds-9 css-0 cds-11 cds-grid-item cds-56 cds-64 cds-76 cds-90')

# Extraire les informations souhaitées
for cours in cours_list:
    title = cours.find('h3', class_='cds-CommonCard-title css-6ecy9b')
    image = cours.find('img')
    rating = cours.find('span', class_='css-6ecy9b')
    duration = cours.find('p', class_='css-vac8rf')
    link = cours.find('a', href=True)  # Trouver le lien (attribut href)

    # Afficher les informations extraites
    print("Titre du cours:", title.get_text() if title else 'Non trouvé')
    print("Image URL:", image['src'] if image else 'Non trouvé')
    print("Note:", rating.get_text() if rating else 'Non trouvé')
    print("Durée:", duration.get_text() if duration else 'Non trouvé')
    print("Lien vers le cours:", link['href'] if link else 'Non trouvé')  # Afficher le lien
    print('-' * 60)

# Fermer le navigateur après l'extraction
driver.quit()

'''
That Code are used to incresse the data quality !
Problem : Courses with same title but different content !
Solution : using prompt engineering title + category + subcategory = new title !

'''
import google.generativeai as genai
import pandas as pd
import time
import csv
import random

file_path = "/Users/youssefchaabi/data_formation_after_shower.csv"

genai.configure(api_key="")
model = genai.GenerativeModel("gemini-1.5-flash")
i = 0
def reformuler(titre:str):
    #i=i+1
    
    response = model.generate_content("reformule le titre de la formation suivant en un titre attirant le titre donnée est de cette forme domaine - sous domaine - titre a ameliorer, fait un titre lux classe A mais qu'il soit naturell ne commence pas toujours des maitriser, apprenez fait mais pas toujours !! il dit la meme chose pas d'abvreation  . je veux que le titre soit innovant des nouvelle mots utilise les synonymes (les deux titres doivent dire la meme chose quand meme !) !(reponse juste avec le titre pas plus !), le titre : "+titre)
    
    time.sleep(1)
    print(i)
    print(response.text)
    return str(response.text)
def proc():

    df = pd.read_csv(file_path)
    """df["CLASSEMENT"] = "NULL"
    df.to_csv(file_path, index=False)
    print("cancel here hun")
    time.sleep(10)"""
    # Mélanger l'index des lignes de manière aléatoire

    # Modifier et sauvegarder ligne par ligne de manière aléatoire
    for idx, row in df.iterrows():
        if row['new_title'] != "RIEN":
            continue

        # Modifier la ligne
        df.at[idx, 'new_title'] = reformuler(row['DOMAINE_CATGEGORIE'] + " - " + row['SOUS_DOMAINE_CATEGORIE'] + " - " + row['FORMATION_COURS'])

    # Sauvegarde après la boucle
        df.to_csv(file_path, index=False)

    print("Modifications effectuées et sauvegardées!")


def clean():
    df = pd.read_csv(file_path)
    df['KEYWORDS'] = ""
    df['CLASSEMENT'] = "RIEN"
    df.to_csv(file_path, index=False)
def recherche(titre:str):
    #i=i+1
    text = """Objectif : Générer 14 mots-clés pour un titre de formation donné.
        Critères :

        7 technologies similaires au titre de la formation (ex. : LinkedIn → Indeed, Instagram → Facebook).
        6 autres mots-clés pertinents pour faciliter la recherche (ex. : outils, méthodologies, concepts clés).
        Pas de répétition, mots-clés précis et spécifiques.
        Pas de répétition, mots-clés précis et spécifiques. (si un mot dans le titre ne le fait pas en mots clé)
        l'intituler est le plus important !! pour generer les mots clé
        les mots clé doivent dependre directement avec l'intituler ! 
        je veux une reponse de ce type (motclé1 motclé2 motclé3 ... techno1 techo2 ...) 
        repondre juste avec les mots clé pas plus !!! toujours une reponse de cette forme : (motclé1 motclé2 motclé3 ... techno1 techo2 ...) 
        Exemple :
        Titre : Bureautique || PAO/CAO || PowerPoint - Avancé (domaine - sous domaine - intituler)
        Exemple de reponse :(motclé1 motclé2 motclé3 ... techno1 techo2 ...) 
        Google Slides, Keynote, Prezi, Microsoft Teams, Trello, Canva, LibreOffice.\n titre :"""
    response = model.generate_content(text+titre)
    time.sleep(1)
    #print(i)
    print(response.text)
    return str(response.text).replace("\n","")

def proc2():
    df = pd.read_csv(file_path)
    """df["CLASSEMENT"] = "RIEN"
    df.to_csv(file_path, index=False)
    print("cancel here hun")
    time.sleep(10)"""

    # Modifier et sauvegarder ligne par ligne de manière aléatoire
    for idx, row in df.iterrows():
        if row['CLASSEMENT'] != "RIEN":
            continue

        # Modifier la ligne
        df.at[idx, 'KEYWORDS'] = recherche(row['DOMAINE_CATGEGORIE'] + " - " + row['SOUS_DOMAINE_CATEGORIE'] + " - " + row['FORMATION_COURS'])
        df.at[idx, 'CLASSEMENT'] = "YES"
    # Sauvegarde après la boucle
        df.to_csv(file_path, index=False)

    print("kayn !")
proc2()
#recherche("Bureautique || PAO/CAO || Maitrisez Excel,word,powerpoint")
#clean()
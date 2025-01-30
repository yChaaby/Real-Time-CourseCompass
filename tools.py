import cx_Oracle
from kafka import KafkaProducer
import json
import streamlit as st
from typing import List
from models import Formation, Formateur, Client
# Connexion à la base de données Oracle
def connect_to_oracle():
    try:
        cx_Oracle.init_oracle_client(lib_dir="/Users/youssefchaabi/instantclient_19_16")
    except:
        print("An exception occurred")
    # Remplace les valeurs ci-dessous par tes propres paramètres de connexion
    dsn = cx_Oracle.makedsn("localhost", "1521", service_name="XEPDB1")
    conn = cx_Oracle.connect(user="SEFORMER", password="153300", dsn=dsn)
    return conn
# Fonction de recherche dans la base de données
def search_in_formateurs(ID_for):

    conn = connect_to_oracle()
    cursor = conn.cursor()
    # Exemple de requête SQL, avec des paramètres pour éviter les injections SQL
    cursor.execute("SELECT formations.formation_cours, formations.id_formation, former.site_web, former.telephone, former.adresse, formateurs.nom_formateur FROM former, formations, formateurs  WHERE former.id_formateur = formateurs.id_formateur and former.id_formation = formations.id_formation and formations.id_formation = :1", [ID_for])
    print(cursor)
    results = cursor.fetchall()
    # Fermer la connexion
    cursor.close()
    conn.close()
    list_formateurs = []
    streamInteraction(formation_id=ID_for,username=(st.session_state.user).id )
    for row in results:
        list_formateurs.append(Formateur(
        nom_formateur=row[5],
        formation_id=row[1],
        site_web=row[2],
        numero=row[3],
        adresse=row[4]
        ))
    return list_formateurs
def rechercher_formation_avancee(p_chaine, cat):
    conn = connect_to_oracle()
    cursor = conn.cursor()

    # Déclaration du curseur pour récupérer les résultats
    result_cursor = cursor.var(cx_Oracle.CURSOR)

    # Si la catégorie est "Tous les categories", ajuster le paramètre
    if "Tous les categories" in cat:
        cat = "text"  # Ou tout autre traitement nécessaire selon vos besoins
    
    # Appel de la procédure stockée
    try:
        cursor.callproc("rechercher_formation_avancee", [p_chaine, 0, 12, result_cursor])

        # Récupérer les résultats depuis le curseur
        results = result_cursor.getvalue().fetchall()

        # Fermer le curseur et la connexion
        cursor.close()
        conn.close()

        # Création de la liste des formations
        list_formation = []
        for row in results:
            list_formation.append(Formation(id_formation=row[0],
                                            domaine_categorie=row[1],
                                            sous_domaine_categorie=row[2],
                                            formation_cours=row[3]
                                            ))

        # Retourner la liste des formations
        return list_formation

    except cx_Oracle.DatabaseError as e:
        print(f"Une erreur est survenue: {e}")
        cursor.close()
        conn.close()

def search_cats():
    conn = connect_to_oracle()
    cursor = conn.cursor()
    # Exemple de requête SQL, avec des paramètres pour éviter les injections SQL
    cursor.execute("select DISTINCT DOMAINE_CATGEGORIE from FORMATIONS")
    results = cursor.fetchall()
    # Fermer la connexion
    cursor.close()
    conn.close()
    return list(results)
# Interface de recherche Streamlit
def check_credentials(username, password):
    conn = connect_to_oracle()
    cursor = conn.cursor()
    
    # Exemple de requête SQL pour vérifier les informations de l'utilisateur
    query = "SELECT * FROM clients WHERE username = :username AND mot_de_passe = :password"
    cursor.execute(query, {"username": username, "password": password})
    
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    print("--",user)
    if user:
        return True  # Authentification réussie
    else:
        return False  # Authentification échouée
def get_user(username):
    conn = connect_to_oracle()
    cursor = conn.cursor()
    # Exemple de requête SQL, avec des paramètres pour éviter les injections SQL
    cursor.execute("SELECT * FROM clients where username = :1", [username])
    print(cursor)
    results = cursor.fetchall()
    # Fermer la connexion
    cursor.close()
    conn.close()
    for row in results:
        return Client(id = row[0], nom=row[1], prenom=row[2], age=row[3], username=username)
    
def streamInteraction(username, formation_id, with_formation=None):
    producer = KafkaProducer(
        bootstrap_servers=['localhost:9092'],  # Adresse du broker Kafka
        value_serializer=lambda v: json.dumps(v).encode('utf-8')  # Sérialisation JSON
    )
    topic = "interaction"
    print("le ID : ----",username,type(username))
    print("le Iid_formation : ----",formation_id,type(formation_id))
    message = {"id_client": username, "id_formation": formation_id}
    producer.send(topic, value=message)


import cx_Oracle
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
    conn = cx_Oracle.connect(user="SEFORMAER_PLUS", password="153300", dsn=dsn)
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
    i=0
    # Déclaration du curseur pour récupérer les résultats
    result_cursor = cursor.var(cx_Oracle.CURSOR)
    if "Tous les categories" in cat:
        i = 1
        cat = "text"
    # Appel de la procédure
    print(p_chaine, result_cursor, cat, i)
    cursor.callproc("rechercher_formation_avancee", [p_chaine, cat,result_cursor, i])
    
    # Récupération des résultats
    results = result_cursor.getvalue().fetchall()
    
    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()
    print(results)
    list_formation = []
    for row in results:
        list_formation.append(Formation(id_formation=row[0], domaine_categorie=row[1], sous_domaine_categorie=row[2], formation_cours=row[3]))
    Ids = [row[0] for row in results]
    Nom_for = [row[3] for row in results]
    
    return list_formation
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
from typing import List
from streamlit_pills import pills
import streamlit as st
import cx_Oracle
from streamlit_searchbox import st_searchbox
from models import Formation, Formateur

st.set_page_config(layout="wide")

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
    cursor.execute("SELECT formations.formation_cours, formations.id_formation, former.site_web, former.telephone, former.adresse FROM former, formations, formateurs  WHERE former.id_formateur = formateurs.id_formateur and former.id_formation = formations.id_formation and formations.id_formation = :1", [ID_for])
    print(cursor)
    results = cursor.fetchall()
    # Fermer la connexion
    cursor.close()
    conn.close()
    list_formateurs = []
    for row in results:
        list_formateurs.append(Formateur(
        nom_formateur=row[0],
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
st.title("SeFormer")

selected = pills("Categories",[("Tous les categories 👨🏻‍🏫", )] + search_cats())

def search_course(searchterm: str) -> List[any]:
    return rechercher_formation_avancee(searchterm, selected[0]) if searchterm else []

# pass search function to searchbox
selected_value = st_searchbox(
    search_course,
    key="rechercher une formation",
)
with st.container():
    # Appliquer un style pour le rectangle
    if selected_value is not None:
        for formateur in search_in_formateurs(selected_value.ID_FORMATION):
            # Construire le contenu HTML de façon conditionnelle
            address = f"<p><strong>📍</strong> {formateur.ADRESSE}</p>" if formateur.ADRESSE is not None else ""
            phone = f"<p><strong>☎️</strong> {formateur.NUMERO}</p>" if formateur.NUMERO is not None else ""
            website_button = (
                f'<a href="{formateur.SITE_WEB}" target="_blank" style="text-decoration: none;">'
                f'<button style="background-color: #FF4B4B; color: white; padding: 8px 16px; '
                f'border: none; border-radius: 8px; cursor: pointer;">'
                f'Visitez le site web</button></a>'
            ) if formateur.SITE_WEB is not None else ""

            formateur_info = f"{formateur.NOM_FORMATEUR}" if formateur.NOM_FORMATEUR else ""
            selected_info = f"{selected_value}" if selected_value else ""
            
            # Afficher uniquement les attributs non None
            st.markdown(
                f"""
                <div style="border: 2px solid #FF4B4B; border-radius: 12px; padding: 8px; margin: 5px;">
                <h3>{formateur_info} || {selected_info}</h3>
                {address}
                {phone}
                {website_button}
                </div>
                """,
                unsafe_allow_html=True
            )
        
print(selected[0])
print(selected_value)
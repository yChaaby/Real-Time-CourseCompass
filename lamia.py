import streamlit as st
import cx_Oracle

# Fonction pour établir la connexion à la base de données
def get_db_connection():
    dsn_tns = cx_Oracle.makedsn('hostname', 'port', service_name='service_name')  # Remplacez par vos paramètres
    conn = cx_Oracle.connect(user='username', password='password', dsn=dsn_tns)
    return conn

# Fonction pour appeler la procédure et récupérer les résultats
def rechercher_formation_avancee(p_chaine):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Déclaration du curseur pour récupérer les résultats
    result_cursor = cursor.var(cx_Oracle.CURSOR)
    
    # Appel de la procédure
    cursor.callproc("rechercher_formation_avancee", [p_chaine, result_cursor])
    
    # Récupération des résultats
    results = result_cursor.getvalue().fetchall()
    
    # Fermer le curseur et la connexion
    cursor.close()
    conn.close()
    
    return results

# Interface utilisateur Streamlit
st.title("Recherche de Formations")

# Champ de saisie pour la recherche
p_chaine = st.text_input("Entrez votre recherche:")

if st.button("Rechercher"):
    if p_chaine:
        # Appel de la procédure avec la chaîne de recherche
        results = rechercher_formation_avancee(p_chaine)

        # Affichage des résultats
        if results:
            st.write("Résultats trouvés:")
            for row in results:
                st.write(f"ID: {row[0]}, Domaine: {row[1]}, Sous-domaine: {row[2]}, Cours: {row[3]}, "
                         f"Edit Distance: {row[4]}, Jaro-Winkler: {row[5]}, Pertinence: {row[6]}")
        else:
            st.write("Aucun résultat trouvé.")
    else:
        st.write("Veuillez entrer une chaîne de recherche.")
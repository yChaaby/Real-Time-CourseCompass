from typing import List
from streamlit_pills import pills
import streamlit as st
from streamlit_searchbox import st_searchbox
from models import Formation, Formateur
from tools import connect_to_oracle, search_in_formateurs, search_cats, rechercher_formation_avancee, check_credentials, get_user


#st.set_page_config(layout="wide")
titre = st.empty()

hide_header_style = """
    <style>
    header {
        visibility: hidden;
    }
    </style>
"""
st.markdown(hide_header_style, unsafe_allow_html=True)

def fun():
    selected = pills("Categories",[("Tous les categories 👨🏻‍🏫", )] + search_cats())
    def search_course(searchterm: str) -> List[any]:
        return rechercher_formation_avancee(searchterm, selected[0]) if searchterm else []
    print(selected)
# pass search function to searchbox
    selected_value = st_searchbox(
        search_course,
        placeholder="Que souhaitez-vous apprendre ?",
        key="rechercher une formation"
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
                    f'<button style="background-color: #AC947F; color: white; padding: 8px 16px; '
                    f'border: none; border-radius: 8px; cursor: pointer;">'
                    f'Visitez le site web</button></a>'
                ) if formateur.SITE_WEB is not None else ""

                formateur_info = f"{formateur.NOM_FORMATEUR}" if formateur.NOM_FORMATEUR else ""
                selected_info = f"{selected_value}" if selected_value else ""
                
                # Afficher uniquement les attributs non None
                st.markdown(
                    f"""
                    <div style="border: 2px solid #AC947F; border-radius: 8px; padding: 15px; margin-bottom: 7px;">
                    <h4>{formateur_info} || {selected_info}</h3>
                    {address}
                    {phone}
                    {website_button}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

print(st.session_state)

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False  # Initialisation de la variable d'authentification


if not st.session_state.authenticated:
    titre.title("SeFormer - Page d'authentification")
    username_ph = st.empty()
    password_ph = st.empty()
    connect = st.empty()
    # Demander à l'utilisateur de saisir ses informations
    username = username_ph.text_input("Nom d'utilisateur")
    password = password_ph.text_input("Mot de passe", type="password")

    # Vérifier l'authentification
    if connect.button("Se connecter"):
        if check_credentials(username, password):
            # Authentification réussie, stocker l'état dans la session
            st.session_state.authenticated = True
            st.session_state.user = get_user(username)  # Stocker le nom d'utilisateur

            # Changer le titre de la page
            titre.title("SeFormer - Accueil")
            username_ph.empty()
            password_ph.empty()
            connect.empty()
            # Afficher un message de bienvenue
            st.success(f"Bienvenue {st.session_state.user.prenom} ! ")
            
            # Afficher le contenu principal
            fun()
            print(st.session_state)

        else:
            st.error("Nom d'utilisateur ou mot de passe incorrect.")
else:
    # Si déjà authentifié, afficher la page d'accueil
    st.title("SeFormer - Accueil")
    st.success(f"Bienvenue {st.session_state.user.prenom}!")
    fun()

    # Option de déconnexion



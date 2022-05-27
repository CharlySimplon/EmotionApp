import streamlit as st
import requests
from patient import Patient
from fonctions import Data

URL_API = "http://host.docker.internal:8000"


class Coach():

    def __init__(self, username):
        self.username = username

    def create_user(is_admin, username, password):
        infos = {
            "is_admin": is_admin,
            "username": username,
            "password": password
        }
        response = requests.post(f"{URL_API}/users", json=infos)
        if response.status_code == 200:
            return f"Successfully created {infos['username']}"
        else:
            return "Can't create this user"


    def manage_users(self):

        username = st.text_input("Username du patient à ajouter")
        password = st.text_input("Password du patient à ajouter")
        new_user_admin = False

        st.button("Ajouter un patient", on_click=Data.create_user(new_user_admin, username, password))


    def read_diary(self):


        username = st.text_input("Nom du patient")

        if st.checkbox('Lire les notes du patient'):
            response_data = Data.get_user(username)
            user_id = response_data.get('user_id')
            all_notes = Data.get_notes(user_id)
            st.write(all_notes)

    
    def see_feeling(self):

        username = st.text_input("Nom du patient")

        if st.checkbox('Voir les émotions du patient'):
            response_data = Data.get_user(username)
            user_id = response_data.get('user_id')
            all_notes = Data.get_notes(user_id)
            st.write(all_notes)
            
    
    def page(self):

        #---OPTIONS COACH---
        if st.checkbox("GESTION DES PATIENTS"):
            self.manage_users()

        if st.checkbox("VOIR LES NOTES ET LES EMOTIONS D'UN PATIENT"):
            self.read_diary()

        # if st.checkbox("VOIR LES EMOTIONS D'UN PATIENT"):
        #     self.see_feeling()
        
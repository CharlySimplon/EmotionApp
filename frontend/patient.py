from ssl import ALERT_DESCRIPTION_UNKNOWN_PSK_IDENTITY
import streamlit as st
import requests
import datetime
from fonctions import Data

URL_API = "http://host.docker.internal:8000"




class Patient():

    def __init__(self, username: str, user_id : int):
        self.username = username
        self.user_id = user_id


    # def reading(self):
    #             url = f"http://host.docker.internal:8000/user/{self.user_id}/notes/"
    #             print(f'{self.user_id}')
    #             request = requests.get(url)
    #             response_data = request.json() 
    #             for note in response_data :
    #                 note_content_list = []
    #                 note_content_list.append(note['note_content'])
    #             return  st.write(f"{note_content_list}")


        
    # Create a note for a patient
    def create_note(self):


        note = st.text_input("Racontez succintement votre journée...")

        if st.button('Valider'):

            note_data = {
            "user_id": self.user_id,
            "note_content": note,
            "date": datetime.date.today().strftime("%d%m%Y"),
            "note_sentiment": Data.predict(note)
            }
            requests.post(f"{URL_API}/users/{self.user_id}/notes/", json=note_data)
            response_data = Data.get_user(self.username)
            prediction = response_data.get('notes')[-1]['note_sentiment']
            st.success(f'Votre sentiment de la journée : {prediction}')

            
    # Modify note of the day NOT TESTED YET
    def modify_note(self):
        new_note = st.text_input("Mettez vos modifications...")
        date = datetime.date.today().strftime("%d%m%Y")
        response_data = Data.get_user(self.username)
        note_to_modify = response_data.get("notes")[-1]
        id = note_to_modify['id']
        if st.button('Modifier'):
            if note_to_modify["date"] == date:
                modified_note = {
                    # "id": id,
                    "user_id": self.user_id,
                    "note_content": new_note,
                    "date":date,
                    "note_sentiment": Data.predict(new_note)
                }
                requests.patch(f"{URL_API}/users/{self.user_id}/notes/{id}", json=modified_note)
                response_data = Data.get_user(self.username)
                prediction = response_data.get('notes')[-1]['note_sentiment']
                st.success(f'Votre sentiment de la journée : {prediction}')
            else :
                return st.write("You can't modify a former note")



    
    def read_text(self):

        #CRITERE ANNEE
        years_list = [2018,2019,2020,2021,2022]
        year_choosen = st.selectbox(
            'Année : ',
            (years_list)
            )

        #CRITERE MOIS
        months_dict = {'Janvier': '01', 'Février': '02', 'Mars': '03', 'Avril': '04', 'Mai':'05', 'Juin':'06', 'Juillet':'07', 'Août':'08', 'Septembre': '09', 'Octobre':'10', 'Novembre':'11','Décembre':'12'}
        months_list = ['Janvier', 'Février', 'Mars', 'Avril','Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Décembre']
        month_choosen = st.selectbox(
                    'Mois : ',
                    (months_list),
                )
        month_choosen_number = months_dict[month_choosen]


        #CRITERE JOUR
        day_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31]
        day_choosen = st.selectbox(
                    'Jour : ',
                    (day_list),
                )

        #BOUTTON DE RECHERCHE
        if st.button('Recherche !'):
            #Envoyer à l'API le datetime
            date = f'{day_choosen}{month_choosen_number}{year_choosen}'
            st.write(date)

            note = Data.get_note(self.user_id, date)
            st.write(note)

    
    def page(self):

        #---OPTIONS PATIENT---

        if st.checkbox('Ecrire dans votre journal intime'):
            self.create_note()

        if st.checkbox('Modifier du contenu'):
            self.modify_note()

        if st.checkbox('Lire certains de vos écrits'):
            self.read_text()
        









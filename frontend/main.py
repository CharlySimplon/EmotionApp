import streamlit as st
from PIL import Image
from authentification import Login
from fonctions import Data

import requests



URL_API = "http://host.docker.internal:8000"



def main():

    # #HAUT DE PAGE
    st.title("Journal intime avec Coach Zen")

    #LOGO
    img = Image.open("diary.jpg") 
    st.image(img, width=600) 

    x = requests.get('http://host.docker.internal:8000/')
    st.write(x.json()["message"])

    # Data.create_user(1, "ZEN", "1234")
    # Data.create_user(0, 'Jean', '5678' )
    

    #Lancement page d'accueil pour se log
    Login().page()




if __name__ == '__main__':
    main()
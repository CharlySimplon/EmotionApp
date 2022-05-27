import streamlit as st
import streamlit_authenticator as stauth
from patient import Patient
from coach import Coach
import requests

URL_API = "http://host.docker.internal:8000"

class Login():

    def page(self):

        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password")
        # hashed_password = stauth.Hasher(password).generate()
        hashed_password = password
        # st.sidebar.button("Connexion", on_click=self.chosen_page(username, hashed_password))
        if st.sidebar.checkbox('Connexion'):
            self.chosen_page(username, hashed_password)

        # authenticator = stauth.authenticate(username,hashed_password,
        # 'some_cookie_name','some_signature_key',cookie_expiry_days=30)

        # username, authentication_status = authenticator.login('Login','main')

        # if authentication_status:
        #     st.write('Welcome *%s*' % (name))
        #     st.title('Some content')
        # elif authentication_status == False:
        #     st.error('Username/password is incorrect')
        # elif authentication_status == None:
        #     st.warning('Please enter your username and password')

        # if st.session_state['authentication_status']:
        #     st.write('Welcome *%s*' % (st.session_state['name']))
        #     st.title('Some content')
        # elif st.session_state['authentication_status'] == False:
        #     st.error('Username/password is incorrect')
        # elif st.session_state['authentication_status'] == None:
        #     st.warning('Please enter your username and password')
       
    def chosen_page(self, username, hashed_password):
        
        url = f"http://host.docker.internal:8000/login/{username}"
        requestpost = requests.get(url)
        response_data = requestpost.json() 
        is_admin = response_data.get("is_admin")
        db_password = response_data.get("hashed_password")
        user_id = response_data.get("id")


        if is_admin == True and db_password == hashed_password :
            Coach(username).page()
        elif is_admin == False and db_password == hashed_password :
            user = Patient(username,user_id)
            user.page()
        elif is_admin == True and db_password != hashed_password :
            return st.write("Mot de passe incorrect")
        elif is_admin == False and db_password != hashed_password :
            return st.write("Mot de passe incorrect")
        else:
            return st.write("VEUILLEZ VOUS AUTHENTIFIER")


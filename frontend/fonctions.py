import streamlit as st
import pandas as pd
import sqlite3
from sqlite3 import Connection
import requests
import datetime

import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

URL_API = "http://host.docker.internal:8000"


class Data():

    def init_db_users(conn: Connection):
        URI_SQLITE_DB = "users_notes.db"
        conn = Data.get_connection(URI_SQLITE_DB)

        conn.execute(
            """CREATE TABLE IF NOT EXISTS Users
                (
                    user_id INT PRIMARY KEY NOT NULL,
                    is_admin BOOL,
                    username VARCHAR(50),
                    password VARCHAR(50)
                );"""
        )
        conn.commit()

    def init_db_notes(conn: Connection):
        URI_SQLITE_DB = "users_notes.db"
        conn = Data.get_connection(URI_SQLITE_DB)

        conn.execute(
            """CREATE TABLE IF NOT EXISTS Notes
                (
                    note_id INT PRIMARY KEY NOT NULL,
                    user_id INT,
                    date DATE,
                    note_content VARCHAR(300),
                    note_sentiment VARCHAR(30)
                );"""
        )
        conn.commit()

    def get_admin_rights(username, hashed_password):
        URI_SQLITE_DB = "users_notes.db"
        conn = Data.get_connection(URI_SQLITE_DB)
        
        is_admin = pd.read_sql("SELECT * FROM Users", con=conn)
        return is_admin

    def get_all_users(Users):
        user_list=[]
        for info in Users.query.all():
            user_list.append(info)
        return user_list

    def get_user(username):
        url = f"http://host.docker.internal:8000/login/{username}"
        requestpost = requests.get(url)
        return requestpost.json() 
        

    def get_content(user_id):
        URI_SQLITE_DB = "users_notes.db"
        conn = Data.get_connection(URI_SQLITE_DB)
        
        content = pd.read_sql("SELECT * FROM Notes", con=conn)
        return content

        
    @st.cache(hash_funcs={Connection: id})
    def get_connection(path: str):
        """Put the connection in cache to reuse if path does not change between Streamlit reruns.
        NB : https://stackoverflow.com/questions/48218065/programmingerror-sqlite-objects-created-in-a-thread-can-only-be-used-in-that-sa
        """
        return sqlite3.connect(path, check_same_thread=False)

    # create user
    def create_user(is_admin, username, password):
        infos = {
            "is_admin": is_admin,
            "username": username,
            "password": password
        }
        response = requests.post(f"{URL_API}/users/", json=infos)
        if response.status_code == 200:
            return f"Successfully created {infos['username']}"
        else:
            return "Can't create this user"


        
    # Return all notes of a patient
    def get_notes(user_id):  
        return requests.get(f"{URL_API}/users/{user_id}/notes/").json()

    # get one note from a patient
    def get_note(user_id, id):  
        return requests.get(f"{URL_API}/users/{user_id}/notes/{id}").json()
    
    # get one note from a patient for a date
    def get_text(user_id, date):  
        return requests.get(f"{URL_API}/users/{user_id}/text/{date}").json()


    def delete_note(user_id, id):
        infos = {
            "user_id":user_id,
            "id":id
        }
        return requests.delete(f"{URL_API}/users/{user_id}/notes/{id}", json=infos)

    def predict(text):

        text_to_predict = [text]

        vocab_size = 10000
        oov_token = "<OOV>"
        tokenizer = Tokenizer(num_words = vocab_size, oov_token=oov_token)
        tokenizer.fit_on_texts(text_to_predict)
        word_index = tokenizer.word_index
        text_to_predict_sequences = tokenizer.texts_to_sequences(text_to_predict)

        max_length = 100
        padding_type='post'
        truncation_type='post'
        text_to_predict_padded = pad_sequences(text_to_predict_sequences,maxlen=max_length, padding=padding_type, truncating=truncation_type)
        
        embeddings_index = {}
        f = open('glove.6B.100d.txt', encoding="utf8")
        for line in f:
            values = line.split()
            word = values[0]
            coefs = np.asarray(values[1:], dtype='float32')
            embeddings_index[word] = coefs
        f.close()

        embedding_matrix = np.zeros((len(word_index) + 1, max_length))
        for word, i in word_index.items():
            embedding_vector = embeddings_index.get(word)
            if embedding_vector is not None:
                # words not found in embedding index will be all-zeros.
                embedding_matrix[i] = embedding_vector
        
        model = load_model("my_model_kag_dropout")
        sentiment_pred = model.predict(text_to_predict_padded)
        sentiment_pred = np.argmax(sentiment_pred, axis=1)
        
        label_match = {0:"anger", 1:"fear", 2:"happy", 3:"love", 4:"sadness", 5:"surprise"}
        sentiment_pred = label_match[sentiment_pred[0]]

        return sentiment_pred
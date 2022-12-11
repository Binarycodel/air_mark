from email.message import EmailMessage
from streamlit_extras import switch_page_button

import streamlit as st
import mysql.connector

# Initialize connection.
# Uses st.experimental_singleton to only run once.
@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.

@st.experimental_memo(ttl=600)
def get_record(query):
    with conn.cursor() as cur:
        cur.execute(query)
        cur 
        return cur.fetchall()




@st.experimental_memo(ttl=600)
def add_user(id, location, destination, category):
    query = '''INSERT INTO airmark_databases.user(id, location, destination , category) VALUES(%s, %s, %s, %s)'''
    isSuccess = False 
    with conn.cursor() as curs: 
        # (id, first_name, second_name, email, password)
        curs.execute(query , (id, location, destination, category))
        isSuccess = True
        print('execution successful')
    return isSuccess


# if add_user(4,'salam', 'ahmed', 'ahmed@gmail.com', 'binary'):
#     print('confirm')
# else:
#     print('error')



@st.experimental_memo(ttl=600)
def add_booking(id, first_name, second_name, email, password):
    query = '''INSERT INTO airmark_databases.flight_booking(id, first_name, second_name , email, password) VALUES(%s, %s, %s, %s ,%s)'''
    isSuccess = False 
    with conn.cursor() as curs: 
        # (id, first_name, second_name, email, password)
        curs.execute(query , (id, first_name, second_name, email, password))
        isSuccess = True
        print('execution successful')
    return isSuccess


rows = get_record("SELECT * from user;")
print(rows)

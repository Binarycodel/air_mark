import streamlit as st 
from streamlit_extras import switch_page_button
import mysql.connector



# defining global parameter
login_status = False


# app title
st.title('AirMark Management System')


# widgets
st.header('Login In')


# ==============  DATABSE CONNECTIVITIES ======================
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
        return cur.fetchall()




@st.experimental_memo(ttl=600)
def add_user(id, first_name, second_name, email, password):
    query = '''INSERT INTO airmark_databases.user(id, first_name, second_name , email, password) VALUES(%s, %s, %s, %s ,%s)'''
    isSuccess = False 
    with conn.cursor() as curs: 
        # (id, first_name, second_name, email, password)
        curs.execute(query , (id, first_name, second_name, email, password))
        isSuccess = True
        print('execution successful')
    return isSuccess

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


# ========================== END OF DATABASE CONNECTION ===============================

# rows = get_record("SELECT email, password from user;")
# st.write(rows)

# status message 
def status_message(status=False, message='error'):
    if status:
        status_l1.error(message)
    else:
        status_l1.success(message)

# layout definations (three columns)
status_l1, statusl_l2 = st.columns([2,1])
email1, email2 = st.columns([2,1])
pass1, pass2 = st.columns([2,1])




email = email1.text_input("Enter Email")
password = pass1.text_input('Enter Password', type='password')

col_one , col_two = st.columns([1,1])

sign_button = col_two.button('Sign Up')
if sign_button: 
    switch_page_button.switch_page("signup")



if col_one.button('login'):
    # validate credentials 
    rows = get_record("SELECT email, password from user;")
    # st.write(rows)
    for d in rows: 
        username, pas = d[0], d[1]
        if email.strip() == username.strip() and password.strip() == pas.strip(): 
            
            #  creating session 
            if  'user' not in st.session_state: 
                st.session_state['user'] = username
            
            switch_page_button.switch_page("Home")
    else: 
        status_message(True, 'Wrong Email or Password')
        # st.write('something wrong')


col_two.checkbox('Remember Me?', value=True)



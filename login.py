import streamlit as st 
from streamlit_extras import switch_page_button
import databases as db


# defining global parameter
login_status = False

database = db.Database()
database.create_user_table()
database.create_booking_table()
database.create_comment_table()

# app title
st.title('AirMark Management System')


# widgets
st.header('Login In')


# ==============  DATABSE CONNECTIVITIES ======================

def get_record(query):
    return database.validate_user_record()
    

def add_user(id, first_name, second_name, email, password,sex, age):
    database.insert_to_user_table(first_name, second_name, email, password, sex, age)
    st.write('record addesd successfull')


# ========================== END OF DATABASE CONNECTION ===============================

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
    rows = get_record("SELECT email, password, sex from user_table;")
    st.write(rows)
    # st.write(rows)
    if rows == None : 
        st.warning("No record Found")
    else :

        for d in rows: 
            username, pas, sex = d[0], d[1], d[2]
            if email.strip() == username.strip() and password.strip() == pas.strip(): 
                
                #  creating session 
                if  'user' not in st.session_state: 
                    st.session_state['user'] = username
                    st.session_state['sex'] = sex
                
                switch_page_button.switch_page("Home")
        else: 
            status_message(True, 'Wrong Email or Password')
            # st.write('something wrong')


col_two.checkbox('Remember Me?', value=True)



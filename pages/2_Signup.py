import streamlit as st 
from streamlit_extras import switch_page_button
import databases as db
import streamlit as st

import re

class Validator:
    def __init__(self):
        pass

    def is_valid_email(self, email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        return re.match(pattern, email) is not None

    def is_valid_phone(self, phone):
        pattern = r'^\+?\d{10,15}$'
        return re.match(pattern, phone) is not None

    def is_valid_number(self, number):
        pattern = r'^[0-9]+$'
        return re.match(pattern, number) is not None

    
    
# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)


# st.set_page_config(page_title="signup" , page_icon='📈' , initial_sidebar_state='collapsed')
with open('style.css') as css: 
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)
# ==============  DATABSE CONNECTIVITIES ======================
# st.set_page_config(initial_sidebar_state="collapsed")

database = db.Database()
validator = Validator()


def get_record(query):
    return database.custom_query(query)


def add_user(first_name, second_name, email, password,sex, age , booking_id):
    database.insert_to_user_table(first_name, second_name, email, password, sex, age, booking_id)
    return True 

# ========================== END OF DATABASE CONNECTION ===============================

# defining global parameter
login_status = False


# app title
st.title('Air Remark Management System')


# widgets
st.header('Register New User ')


# status message 
def status_message(status=False, message='error'):
    if status:
        status_l1.error(message)
    else:
        status_l1.success(message)

# layout definations (three columns)
status_l1, statusl_l2 = st.columns([2,1])
name1, name2 = st.columns([2,1])
email1, email2 = st.columns([2,1])
password1, password2 = st.columns([2,1])
pass1, pass2 = st.columns([2,1])
sex_panel , age_panel = st.columns([2,1])




fname = name1.text_input("First Name")
lname = name2.text_input("Last Name")
email = email1.text_input("Email" )
# booking_id = email2.text_input('Booking ID')
booking_id = ' '
password = pass1.text_input('Password', type='password')
password2 = pass2.text_input('Confirm Password', type='password')

sex = sex_panel.selectbox('Select Gender' , ('Male', 'Female'))
age = age_panel.text_input("Enter Age")


col_one , col_two = st.columns([1,1])

sign_button = col_two.button('Back')
if sign_button: 
    switch_page_button.switch_page("login")



regitem  = [fname, lname, email, password, password2]

if col_one.button('Submit'):
    # validate data suply 
    if validator.is_valid_email(email):
        print(regitem)
        if "" not in regitem: 
            if password2 == password : 
                rows = get_record("SELECT * from user_table;")
                id = len(rows) + 1

                # checking if gemail exist ... 
                emails = get_record('select email from user_table')
                em = [m for m in emails]
                st.write(em)
                if email not in em: 
                    st.write('its is true')
                    if add_user(fname, lname, email, password , sex.lower() , int(age) , booking_id.lower()):
                        status_message(False, 'Successful...')
                        switch_page_button.switch_page("login")
                    else : 
                        status_message(True, 'An Error Occoure')
                else:
                    status_message(True, 'Email Already Used...')
            else : 
                status_message(True, 'Password Not Matching')
            
        else: 
            status_message(True, 'Please fill the field complete')

    else: 
        status_message(True, 'Invalid Email Addresss')

# col_two.checkbox('Remember Me?', value=True)


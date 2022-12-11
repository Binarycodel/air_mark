import streamlit as st 
from streamlit_extras import switch_page_button
# import database as db
import streamlit as st
import mysql.connector


st.set_page_config(page_title="signup" , page_icon='📈')

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
        cur 
        return cur.fetchall()




@st.experimental_memo(ttl=600)
def add_user( first_name, second_name, email, password, sex, age):
    query = '''INSERT INTO airmark_databases.user( first_name, second_name, email, password, sex, age ) VALUES(%s, %s, %s, %s ,%s, %s)'''
    isSuccess = False 
    with conn.cursor() as curs: 
        # (id, first_name, second_name, email, password)
        curs.execute(query , ( first_name, second_name, email, password , sex, age))
    
        isSuccess = True
        print('execution successful')
    return isSuccess

# ========================== END OF DATABASE CONNECTION ===============================

# defining global parameter
login_status = False


# app title
st.title('Air Remark Management System')


# widgets
st.header('Register here ')


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
email = email1.text_input("Email")
password = pass1.text_input('Password', type='password')
password2 = pass2.text_input('Confirm Password', type='password')

sex = sex_panel.selectbox('Select Gender' , ('Male', 'Femail'))
age = age_panel.text_input("Enter Age")


col_one , col_two = st.columns([1,1])

sign_button = col_two.button('Back')
if sign_button: 
    switch_page_button.switch_page("login")



regitem  = [fname, lname, email, password, password2]

if col_one.button('Register'):
    # validate data suply 
    print(regitem)
    if "" not in regitem: 
        if password2 == password : 
            rows = get_record("SELECT * from user;")
            id = len(rows) + 1

            # checking if gemail exist ... 
            emails = get_record('select email from user')
            em = [m for m in emails]
            st.write(em)
            if email not in em: 
                st.write('its is true')
                if add_user(fname, lname, email, password , sex.lower() , int(age)):
                    status_message(False, 'Successful...')
                    switch_page_button.switch_page("login")
                else : 
                    status_message(True, 'An Error Occoure')
            else:
                status_message(True, 'Email Already Used...')
        else : 
            status_message(True, 'Please use the same password')
        
    else: 
        status_message(True, 'Please fill the field complete')


# col_two.checkbox('Remember Me?', value=True)

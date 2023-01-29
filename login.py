import streamlit as st 
from streamlit_extras import switch_page_button
import databases as db

st.set_page_config(initial_sidebar_state="collapsed")
# defining global parameter
login_status = False

database = db.Database()
database.create_user_table()
database.create_admin_table()
database.check_admin_default()
database.create_comment_table()
database.create_airlinestaff_table()

no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

# hide_menu_style = """
#         <style>
#         #MainMenu {visibility: hidden;}
#         </style>
#         """
# st.markdown(hide_menu_style, unsafe_allow_html=True)


# app title
st.title('AirMark Management System')

with open('style.css') as css: 
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


if 'user'  in st.session_state:
    switch_page_button.switch_page("home")

if 'admin' in st.session_state: 
    switch_page_button.switch_page('home')


# widgets
st.header('Login')


# ==============  DATABSE CONNECTIVITIES ======================

def get_record(query):
    return database.custom_query(query)
    

def add_user(id, first_name, second_name, email, password,sex, age):
    database.insert_to_user_table(first_name, second_name, email, password, sex, age)
    st.write('record addesd successfull')


# ========================== END OF DATABASE CONNECTION ===============================


user_page , admin_page, Airline_staff = st.tabs(['Users' , 'Admin', 'Ariline-Staff'])



# status message 
def status_message(status=False, message='error'):
    if status:
        status_l1.error(message)
    else:
        status_l1.success(message)

def status_message2(status=False, message='error'):
    if status:
        lay_one.error(message)
    else:
        lay_one.success(message)

with Airline_staff:
    # layout definations (three columns)
    status_l1, statusl_l2 = st.columns([2,1])
    eml, eml2 = st.columns([2,1])
    pass1, pass2 = st.columns([2,1])


    email = eml.text_input("Staff ID")
    password = pass1.text_input('Enter Password', type='password' , key='pm')

    col_one , col_two = st.columns([1,1])

    sign_button = col_two.button('Sign Up', key='staff')
    if sign_button: 
        switch_page_button.switch_page("staff")




    if col_one.button('login', key='staff_log'):
        # validate credentials 
        rows = get_record("SELECT staff_name,staff_id, email, airline, password  from airlinestaff_table;")
        # st.write(rows)
        # st.write(rows)
        if rows == None : 
            st.warning("No record Found")
        else :

            for d in rows: 
                st_name, st_id , my_email , arline , passs= d[0], d[1], d[2] , d[3] , d[4]
                full_name = f'{st_name} {st_id}'
                # st.write(f'{st_id} {email} {passs} {password}')
                if st_id.strip() == email.strip() and password.strip() == passs.strip(): 
                    
                    #  creating session 
                    if  'staff_id' not in st.session_state: 
                        st.session_state['staff_name'] = st_name
                        st.session_state['staff_id'] = st_id
                        st.session_state['staff_email'] = email
                        st.session_state['airline'] = arline
                    
                    switch_page_button.switch_page("staff_menu")
            else: 
                status_message(True, 'Wrong Email or Password')
                # st.write('something wrong')


    col_two.checkbox('Remember Me?', value=True, key='check') 



with user_page: 

    # layout definations (three columns)
    status_l1, statusl_l2 = st.columns([2,1])
    email1, email2 = st.columns([2,1])
    pass1, pass2 = st.columns([2,1])


    email = email1.text_input("Enter Email", key='em')
    password = pass1.text_input('Enter Password', type='password')

    col_one , col_two = st.columns([1,1])

    sign_button = col_two.button('Sign Up')
    if sign_button: 
        switch_page_button.switch_page("signup")



    if col_one.button('login'):
        # validate credentials 
        rows = get_record("SELECT email, password, sex, first_name, second_name  from user_table;")
        # st.write(rows)
        # st.write(rows)
        if rows == None : 
            st.warning("No record Found")
        else :

            for d in rows: 
                username, pas, sex , fn , sn = d[0], d[1], d[2] , d[3] , d[4]
                full_name = f'{fn} {sn}'
                if email.strip() == username.strip() and password.strip() == pas.strip(): 
                    
                    #  creating session 
                    if  'user' not in st.session_state: 
                        st.session_state['user'] = username
                        st.session_state['sex'] = sex
                        st.session_state['email'] = email
                        st.session_state['full_name'] = full_name
                    
                    switch_page_button.switch_page("Home")
            else: 
                status_message(True, 'Wrong Email or Password')
                # st.write('something wrong')


    col_two.checkbox('Remember Me?', value=True)


with admin_page:
     # layout definations (three columns)
    lay_one, lay_two= st.columns([2,1])
    em1, em2 = st.columns([2,1])
    pa1, pa2 = st.columns([2,1])


    email2 = em1.text_input("Email")
    password2 = pa1.text_input('Password', type='password')

    col_1 , col_2 = st.columns([1,1])

    # sign_button = col_two.button('Sign Up')
    # if sign_button: 
    #     switch_page_button.switch_page("signup")

    if col_1.button('Signin'):
        # validate credentials 
        rd = get_record("SELECT email, password  from admin;")
        # st.write(rows)
        if rd == None : 
            st.warning("No record Found")
        else :

            for d in rd: 
                em, ps = d[0], d[1]
                # st.write(f'{em==email2} {ps==password2}')
                if em.strip() == email2.strip().lower() and ps.strip() == password2.strip().lower(): 
                   
                    st.write('WRITE UP......')
                    #  creating session 
                    if  'admin' not in st.session_state: 
                        st.session_state['admin'] = em                   
                    switch_page_button.switch_page("home")
            else: 
                st.error('wrong login credentials')
                # st.write('something wrong')


    # col_2.checkbox('Remember Me ?', value=True)

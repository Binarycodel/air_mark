from streamlit_extras import switch_page_button
import streamlit as st
# st.set_page_config(initial_sidebar_state="collapsed")


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


with open('style.css') as css: 
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


if 'user' in st.session_state:
    del st.session_state['user']
    del st.session_state['sex']
    del st.session_state['email']

if 'admin' in st.session_state:
    del st.session_state['admin']

if 'staff_id' in st.session_state:
    del st.session_state['staff_name']
    del st.session_state['staff_id']
    del st.session_state['staff_email']
    del st.session_state['airline']

switch_page_button.switch_page("login")
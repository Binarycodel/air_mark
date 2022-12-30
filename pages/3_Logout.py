from streamlit_extras import switch_page_button
import streamlit as st
# st.set_page_config(initial_sidebar_state="collapsed")



hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


with open('style.css') as css: 
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)


if 'user' in st.session_state:
    del st.session_state['user']
    del st.session_state['sex']

if 'admin' in st.session_state:
    del st.session_state['admin']

switch_page_button.switch_page("login")
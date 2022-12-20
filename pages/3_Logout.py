from streamlit_extras import switch_page_button
import streamlit as st


if 'user' in st.session_state:
    del st.session_state['user']
    del st.session_state['sex']
switch_page_button.switch_page("login")
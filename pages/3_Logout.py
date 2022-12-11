from streamlit_extras import switch_page_button
import streamlit as st


del st.session_state['user']
switch_page_button.switch_page("login")
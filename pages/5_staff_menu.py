
import streamlit as st
import databases as db 
import pandas as pd
import numpy as np 
from streamlit_extras import switch_page_button
import matplotlib.pyplot as plt


database = db.Database()

ad_lay1 , ad_lay2 = st.columns([4, 2])
logout_bt = ad_lay2.button('logout')
ad_lay1.header(f'Staff Page') 
# ==========================  IF ADMIN LOGIN ========================
# report_tab , settings_tab = st.tabs(['Report' , 'Settings'])


# st.set_page_config(initial_sidebar_state='collapsed')


no_sidebar_style = """
    <style>
        div[data-testid="stSidebarNav"] {display: none;}
    </style>
"""
st.markdown(no_sidebar_style, unsafe_allow_html=True)

if logout_bt: 
    switch_page_button.switch_page('logout')

st.subheader(f' Welcome {st.session_state.staff_name}')


com_data  = database.custom_query('select * from comment_table')
# st.write(com_data)
df = pd.DataFrame(com_data, columns=['AIRLINE', 'BOOKING ID' , 'ROUTE', 'COMMNET', 'SENTIMENT'])
# st.table(df)
positive_sent = df['SENTIMENT'][df.SENTIMENT == 'Positive']
negative_sent =  df['SENTIMENT'][df.SENTIMENT == 'Negative']

if positive_sent.empty: 
    
    pos_size = 0
else: 
    pos_size = len(positive_sent)

if negative_sent.empty: 
    neg_size = 1
else: 
    neg_size = len(negative_sent)

X = [pos_size , neg_size]
st.subheader('Statistic Distribution')
sta1 , sta2 =  st.columns([2,2])

if (pos_size >= 2) and (neg_size >= 1): 
    fig, ax = plt.subplots()
    _ , txt , _ = ax.pie(x=X , labels=['Positive', 'Negative'] , autopct='%1.2f%%', colors=['green', 'orange'])
    sta1.pyplot(fig)
    # ==========================

    fig2, ax2 = plt.subplots()
    fig.set_figwidth(1)
    fig.set_figheight(2)
    ax2.bar(['Positive', 'Negative'] , X , color=['green', 'orange'])
    # txt[0].set_fontsize(3)
    # txt[1].set_fontsize(3)
    # ax.set_title('Gender Distribution Sentiment')
    # ax.set_xlabel('Gender')
    # ax.set_ylabel('Sex Count')
    sta2.pyplot(fig2)

st.subheader (f'{st.session_state.airline} Customer Review')
for damta in range(len(com_data)):
    da , bu = st.columns([4,1])
    sim_da = com_data[damta]
    airline,  b_id , rt , com , sn= sim_da[0], sim_da[1], sim_da[2], sim_da[3] , sim_da[4]

    if airline == st.session_state.airline: 
        da.markdown(f'{b_id}  ({rt}) <br>  {com[:50]} ', unsafe_allow_html=True)
        if sn =='Negative':
            bu.error(f'{sn}')
        else: 
            bu.success(f'{sn}')
        st.markdown("<hr>" , unsafe_allow_html=True)
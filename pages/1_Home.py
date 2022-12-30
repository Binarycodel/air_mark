import streamlit as st
import pandas as pd
from PIL import Image

from streamlit_extras import switch_page_button
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.figure_factory as ff
import databases as db 
from textblob import TextBlob

st.set_page_config(page_title="Home" , page_icon='📈')
is_admin = False


hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)



with open('style.css') as css: 
    st.markdown(f'<style>{css.read()}</style>', unsafe_allow_html=True)

# st.set_page_config(initial_sidebar_state="collapsed")
    
    # switch_page_button.switch_page("login")
if 'admin' in st.session_state: 
    is_admin = True
elif 'user' in st.session_state:
    user_id = st.session_state.user 
else: 
    switch_page_button.switch_page("login")
    


# ==============  DATABSE CONNECTIVITIES ======================
dataase = db.Database()
# =============================================================


if is_admin: 
    ad_lay1 , ad_lay2 = st.columns([4, 2])
    logout_bt = ad_lay2.button('logout')
    ad_lay1.header(f'Admin Page') 
    # ==========================  IF ADMIN LOGIN ========================
    report_tab , settings_tab = st.tabs(['Report' , 'Settings'])

    with report_tab: 
        import numpy as np 
        

        if logout_bt: 
            switch_page_button.switch_page('logout')

        st.subheader(f' Welcome {st.session_state.admin}')

        com_data  = dataase.custom_query('select * from comment_table')
        st.markdown('#### USER COMMENTS')
        # st.write(com_data)
        df = pd.DataFrame(com_data, columns=['AIRLINE', 'BOOKING ID' , 'ROUTE', 'COMMNET', 'SENTIMENT'])
        st.table(df)
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
            # fig.set_figwidth(1)
            # fig.set_figheight(2)
            _ , txt , _ = ax.pie(x=X , labels=['Positive', 'Negative'] , autopct='%1.2f%%' )
            # txt[0].set_fontsize(3)
            # txt[1].set_fontsize(3)
            # ax.set_title('Gender Distribution Sentiment')
            # ax.set_xlabel('Gender')
            # ax.set_ylabel('Sex Count')
            sta1.pyplot(fig)


            # ==========================

            fig2, ax2 = plt.subplots()
            fig.set_figwidth(1)
            fig.set_figheight(2)
            ax2.bar(['Positive', 'Negative'] , X , color=['green', 'blue'])
            # txt[0].set_fontsize(3)
            # txt[1].set_fontsize(3)
            # ax.set_title('Gender Distribution Sentiment')
            # ax.set_xlabel('Gender')
            # ax.set_ylabel('Sex Count')
            sta2.pyplot(fig2)

        
        with settings_tab:

            with st.form('resert_password_form'): 
                st.subheader('Reset PassCode')
                old_pass = st.text_input('Old Password')
                new_password = st.text_input('New Password')
                new_password = st.text_input('Confirm Password')
                
                credential_detail = [old_pass, new_password, new_password]

                update_buttion = st.form_submit_button('Update')

                if update_buttion: 

                    if '' not in credential_detail: 

                        if credential_detail[1] == credential_detail[2]:
                        # validate old password in the database 
                            current_p = dataase.custom_query('select password from admin')
                            c = current_p[0][0]
                            if old_pass.lower() == str(c).lower():
                                em = st.session_state.admin
                                st.write(f'email {em}')
                                if dataase.update_admin_table(em):
                                    st.success('Record Update...')
                            else: 
                                st.warning('Wrong old password')
                        else: 
                            st.error('password not macthing')
                
                    else :
                        st.warning('fill all details')    \

            
            with st.form('add_user_form'): 
                    st.subheader('Add Admin')
                    eml  = st.text_input('Email')
                    reg_code = st.text_input('Reg. Code')
                    pass_word = st.text_input('Password')
                    conf_passw = st.text_input('Confirm Password')
                    
                    cred_dtail = [eml, reg_code, pass_word, conf_passw]

                    update_buttion = st.form_submit_button('Submit')

                    if update_buttion: 

                        if '' not in cred_dtail: 

                            if cred_dtail[2] == cred_dtail[3]:
                            # validate old password in the database 
                                current_em = dataase.custom_query('select email from admin')
                                c_email = False
                                for index in range(len(current_em)):
                                    cc = current_em[index][0]
                                    if str(cc).lower() == eml.lower():
                                        c_email == True
                                        break
                                else: 
                                    c_email = False

                                if c_email : 
                                    st.warning('email in use')
                                else: 
                                    confirm = dataase.insert_into_admin_table(cred_dtail[0], cred_dtail[2], cred_dtail[1])

                                    if confirm: 
                                        st.success('Admin Added')
                                    else: 
                                        st.error('An Error Occur')


                            else: 
                                st.error('password not macthing')
                    
                        else :
                            st.warning('fill all details')  
                    
            
           
      

else: 
      # ==========================  IF USER LOGIN =======================
    st.header('user')

 


    def add_booking(email, password, reg_code):
        return dataase.insert_into_admin_table(email, password, reg_code)


    def add_comment(airportloc, booking_txt , route_txt , comment_page, polar):
        return dataase.insert_into_comment_table(airportloc, booking_txt , route_txt , comment_page, polar)
        

    # ========================== END OF DATABASE CONNECTION ===============================

    airport = pd.read_csv('datasource/ng_airports.csv')
    df = pd.read_csv('datasource/sent_data.csv')


    # ========================== loading statistic data ========


    def get_sex_statistic(df):   
        m , f =df['sex'].value_counts()
        return [m ,f] , ['male', 'female'] 


    def get_sent_statistic(df):
        sent_d = df.groupby('airline_sentiment').value_counts()
        pos = sent_d['positive'].count()
        neg = sent_d['negative'].count()
        nut = sent_d['neutral'].count()
        y = [nut, pos, neg]
        x = df.airline_sentiment.unique()
        return x, y

    def get_age_statistic(df): 
        return df['age'].unique()

    age_data = get_age_statistic(df)
    sex_data = get_sex_statistic(df)
    sentiment_data = get_sent_statistic(df)

    # ================================= END OF STATISTIC DATA ==============

    # ================ HELPER METHODS ===================
    def get_sentence_sentiment(text): 
        
        sentiment_text = ''
        polar = TextBlob(text).sentiment.polarity

        if polar < 0 :
            sentiment_text='Negative'
        elif polar == 0 : 
            sentiment_text='Neutral'
        else: 
            sentiment_text = "Positive"
            
            
        return sentiment_text, polar



    # ================= END OF HELOPER METHOD =================
    c1 , c2 = st.columns([3,1])
    # text_input('', label_visibility='collapsed', value ='Search...')
    lgout = c2.button('Signout')
    c1.markdown('## Nigeria AirMark  System.')

    if lgout: 
        switch_page_button.switch_page("logout")

    # getting user session 

    user_id = st.session_state.user

    st.write(f'Welcome {user_id}')


    # tup_list = tuple(data.iloc[index].values)

    dashboard_page , comment_page = st.tabs(['Dashboard', 'Comment'])

    # import data
    with dashboard_page:
        image = Image.open('image/flight_image.jpg')
        st.image(image, )
        # Three colums of information.... 
        col_1 , col_2, col_3 = st.columns([1,1,1])

        with col_1:
            with st.form('dist_for', clear_on_submit=True):
                st.markdown(f'# {len(airport)} Nigeria')
                st.markdown('##### Marjor Airport')
                bt = st.form_submit_button('')

        with col_2:
            data = None
            records = dataase.custom_query('select email, first_name , sex, age, booking_id from user_table')
            for record in range(len(records)):
                if records[record][0] == st.session_state.user:
                    data = records[record]
                    break
            st.write(f' Email : {data[0]}')
            st.write(f' Name : {data[1]}')
            st.write(f' Age : {data[3]}')
            st.write(f' Sex : {data[2]}')
            
        with col_3:
            st.write(f' Bookin_id : {data[4]}')

        # getting all comment on media


   

    with comment_page:
        with st.form('Reg_form', clear_on_submit=True):
            
            st.subheader('Drop Comment')

            # air_port  = pd.read_csv('datasource/ng_airports.csv')
            # airport_name = list(air_port['name'].values)
            # states = list(air_port['region_name'].values)
            # air_port_loc = list(air_port['municipality'].values)
                
            # travil_info = list()
            # for index in range(len(air_port[:30])):
            #     info = f'{airport_name[index]} ({air_port_loc[index]})' 
            #     travil_info.append(info)
            
            # print(travil_info
            airportloc = st.selectbox('AIRLINE ' , [
                'Aero (AEROLINE)',
                'Air Peace (PEACE BIRD)', 
                'Allied Air (BAMBI)',
                'Arik Air (ARIK AIR)', 
                'Azman Air (AZMAN AIR)', 
                'Dana Air (DANACO)',
                'Dornier Aviation Nigeria (DANA AIR)',
                'Green Africa Airways (GREEN AFRICA)',
                'Ibom Air (IBOM)', 
                'K-Impex Airline (KiE BIRD)', 
                'Kabo Air (KABO)', 
                'Kanem Air (KIR)', 
                'Max Air (MAX AIR)'

            ] )

            booking_txt = st.text_input('Booking id')
            route_txt = st.selectbox('Route', [
                'Abuja To kano', 
                'kwara To Jos', 
                'Enugu To Oyo', 
                'Lagos To Kaduna'
            ])
            comment = st.text_area('Comment here')

            # print(airportloc, deptment, name, comment)
            submit_but = st.form_submit_button('Submit')

            sentiment_text, polar = get_sentence_sentiment(comment)
            
            comment_data = [airportloc, booking_txt , route_txt , comment, sentiment_text]
    
            if submit_but:
                if '' not in comment_data:
                    if add_comment(comment_data[0], comment_data[1], comment_data[2], comment_data[3], comment_data[4]):
                        st.success('successfully. Thanks for the feedback')
                else: 
                    st.write('empty data find')
            

            #     
            #     else: 
            #         st.error('Not successfull. ')
        

    
    
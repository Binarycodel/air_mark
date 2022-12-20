import streamlit as st
import pandas as pd
from PIL import Image
import mysql.connector
from streamlit_extras import switch_page_button
import matplotlib.pyplot as plt
import plotly.express as px 
import plotly.figure_factory as ff
import databases as db 
from textblob import TextBlob

st.set_page_config(page_title="Home" , page_icon='📈')

if 'user' not in st.session_state:
    switch_page_button.switch_page("login")
else: 
    user_id = st.session_state.user 





hide_menu_style = """
        <style>
        #MainMenu {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# ==============  DATABSE CONNECTIVITIES ======================

dataase = db.Database()



def add_booking(location, destination, category, email):
    return dataase.insert_into_booking_table(location, destination, category, email)


def add_comment(airport, dept , comment, email, sex, sent_text):
    return dataase.insert_into_comment_table(airport, dept , comment, email,sex, sent_text)
    

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

dashboard_page , book_flight, comment_page = st.tabs(['Flight Dashboard', 'Book Flights', 'Drop Comment'])

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
        pass

    with col_3:
        pass


    

    with st.form('dist_formm', clear_on_submit=True):
        st.subheader('Sex  Distribution')
        fig, ax = plt.subplots()
        fig.set_figwidth(10)
        fig.set_figheight(5.5)
        ax.bar(sex_data[1], sex_data[0], color=['g', 'brown'])
        # ax.set_title('Gender Distribution Sentiment')
        ax.set_xlabel('Gender')
        ax.set_ylabel('Sex Count')
        st.pyplot(fig)
        bt = st.form_submit_button('')

    with st.form('dist_forms', clear_on_submit=True):
        st.subheader('Sentiment Distribution')
        fig, ax = plt.subplots()
        fig.set_figwidth(10)
        fig.set_figheight(5.5)
        ax.bar(list(sentiment_data[0]), sentiment_data[1], color=['g', 'brown' , 'r'])
        # ax.set_title('Gender Distribution Sentiment')
        ax.set_xlabel('Sentiment')
        # ax.set_ylabel('Sex Count')
        st.pyplot(fig)
        b2 = st.form_submit_button('')
            
            
    
with book_flight:
    # data  = pd.read_csv('datasource/drug_data_mini.csv')
    # st.dataframe(data)
    with st.form('dist_form', clear_on_submit=True):
        
        st.subheader('Book Flights Here')

        air_port  = pd.read_csv('datasource/ng_airports.csv')
        airport_name = list(air_port['name'].values)
        states = list(air_port['region_name'].values)
        air_port_loc = list(air_port['municipality'].values)
            
        travil_info = list()
        for index in range(len(air_port[:30])):
            info = f'{airport_name[index]} ({air_port_loc[index]})' 
            travil_info.append(info)
        
        # print(travil_info)
    

        loc = st.selectbox('DISPATCH FROM' , travil_info )
        dest = st.selectbox('TRAVELL TO', travil_info)
        cat = st.selectbox('FLIGHT CATEGORIES', ('Fisrt Class', 'Business Class', 'Economy Class'))

        submit_but = st.form_submit_button('BOOK FLIGHT')

        if submit_but:
            # def add_booking(location, destination, category, email):
            if add_booking(loc, dest, cat, user_id):
                st.success('Flight booked sucessfully (Payment And other essential stuff will be carried out manually)')
            else : 
                st.warning('Operation Not Successful')


with comment_page:
    with st.form('Reg_form', clear_on_submit=True):
        
        st.subheader('Raise Complains Based on Department')

        air_port  = pd.read_csv('datasource/ng_airports.csv')
        airport_name = list(air_port['name'].values)
        states = list(air_port['region_name'].values)
        air_port_loc = list(air_port['municipality'].values)
            
        travil_info = list()
        for index in range(len(air_port[:30])):
            info = f'{airport_name[index]} ({air_port_loc[index]})' 
            travil_info.append(info)
        
        # print(travil_info)
    

        airportloc = st.selectbox('AIRPORT ' , travil_info )

        deptment = st.selectbox('AIRPORT DEPARTMENT' , ('Medical Center', 'Postal freight services', 'Air Security Service', 'VIP & CIP', 'Passenger transportation service', 'Flight Safety and Quality Department', 'Special Transport Services'))
        name = st.text_input('Complianer Name :')
        comment = st.text_area('Comment here')

        print(airportloc, deptment, name, comment)
        submit_but = st.form_submit_button('Register')

        sentiment_text, polar = get_sentence_sentiment(comment)

        if submit_but:
            print(airportloc, deptment, name, comment, sentiment_text)
            if add_comment(airportloc, deptment, comment, user_id , st.session_state.sex, sentiment_text) : 
                st.success('successfully. Thanks for the feedback')
            else: 
                st.error('Not successfull. ')
    

    
    
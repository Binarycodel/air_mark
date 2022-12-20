import sqlite3 as sq
import streamlit as st 

class  Database: 


    def __init__(self) -> None:
        
        with sq.connect('airmark.db')  as db :
            Database.database = db
            self.data = db
            print('Database connected successfully')

# =============================================================== USER AIRMARK SECTION =========================================================

    def create_user_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS user_table(
                    first_name VARCHAR(30) NOT NULL, 
                    second_name VARCHAR(30)  NOT NULL,
                    email VARCHAR(30) PRIMARY KEY NOT NULL, 
                    password varchar(30) NOT NULL, 
                    sex VARCHAR(30) NOT NULL, 
                    age INT NOT NULL
                ); 
                '''
        self.data.execute(query)
        print('user table created succesfully.. ')

    
    def create_comment_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS comment_table(
                    airport VARCHAR(30) NOT NULL, 
                    dept VARCHAR(30)  NOT NULL,
                    comment VARCHAR(100) NOT NULL, 
                    comment_email VARCHAR(30), 
                    sex VARCHAR NOT NULL, 
                    FOREIGN KEY(comment_email) REFERENCES user_table(email) );
                '''
        self.data.execute(query)
        print('comment table created succesfully.. ')

    
    def create_booking_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS booking_table(
                    location VARCHAR(30) NOT NULL, 
                    destination VARCHAR(30)  NOT NULL,
                    category VARCHAR(30) NOT NULL, 
                    book_email VARCHAR(30) NOT NULL,
                    FOREIGN KEY(book_email) REFERENCES user_table(email)
                ) ; 
                '''
        self.data.execute(query)
        print('comment table created succesfully.. ')
    

    def insert_to_user_table(self, fn, sn, email, pwd, sex, age): 
        query = '''
                INSERT INTO user_table( first_name, second_name, email, password, sex, age ) VALUES(?, ?, ? , ? ,?, ?)
                
                '''

        self.data.execute(query , (fn, sn, email, pwd, sex, age))
        self.data.commit()
        print('user added successfully')

    def validate_user_record(self): 
        query = ''' SELECT email, password , sex  FROM user_table  ;'''

        data  = self.data.execute(query)
        print(data)
        return data.fetchall()

# =============================================================== END USER BLOCKCHAIN SECTION =========================================================


    def insert_into_booking_table(self, location, destination, category, email): 
        query = '''
                INSERT INTO booking_table VALUES (?, ?, ?, ? )                
                '''
        self.data.execute(query, (location, destination, category, email))
        self.data.commit()
        return True


    def insert_into_comment_table(self, airport, dept , comment, email , sex, sent_text): 
        query = '''INSERT INTO comment_table(airport, dept , comment, comment_email, sex, sent_polarity) VALUES(?,?,?,?,?, ?) '''
        self.data.execute(query, (airport, dept , comment, email, sex, sent_text))
        self.data.commit()
        return True

    

    def custom_query(self, query):

        data  = self.data.execute(query)
        return data.fetchall()


   
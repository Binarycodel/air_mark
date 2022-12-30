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
                    age INT NOT NULL, 
                    booking_id varchar(30) not null
                ); 
                '''
        self.data.execute(query)
        print('user table created succesfully.. ')

    
    def create_comment_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS comment_table(
                    airport VARCHAR(50) NOT NULL, 
                    booking_id VARCHAR(30)  NOT NULL,
                    route VARCHAR(50) NOT NULL, 
                    comment TEXT(400), 
                    polarity VARCHAR(30) NOT NULL
                    )
                '''
        self.data.execute(query)
        print('comment table created succesfully.. ')
    
    def create_admin_table(self):
        query = '''
                CREATE TABLE IF NOT EXISTS admin(
                    email VARCHAR(30) NOT NULL, 
                    password VARCHAR(30)  NOT NULL, 
                    reg_code varchar(30), 
                    primary key(reg_code)

                ) ; 
                '''
        self.data.execute(query)
        print('comment table created succesfully.. ')

    def check_admin_default(self):
        qr = """ select * from admin"""
        qr_insert = 'insert into admin value(?,?,?)'
        record = self.data.execute(qr).fetchall()
        
        if len(record) == 0: 
            self.insert_into_admin_table('admin', 'admin' , 'admin001')
        else: 
            pass

    

    def insert_to_user_table(self, fn, sn, email, pwd, sex, age, booking_id): 
        query = '''
                INSERT INTO user_table( first_name, second_name, email, password, sex, age, booking_id ) VALUES(?, ?, ? , ? ,?, ?, ?)
                
                '''

        self.data.execute(query , (fn, sn, email, pwd, sex, age, booking_id))
        self.data.commit()
        print('user added successfully')

    def validate_user_record(self): 
        query = ''' SELECT email, password , sex  FROM user_table  ;'''

        data  = self.data.execute(query)
        print(data)
        return data.fetchall()

# =============================================================== END USER BLOCKCHAIN SECTION =========================================================


    def insert_into_admin_table(self, email, password, reg_code ): 
        query = '''
                INSERT INTO admin VALUES (?, ?, ?)                
                '''
        self.data.execute(query, (email, password, reg_code))
        self.data.commit()
        st.write('Completed')
        return True


    def update_admin_table(self, password , em): 
        query = '''
                UPDATE  admin  SET password==? WHERE email==?                
                '''
        self.data.execute(query, (password, em))
        self.data.commit()
        return True


    def insert_into_comment_table(self, airportloc, booking_txt , route_txt , comment_page, polar): 
        query = '''INSERT INTO comment_table VALUES (?, ?, ?, ?, ?) '''
        self.data.execute(query, (airportloc, booking_txt , route_txt , comment_page, polar))
        self.data.commit()
        return True

    
    def custom_query(self, query):

        data  = self.data.execute(query)
        return data.fetchall()


   
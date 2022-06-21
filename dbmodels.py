# databasemodels.py
import os
import sqlite3

# Class database gives access to methods used to access sqllite databases

class database:

    # Method returns all user info from user_database
    def checkdb(self):

        # Connect to file
        conn = sqlite3.connect('user_database.sqlite') 
        # Set cursor
        c = conn.cursor()
        # SQL Query
        c.execute("SELECT username, password FROM userinfo")
        # Get results
        print(c.fetchall())

    # Method returns all user info from ban_database
    #
    #

    # Method checks if user_database exists and if not creates it
    def checkfordb(self):

        if os.path.exists('user_database.sqlite'):
            print ("Database exists!")
            return
        else:
            # Create db
            conn = sqlite3.connect('user_database.sqlite') 
            c = conn.cursor()

            c.execute('''CREATE TABLE IF NOT EXISTS "userinfo"([username] TEXT, [password] TEXT)''')

            conn.commit()
            
            print ("User Database created!")

    # Method checks if ban_database exists and if not creates it
    #
    #


    # Method checks if user login credentials are valid
    def checklogin(self, username, password):    

        conn = sqlite3.connect('user_database.sqlite')
        c = conn.cursor()
        statement = (f'''SELECT username from "userinfo" WHERE username="{username}" AND password = "{password}"''')
        c.execute(statement)
        if not c.fetchone():  # An empty result evaluates to False.
            print("Login failed")
        else:
            print("Welcome")

    # Method checks if user exists in ban_database
    #
    #

    # Method to store new user credentials
    def storelogin(self, username, password):

        conn = sqlite3.connect('user_database.sqlite') 
        c = conn.cursor()    
        c.execute(f'''INSERT INTO "userinfo"(username, password) VALUES
                    ("{username}","{password}")''')

        conn.commit()       

    # Method to store user info in ban_database
    #
    #

db = database()
# db.checkfordb()
db.checklogin('bot', 'botpass2')
# db.checkdb()
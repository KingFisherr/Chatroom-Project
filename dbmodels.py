# databasemodels.py
import os
import sqlite3

# We will implement multiple functions that allow us to use a sqllite database as a means to store encrypted user credentials

def checkfordb():
    if os.path.exists('user_database.db'):
        print ("exist")
    else:
        # Create db
        conn = sqlite3.connect('user_database') 
        c = conn.cursor()

        c.execute('''CREATE TABLE IF NOT EXISTS userinfo([username] TEXT, [password] TEXT)''')

        conn.commit()
        #of call the sql file
#def checklogin(user,password):

#def storelogin(user,password):

checkfordb()
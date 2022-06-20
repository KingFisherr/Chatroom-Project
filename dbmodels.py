# databasemodels.py
import os
import sqlite3

# We will implement multiple functions that allow us to use a sqllite database as a means to store encrypted user credentials


class database:
    def checkdb(self):
        conn = sqlite3.connect('user_database.sqlite') 
        c = conn.cursor()
        c.execute("SELECT username, password FROM userinfo")
        print(c.fetchall())

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

    #def checklogin(self, username, password):
      
    def storelogin(self, username, password):
        conn = sqlite3.connect('user_database.sqlite') 
        c = conn.cursor()    

        c.execute(f'''INSERT INTO "userinfo"(username, password) VALUES
                    ("{username}","{password}")''')

        conn.commit()       

# db = database()
# db.checkfordb()
# db.storelogin('bot', 'botpass')
# db.checkdb()
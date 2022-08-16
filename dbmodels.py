# databasemodels.py
import os
import sqlite3
import bcrypt

# Class database gives access to methods used to access sqllite databases

class database:
    
    def deleteRecord(self):
        conn = sqlite3.connect('user_database.sqlite') 
        c = conn.cursor()
        
        # Deleting all records 
        # f'DELETE FROM userinfo where username = {name}'
        sql_delete_query = "DELETE FROM userinfo"
        c.execute(sql_delete_query)
        conn.commit()
        print("Record deleted successfully ")
        c.close()

    # Method returns all user info from user_database
    def getuserinfo(self):

        # Connect to file
        conn = sqlite3.connect('user_database.sqlite') 
        # Set cursor
        c = conn.cursor()
        # SQL Query
        c.execute("SELECT username, password FROM userinfo")
        # Get results
        print(c.fetchall())

    # Method returns all user info from ban_database
    def getbaninfo(self):

        # Connect to file
        conn = sqlite3.connect('ban_database.sqlite') 
        # Set cursor
        c = conn.cursor()
        # SQL Query
        c.execute("SELECT username, ip FROM banned")
        # Get results
        print(c.fetchall())

    # Method checks if a given database exists and if not creates it
    def checkfordb(self, dbfile):
        #dbfile is name of database file
        if os.path.exists(dbfile):
            # print ("Database exists!")
            return
        else:
            # Create db
            conn = sqlite3.connect(dbfile)
            c = conn.cursor()

            if dbfile == 'user_database.sqlite':
                c.execute('''CREATE TABLE IF NOT EXISTS "userinfo"([username] TEXT, [password] TEXT)''')
            elif dbfile == 'ban_database.sqlite':
                c.execute('''CREATE TABLE IF NOT EXISTS "banned"([username] TEXT, [ip] TEXT)''')

            conn.commit()
            
            print ("Database created!")

    # Method checks if user login credentials are valid against plain text password
    def checklogin(self, username, password):    

        conn = sqlite3.connect('user_database.sqlite')
        c = conn.cursor()
        statement = (f'''SELECT username from "userinfo" WHERE username="{username}" AND password = "{password}"''')
        c.execute(statement)
        if not c.fetchone():  # An empty result evaluates to False.
            return False
        else:
            return True
            
    # Method checks if user login credentials are valid against a bcrypt hash
    def checkloginHash(self, username, password):
        
        conn = sqlite3.connect('user_database.sqlite')
        c = conn.cursor()
        statement = (f'''SELECT password from "userinfo" WHERE username="{username}"''')
        c.execute(statement)
        row = c.fetchone()
        if not row:  # An empty result evaluates to False.
            return False
        else:
            hashed = str(row[0])
            if bcrypt.checkpw(password.encode(), hashed.encode()):
               #print (f'Hashed Pass: {hashed}')
               return True
            else:
               return False
                
    # Method checks if user exists in ban_database
    def checkban(self, username):    

        conn = sqlite3.connect('ban_database.sqlite')
        c = conn.cursor()
        statement = (f'''SELECT username from "banned" WHERE username="{username}"''')
        c.execute(statement)
        if not c.fetchone():  # An empty result evaluates to False.
            return False
        else:
            return True

    # # Method checks if user exists in ban_database (via IP ONLY)
    # def checkban(self, ip):    

    #     conn = sqlite3.connect('ban_database.sqlite')
    #     c = conn.cursor()
    #     statement = (f'''SELECT username from "banned" WHERE ip = "{ip}"''')
    #     c.execute(statement)
    #     if not c.fetchone():  # An empty result evaluates to False.
    #         return False
    #     else:
    #         return True

    # Method to store new user credentials
    def storeuserinfo(self, username, password):

        conn = sqlite3.connect('user_database.sqlite') 
        c = conn.cursor()    
        c.execute(f'''INSERT INTO "userinfo"(username, password) VALUES
                    ("{username}","{password}")''')

        conn.commit() 
        return      

    # Method to store user info in ban_database
    def storebaninfo(self, username, ip):

        conn = sqlite3.connect('ban_database.sqlite') 
        c = conn.cursor()    
        c.execute(f'''INSERT INTO "banned"(username, ip) VALUES
                    ("{username}","{ip}")''')

        conn.commit()   

    # Method to check if a specific username exist in user_info
    def checkUsername(self, username):
        conn = sqlite3.connect('user_database.sqlite')
        c = conn.cursor()
        statement = (f'''SELECT username from "userinfo" WHERE username="{username}"''')
        c.execute(statement)
        if not c.fetchone():  # An empty result evaluates to False.
            return False
        else:
            return True        

#'user_database.sqlite'
# db = database()
# db.deleteRecord()
# db.getuserinfo()
# if db.checklogin("plu", "seed"):
#     print ("yes")
# else:
#     print ("no")
# # db.checkfordb('ban_database.sqlite')

# db.storebaninfo("justforfun@", "ipaddress2")
# # # db.checkban("justforfun@","ipaddress2")

# db.getbaninfo()

# #db.checklogin('bot', 'botpass2')
# # db.checkdb()
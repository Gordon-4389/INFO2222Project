import sqlite3

# This class is a simple handler for all of our SQL database actions
# Practicing a good separation of concerns, we should only ever call 
# These functions from our models

# If you notice anything out of place here, consider it to your advantage and don't spoil the surprise

class SQLDatabase():
    '''
        Our SQL Database

    '''

    # Get the database running
    def __init__(self, database_arg="user1.db"):
        self.conn = sqlite3.connect(database_arg)
        self.cur = self.conn.cursor()

    # SQLite 3 does not natively support multiple commands in a single statement
    # Using this handler restores this functionality
    # This only returns the output of the last command
    def execute(self, sql_string):
        out = None
        for string in sql_string.split(";"):
            try:
                out = self.cur.execute(string)
            except:
                pass
        return out

    # Commit changes to the database
    def commit(self):
        self.conn.commit()

    #-----------------------------------------------------------------------------
    
    # Sets up the database
    # Default admin password
    def database_setup(self, admin_password='admin'):

        # Clear the database if needed
        self.execute("DROP TABLE IF EXISTS Users")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            admin INTEGER DEFAULT 0,
            salt TEXT
            friends TEXT
            public_key TEXT
        )""")

        self.commit()

        # Message Logs (encrypted)
        self.execute("""CREATE TABLE Messages(
            sender TEXT,
            receiver TEXT,
            message TEXT 
        )""")
        self.commit()

        # Add our admin user
        self.add_user('admin', admin_password, '0000', admin=1)

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, salt, public_key_str, admin=0):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id}, '{username}', '{password}', {admin}, '{salt}', '{public_key}')
            """

        sql_cmd = sql_cmd.format(id=0, username=username, password=password, salt=salt, admin=admin, public_key=public_key_str)

        self.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------

    # Get friend_list from a user in Table Users
    def get_friends(self, username):
        sql_query = """
                SELECT friends
                FROM Users
                WHERE username = '{username}'
            """

        # Check if user exists
        self.execute(sql_query)

        # Return result as a form of a list
        result = self.cur.fetchone()[0]
        print(result)
        friend_list = result.split(",")
        print(friend_list)
        
        return friend_list



    #-----------------------------------------------------------------------------
    # Add Friend to user
    def add_friend(self, username, friend):
        # Query if friend already exists
        friend_list = self.get_friends(username)

        # If true: do nothing, if false insert friend into friend list
        if friend not in friend_list:
            friend_list.append(friend)
            to_insert = ","
            to_insert.join(friend_list)
            print(to_insert)

            # replace friend_list entry
            sql_cmd = """
                UPDATE Users
                SET friends = '{friends}'
                WHERE username = '{username}' 
            """

            sql_cmd = sql_cmd.format(username=username, friends=to_insert)
            self.cur.execute(sql_cmd)
            self.commit()

        

        return



    #-----------------------------------------------------------------------------
    def get_salt(self, username):
        sql_query = """
                SELECT salt
                FROM Users
                WHERE username = '{username}'
            """
        
        sql_query = sql_query.format(username=username)

        self.cur.execute(sql_query)
        
        s = self.cur.fetchone()[0]
        # print(s[0])
        # return curs.fetchone()
        return s


    def get_user(self):
        sql_query = """
                SELECT username
                FROM Users
            """
        
        # sql_query = sql_query.format(username=username)

        self.cur.execute(sql_query)
        
        s = self.cur.fetchall()
        return_list = []
        i = 0
        
        while i < len(s):
            return_list.append(s[i][0])
            i+=1
        
        return return_list 
     #-----------------------------------------------------------------------------
    # Check login credentials
    def check_credentials(self, username, password):
        sql_query = """
                SELECT username, password
                FROM Users
                WHERE username = '{username}' AND password = '{password}'
            """

        sql_query = sql_query.format(username=username, password=password)

        
        self.cur.execute(sql_query)
        to_compare = self.cur.fetchone()

        if to_compare == None:
            return False
        elif to_compare[0] == username and to_compare[1] == password:
            return True
        else:
            return False
        # # If our query returns
        # print(self.cur.fetchone())
        # if self.cur.fetchone():
        #     return True
        # else:
        #     return False

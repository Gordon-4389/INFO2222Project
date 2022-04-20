import sqlite3
import hashlib

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
        self.execute("DROP TABLE IF EXISTS Encrypted")
        self.commit()

        # Create the users table
        self.execute("""CREATE TABLE Users(
            Id INT,
            username TEXT,
            password TEXT,
            salt TEXT,
            publickey TEXT
        )""")

        self.commit()

        # Message Logs (encrypted)
        self.execute("""CREATE TABLE Encrypted(
            receiver TEXT,
            ciphermessages TEXT 
        )""")
        self.commit()

        # Add our admin user
        salt = '0000'
        admin_pwd = hashlib.sha256((salt+admin_password).encode()).hexdigest()
        self.add_user('admin', admin_pwd, salt, "ko")
        self.commit()

    #-----------------------------------------------------------------------------
    # User handling
    #-----------------------------------------------------------------------------

    # Add a user to the database
    def add_user(self, username, password, salt, public_key_str):
        sql_cmd = """
                INSERT INTO Users
                VALUES({id},'{username}', '{password}', '{salt}', '{public_key}')
            """
        query_num_users = """
                SELECT COUNT(*)
                FROM Users
            """
        self.cur.execute(query_num_users)
        num_users = self.cur.fetchone()[0]
        this_user_id = num_users
        # print(num_users)

        sql_cmd = sql_cmd.format(id=this_user_id, username=username, password=password, salt=salt,  public_key=public_key_str)
        # print(public_key_str)
        self.cur.execute(sql_cmd)
        self.commit()
        return True

    #-----------------------------------------------------------------------------
    def get_salt(self, username):
        sql_query = """
                SELECT salt
                FROM Users
                WHERE username = '{username}'
            """
        
        sql_query = sql_query.format(username=username)
        print(username)
        self.cur.execute(sql_query)
        try:
            salt = self.cur.fetchone()[0]
            # print(s)
        except:
            return None
        return salt


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
    # Check login credentials (check password database match with username)
    def check_credentials(self, username, password):
        sql_query = """
                SELECT username, password, salt
                FROM Users
                WHERE username = '{username}'
            """

        sql_query = sql_query.format(username=username)

        
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
<<<<<<< Updated upstream

=======
    
    
>>>>>>> Stashed changes
    #-----------------------------------------------------------------------------
    # Get ciphertexts
    def get_user_cipertexts(self, user):
        ciphertexts = """
                SELECT ciphermessages
                FROM Encrypted
                WHERE receiver = '{username}'
            """
        ciphertexts = ciphertexts.format(username=user)
        self.cur.execute(ciphertexts)
        message_list = self.cur.fetchall()
        print(message_list)
        # senders = """
        #         SELECT sender
        #         FROM Encrypted
        #         WHERE receiver = '{username}'
        #     """.format(username=user)
        # self.cur.execute(senders)
        # sender_list = self.cur.fetchall()
        # print(sender_list)
        return message_list
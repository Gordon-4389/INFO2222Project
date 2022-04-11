'''
    Our Model class
    This should control the actual "logic" of your website
    And nicely abstracts away the program logic from your page loading
    It should exist as a separate layer to any database or data structure that you might be using
    Nothing here should be stateful, if it's stateful let the database handle it
'''
import view
import random
# from no_sql_db import database
from sql import SQLDatabase
import hashlib
# from run import manage_db

# Initialise our views, all arguments are defaults for the template
page_view = view.View()

#-----------------------------------------------------------------------------
# Index
#-----------------------------------------------------------------------------

def index():
    '''
        index
        Returns the view for the index
    '''
    return page_view("index")

#-----------------------------------------------------------------------------
# Register
#-----------------------------------------------------------------------------

def register_form():
    return page_view("register")

def register_check(username, password, public_key):
    sql_db = SQLDatabase('user1.db')
    # generate the salt
    salt = str(random.randint(0, 1023)) + username
    # combine the salt with password
    salt_w_password = salt + password
    # hash pwd
    hashed_password = hashlib.sha256(salt_w_password.encode()).hexdigest()
    # print(username)
    sql_db.add_user(username, hashed_password, salt, public_key)
    # print("hello")
    sql_db.commit()
    # print(hashed_password)
    # print(tre)
    return page_view("valid", name=username)
    # do the database insert here
#-----------------------------------------------------------------------------
# Login
#-----------------------------------------------------------------------------

def login_form():
    '''
        login_form
        Returns the view for the login_form
    '''
    return page_view("login")

#mkmk
#-----------------------------------------------------------------------------

# Check the login credentials
def login_check(username, password):
    '''
        login_check
        Checks usernames and passwords

        :: username :: The username
        :: password :: The password

        Returns either a view for valid credentials, or a view for invalid credentials
    '''

    # By default assume good creds
    login = True

    # if database.search_table("users", "username", username) == None: # Incorrect Username
    #     err_str = "Incorrect Username!!!"
    #     login = False

    # # Hash magic on password here & add salt
    # if database.search_table("users", "password", password) == None: # Incorrect pwd
    #     err_str = "Incorrect Password"
    #     login = False
    sql_db = SQLDatabase('user1.db')

    salt = str(random.randint(0, 1023)) + username
    # getting the salt of this username
    salt = sql_db.get_salt(username)
    if salt == None:
        return page_view("invalid", reason="error")
    # print(salt)
    # combine the salt with password
    salt_w_password = salt + password
    # hash pwd
    hashed_password = hashlib.sha256(salt_w_password.encode()).hexdigest()
    # print(hashed_password)

    

    if sql_db.check_credentials(username, hashed_password) == False:
        err_str = "Incorrect password"
        login = False
    
    
    # if username != "admin": # Wrong Username
    #     err_str = "Incorrect Username"
    #     login = False
    
    # if password != "password": # Wrong password
    #     err_str = "Incorrect Password"
    #     login = False
        
    if login: 
        friendlist = sql_db.get_user()
        # print(friendlist)
        # a = ','.join(friendlist)
        # print(a)

        
        return page_view("login_valid", name=username, list=friendlist)
    else:
        return page_view("invalid", reason=err_str)

    
#-----------------------------------------------------------------------------
# Send message
#-----------------------------------------------------------------------------
def mess_form():
    return page_view("message_send")

def send_mess(receiver, message):
    # ecrypt mess here and then store it in the database
    return page_view("send_result", name=receiver)

#-----------------------------------------------------------------------------
# See incoming message
#-----------------------------------------------------------------------------
def incoming():
    # get list of message here
    return page_view("incoming")

#-----------------------------------------------------------------------------
# About
#-----------------------------------------------------------------------------

def about():
    '''
        about
        Returns the view for the about page
    '''
    return page_view("about", garble=about_garble())



# Returns a random string each time
def about_garble():
    '''
        about_garble
        Returns one of several strings for the about page
    '''
    garble = ["leverage agile frameworks to provide a robust synopsis for high level overviews.", 
    "iterate approaches to corporate strategy and foster collaborative thinking to further the overall value proposition.",
    "organically grow the holistic world view of disruptive innovation via workplace change management and empowerment.",
    "bring to the table win-win survival strategies to ensure proactive and progressive competitive domination.",
    "ensure the end of the day advancement, a new normal that has evolved from epistemic management approaches and is on the runway towards a streamlined cloud solution.",
    "provide user generated content in real-time will have multiple touchpoints for offshoring."]
    return garble[random.randint(0, len(garble) - 1)]


#-----------------------------------------------------------------------------
# Debug
#-----------------------------------------------------------------------------

def debug(cmd):
    try:
        return str(eval(cmd))
    except:
        pass


#-----------------------------------------------------------------------------
# 404
# Custom 404 error page
#-----------------------------------------------------------------------------

def handle_errors(error):
    error_type = error.status_line
    error_msg = error.body
    return page_view("error", error_type=error_type, error_msg=error_msg)
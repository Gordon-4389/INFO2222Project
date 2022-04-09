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
# RSA encryption
Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

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

def register_check(username, password):
    sql_db = SQLDatabase('user1.db')
    # generate the salt
    salt = str(random.randint(0, 1023)) + username
    # combine the salt with password
    salt_w_password = salt + password
    # hash pwd
    hashed_password = hashlib.sha256(salt_w_password.encode()).hexdigest()
    sql_db.add_user(username, hashed_password, salt)
    sql_db.commit()
    print(hashed_password)
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

    # salt = str(random.randint(0, 1023)) + username
    # getting the salt of this username
    salt = sql_db.get_salt(username)
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
        return page_view("valid", name=username)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# Friend list
#-----------------------------------------------------------------------------
# Display Friend List
# def display_friends(username):
#     '''
#         display_friends
#         Display friends of user

#         :: username :: The username of user

#         Return a friend list of user (page view)
#     '''
#     sql_db = SQLDatabase('user1.db')
#     friends = sql.get_friends(username)

#     return #page_view("friends", list=friends)


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
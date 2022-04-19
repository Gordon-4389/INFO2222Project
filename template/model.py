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
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto import Random

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

    if username is "" or password is "":
        
    sql_db = SQLDatabase('user1.db')

    # Random Salt Generation and shuffle it twice
    salt = str(random.randint(0000, 9999)) + username
    rand_salt = ''.join(random.sample(salt,len(salt)))
    rand_salt = ''.join(random.sample(rand_salt,len(rand_salt)))
    # combine the salt with password
    salt_w_password = rand_salt + password
    # hash password
    hashed_password = hashlib.sha256(salt_w_password.encode()).hexdigest()

    # Key Generation
    private_key = RSA.generate(2048, Random.new().read)
    public_key = private_key.public_key()

    # Add user into database
    pub_key_db = convert_pub_key_to_str(public_key)
    # print(pub_key_db)
    # print(username, hashed_password, rand_salt, pub_key_db)
    sql_db.add_user(username, hashed_password, rand_salt, pub_key_db)
    sql_db.commit()
    # print(hashed_password)
    # print(tre)

    return page_view("valid", name=username)

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
    # sql_db.execute("SELECT * FROM Users"))
    # pirnt(sql_db.cur.fetchall())
    # print(username)
    # print(password)

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
        err_str = "Incorrect username or password"
        login = False
    
    
    # if username != "admin": # Wrong Username
    #     err_str = "Incorrect Username"
    #     login = False
    
    # if password != "password": # Wrong password
    #     err_str = "Incorrect Password"
    #     login = False
        
    if login: 
        friendlist = sql_db.get_user()
        print(friendlist)
        # a = ','.join(friendlist)
        # print(a)

        
        return page_view("login_valid", name=username, list=friendlist)
    else:
        return page_view("invalid", reason=err_str)

#-----------------------------------------------------------------------------
# Key formatting and handling
#-----------------------------------------------------------------------------
# Convert Public Key (PEM format) to string and vice versa
def convert_pub_key_to_str(public_key):
    pem_prefix = '-----BEGIN PUBLIC KEY-----\n'
    pem_suffix = '\n-----END PUBLIC KEY-----'

    # Export PEM format key to multi-line string format
    to_convert = public_key.exportKey('PEM').decode('ASCII')
    # Remove prefixes & suffixes
    to_convert = to_convert.removeprefix(pem_prefix).removesuffix(pem_suffix)
    # Remove newline characters
    converted_pub_key = to_convert.replace('\n','') 
    return converted_pub_key

def read_public_key_as_PEM(public_key_string):
    '''
        read_public_key
        Converts the public key string found in User to a PEM format and imports it

        :: public_key_string :: Public key in ASCII format after retrieval from database
        
        Returns the imported key
    '''
    # Attach prefixes and suffixes back into string
    to_import = '-----BEGIN PUBLIC KEY-----\n{}\n-----END PUBLIC KEY-----'.format(public_key_string)
    imported_key = RSA.import_key(to_import) # May/may not be needed
    return imported_key

    
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
# TODO: Escape character handling in SQL lines
#-----------------------------------------------------------------------------

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
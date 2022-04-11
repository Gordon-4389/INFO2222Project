'''
    This file will handle our typical Bottle requests and responses 
    You should not have anything beyond basic page loads, handling forms and 
    maybe some simple program logic
'''

from bottle import route, get, post, error, request, static_file

import model
import json
# import register
# import key_manage.js

#-----------------------------------------------------------------------------
# Static file paths
#-----------------------------------------------------------------------------

# Allow image loading
@route('/img/<picture:path>')
def serve_pictures(picture):
    '''
        serve_pictures

        Serves images from static/img/

        :: picture :: A path to the requested picture

        Returns a static file object containing the requested picture
    '''
    return static_file(picture, root='static/img/')

#-----------------------------------------------------------------------------

# Allow CSS
@route('/css/<css:path>')
def serve_css(css):
    '''
        serve_css

        Serves css from static/css/

        :: css :: A path to the requested css

        Returns a static file object containing the requested css
    '''
    return static_file(css, root='static/css/')

#-----------------------------------------------------------------------------

# Allow javascript
@route('/js/<js:path>')
def serve_js(js):
    '''
        serve_js

        Serves js from static/js/

        :: js :: A path to the requested javascript

        Returns a static file object containing the requested javascript
    '''
    return static_file(js, root='static/js/')

#-----------------------------------------------------------------------------
# Pages
#-----------------------------------------------------------------------------

# Redirect to login
@get('/')
@get('/home')
def get_index():
    '''
        get_index
        
        Serves the index page
    '''
    return model.index()

#-----------------------------------------------------------------------------

# Display the login page
@get('/login')
def get_login_controller():
    '''
        get_login
        
        Serves the login page
    '''
    return model.login_form()

#-----------------------------------------------------------------------------

# Attempt the login
@post('/login')
def post_login():
    '''
        post_login
        
        Handles login attempts
        Expects a form containing 'username' and 'password' fields
    '''

    # Handle the form processing
    username = request.forms.get('username')
    password = request.forms.get('password')
    
    # Call the appropriate method
    return model.login_check(username, password)



#-----------------------------------------------------------------------------
@get('/register')
def get_register_controller():
    return model.register_form()

# Attempt the register
@post('/register')
def post_register():
    username = request.forms.get('username')
    password = request.forms.get('password')
    email = request.forms.get('email')
    # output = request.get_json()
    # print(output)
    # result = json.loads(output) #this converts the json output to a python dictionary
    # print(result) # Printing the new dictionary
    # print(type(result))#this shows the json converted as a python dictionary
    with open('public.txt') as f:
        lines = f.readlines()
        public_key = lines[1]
    # print(lines)
    return model.register_check(username, password, public_key)
# ------------------------------------------------------------------------------
@get('/send')
def get_sendmess_page():
    return model.mess_form()

# send message
@post('/send')
def post_message():
    receiver = request.forms.get('receiver')
    message = request.forms.get('message')
    return model.send_mess(receiver, message)

# ------------------------------------------------------------------------------

@get('/incoming_mess')
def get_incoming_page():
    return model.incoming()

# ------------------------------------------------------------------------------
@get('/about')
def get_about():
    '''
        get_about
        
        Serves the about page
    '''
    return model.about()
#-----------------------------------------------------------------------------

# Help with debugging
@post('/debug/<cmd:path>')
def post_debug(cmd):
    return model.debug(cmd)

#-----------------------------------------------------------------------------

# 404 errors, use the same trick for other types of errors
@error(404)
def error(error): 
    return model.handle_errors(error)

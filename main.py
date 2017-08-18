from flask import Flask, request, redirect
import os
import jinja2
import string

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

app = Flask(__name__)
app.config['DEBUG'] = 'TRUE'

@app.route('/')
def index():
    """loads user-signup form"""
    template = jinja_env.get_template('index.html')
    return template.render()

def length(parameter):
    """checks the number of characters in the user input fields"""
    if len(parameter) >= 3 and len(parameter) <= 20:
        return True

def no_space(parameter):
    """checks if any spaces are in the user input fields"""
    if parameter.count(" ") == 0:
        return True

def confirmation(parameter, parameter2):
    """checks if the passwords match"""
    if parameter == parameter2:
        return True

def email_symbol(parameter):
    """checks if the email has the right symbols"""
    if parameter.count("@") == 1 and parameter.count(".") == 1:
        return True

@app.route('/valid', methods=['POST'])
def valid():
    """checks if the fields are valid"""
    username = request.form['username']
    password = request.form['password']
    pass_conf = request.form['pass_conf']
    email = request.form['email']

    if length(username) and no_space(username):
        username_error = ""
    else:
        username_error = "Not a valid username"

    if length(password) and no_space(password) and confirmation(password, pass_conf):
        password_error = ""
    elif not confirmation(password, pass_conf):
        password_error = "Passwords do not match"
    else:
        password_error = "Not a valid password" 
    if email == "" or length(email) and email_symbol(email):
        email_error = ""
    else:
        email_error = "Not a valid email"
    if username_error == "" and password_error == "" and email_error == "":
        return redirect('/welcome?username='+  username)
    else:
        template = jinja_env.get_template('index.html')
        return template.render(username_error=username_error, password_error=password_error,
                               email_error=email_error, username=username, email=email)


@app.route('/welcome')
def welcome():
    """loads welcome page with username"""
    username = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=username)

app.run()
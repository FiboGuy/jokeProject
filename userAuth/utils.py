import re

usernameReg=r'[A-Za-z0-9]{3,}'
passwordReg=r'[A-Za-z0-9]{4,}'
emailReg=r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'

def validUsername(username):
    return re.match(usernameReg,username)

def validPassword(password):
    return re.match(passwordReg,password)

def validEmail(email):
    return re.match(emailReg,email)
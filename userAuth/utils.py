import re

usernameReg=r'\w{3,}'
passwordReg=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{6,18}$'
emailReg=r'^([a-zA-Z0-9_.+-])+@([a-zA-Z0-9-]+)\.([a-z]+)$'

def validUsername(username):
    return re.match(usernameReg,username)

def validPassword(password):
    return re.match(passwordReg,password)

def validEmail(email):
    return re.match(emailReg,email)
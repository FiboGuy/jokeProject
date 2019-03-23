import re
import os
from PIL import Image

usernameReg=r'\w{3,}'
passwordReg=r'^(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z]).{6,18}$'
emailReg=r'^([a-zA-Z0-9_.+-])+@([a-zA-Z0-9-]+)\.([a-z]+)$'

def validUsername(username):
    return re.match(usernameReg,username)

def validPassword(password):
    return re.match(passwordReg,password)

def validEmail(email):
    return re.match(emailReg,email)

def deleteUserImages(user):
    user='user_'+user
    dir=os.path.join(os.path.dirname(os.path.abspath(__file__)),'../media')
    users=os.listdir(dir)
    if user not in users: return
    userdir = os.path.join(dir,users[users.index(user)])
    for i in os.listdir(userdir):
        os.remove(os.path.join(userdir,i))

    
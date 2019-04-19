from django.contrib.sessions.models import Session
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.auth.models import User
from datetime import datetime, timedelta
import time
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

def getUserFromSession(key, refresh=False):
    session = Session.objects.get(pk=key)
    if refresh:
        session.expire_date = datetime.now() + timedelta(days=1)
        session.save()
    data = session.get_decoded()
    user = User.objects.get(id = data['user_id'])
    return user

def login(user):
    try:
        session = Session.objects.get(pk=user.profile.session)
        session.expire_date = datetime.now() + timedelta(days=1)
        session.save()
    except:
        session = SessionStore()
        session['user_id'] = user.id
        session['created_at'] = time.time()
        session.set_expiry(86400)
        session.save()
        user.profile.session = session.session_key
        user.profile.save()
    return session

    
    # getUserAndRefreshSession
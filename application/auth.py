from .models import User
from sqlalchemy import exc
from .responses import ValidationError

def readcookie(cookie):
  try:
    cookieData = cookie.split(';')
  except:
    return '', ''
  else:
    token = ''
    user_id = ''
    for i in cookieData:
      if "Token" in i:
        token = i.split('=')[1]
      elif "User" in i:
        user_id = i.split('=')[1]
      if token != '' and user_id != '':
        break
  return token, user_id

def authenticate(cookie):
  token, user_id = readcookie(cookie)
  if token == '' or user_id == '':
    return False, 'UNAUTHORIZED! Please include valid credentials'
  try:
    user = User.query.filter_by(user_id = user_id).one()
  except exc.NoResultFound:
    return False, "No user found with the signed in User ID. Please login again."
  else:
    if user.fs_uniquifier == token:
      return True, user_id
    return False, 'Auth Token is invalid'
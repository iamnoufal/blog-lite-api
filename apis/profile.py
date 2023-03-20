from flask_restful import Resource
from flask import request, make_response

from application.models import *
from application.auth import authenticate

from .user import UserAPI

class ProfileAPI(Resource):
  def get(self):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      user = UserAPI()
      return user.get(user_id)
    else:
      resp = make_response()
      resp.status_code = 401
      resp.status = user_id
      return resp
    
  def post(self):
    return "Method not allowed"

  def put(self):
    return 'method not allowed'
  
  def delete(self):
    return "Method not allowed"
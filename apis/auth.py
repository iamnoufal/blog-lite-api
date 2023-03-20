from flask_restful import Resource, reqparse, fields
from flask import request

from sqlalchemy import exc

from application.models import User
from application.responses import *
from application.auth import authenticate

from .feed import FeedAPI

auth_input_fields = reqparse.RequestParser()
auth_input_fields.add_argument("user_id")
auth_input_fields.add_argument("email")
auth_input_fields.add_argument('password')

feed_output_fields = {
  "posts": fields.List(fields.Nested({
    "post_id": fields.String, 
    "title": fields.String, 
    "description": fields.String,
    "created": fields.String,
    "modified": fields.String,
    "user": fields.Nested({
      "user_id": fields.String,
      "name": fields.String,
      "email": fields.String,   
    })
  }))
}

class AuthAPI(Resource):
  
  def post(self):
    args = auth_input_fields.parse_args()
    user_id = args.get('user_id')
    email = args.get('email')
    password = args.get('password')
    try:
      if user_id == "":
        user = User.query.filter_by(email = email).one()
      else:
        user = User.query.filter_by(user_id = user_id).one()
    except exc.NoResultFound:
      raise NotFoundError(code=404, emsg="User with the entered User ID/Email doesn't exist")
    else:
      if user.password == password:
        return user.fs_uniquifier
      raise ValidationError(code=401, emsg="Incorrect password")

  def get(self):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      feed = FeedAPI()
      return feed.get(user_id)
    else:
      raise ValidationError(code=401, emsg=user_id)

  def put(self):
    return "Method not allowed"

  def delete(self):
    return "Method not allowed"

  
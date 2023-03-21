from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request, render_template
from flask_mail import Message

from application.db import db
from application.models import *
from application.responses import *
from application.auth import authenticate
from application.mail import mail

# from templates.mail import createAccount

from sqlalchemy import exc

import random
import string

from datetime import datetime

user_input_fields = reqparse.RequestParser()
user_input_fields.add_argument("user_id")
user_input_fields.add_argument("name")
user_input_fields.add_argument("email")
user_input_fields.add_argument("password")
user_input_fields.add_argument("image")
user_input_fields.add_argument("about")

update_user_input_fields = reqparse.RequestParser()
update_user_input_fields.add_argument("user_id")
update_user_input_fields.add_argument("name")
update_user_input_fields.add_argument("image")
update_user_input_fields.add_argument("about")

post_output_fields = {
  "post_id": fields.String, 
  "title": fields.String, 
  "description": fields.String,
  "image": fields.String, 
  "created": fields.String,
  "modified": fields.String
}

other_user_output_fields = {
  "user_id": fields.String,
  "name": fields.String,
  "email": fields.String,
}

user_output_fields = {
  "user_id": fields.String,
  "name": fields.String,
  "email": fields.String,
  "created_on": fields.String,
  "last_login": fields.String,
  "followers_list": fields.List(fields.Nested(other_user_output_fields)),
  "following_list": fields.List(fields.Nested(other_user_output_fields)),
  "posts": fields.List(fields.Nested(post_output_fields)),
  "image": fields.String,
  "about": fields.String
}

class UserAPI(Resource):

  @marshal_with(user_output_fields)
  def get(self, user_id):
    try: 
      user = User.query.filter_by(user_id = user_id).one()
      followers, following = [], []
      for i in user.followers:
        try:
          follower_user = User.query.filter_by(user_id = i.from_id).one()
        except exc.NoResultFound:
          followers.append({
            "user_id": user.i.from_id,
            "name": "Deleted user",
            "email": None,
            "posts": []
          })
        else:
          followers.append(follower_user)
      for i in user.following:
        try:
          following_user = User.query.filter_by(user_id = i.to_id).one()
        except exc.NoResultFound:
          following.append({
            "user_id": i.to_id,
            "name": "Deleted user",
            "email": None,
            "posts": []
          })
        else:
          following.append(following_user)
      user.followers_list = followers
      user.following_list = following
    except exc.NoResultFound:
      raise NotFoundError(code=404, emsg="User not found")
    else:
      return user
  
  def post(self):
    args = user_input_fields.parse_args()
    user = User()
    user.name = args.get("name")
    user.user_id = args.get("user_id")
    user.email = args.get("email")
    user.password = args.get('password')
    user.image = args.get("image")
    user.about = args.get('about')
    user.created_on = str(datetime.today())[:16]
    user.last_login = str(datetime.today())[:16]
    user.fs_uniquifier = ''.join(random.choices(string.digits, k=6))
    mail_template = render_template('verify-account.html', user = user)
    try:
      db.session.add(user)
      db.session.commit()
      msg = Message(sender=("Noufal Rahman", "noufal@gmail.com"), recipients=[user.email])
      msg.html = mail_template
      mail.send(msg)
    except exc.IntegrityError:
      db.session.rollback()
      error_msg = "User ID already exists. Please try a different User ID or login with this User ID"
      error_code = 400
      fake_user = User.query.filter_by(user_id = user.user_id).first()
      if fake_user is None:
        error_msg = "Email already exists. Please use a different Email ID or login with this Email ID"
      raise DuplicateError(code=error_code, emsg=error_msg)
    else:
      return 200
    
  def put(self):
    cookie = request.headers.get('Cookie')
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      args = update_user_input_fields.parse_args()
      user = User.query.filter_by(user_id = user_id).one()
      user.name = args.get("name")
      user.user_id = args.get('user_id')
      user.image = args.get('image')
      user.about = args.get('about')
      try:
        db.session.commit()
      except exc.IntegrityError:
        raise DuplicateError(emsg = "User ID exists. Please use a different User ID", code = 400)
      else:
        return 200

  def delete(self):
    pass
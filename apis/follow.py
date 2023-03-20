from flask_restful import Resource, reqparse
from flask import request 

from application.models import Followers
from application.auth import authenticate
from application.db import db
from application.responses import *

follow_input_fields = reqparse.RequestParser()
follow_input_fields.add_argument('follow')
follow_input_fields.add_argument('unfollow')

class FollowAPI(Resource):
  def post(self):
    cookie = request.headers.get('Cookie')
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      args = follow_input_fields.parse_args()
      follower = Followers()
      follower.from_id = user_id
      follower.to_id = args.get('follow')
      try:
        db.session.add(follower)
        db.session.commit()
      except:
        db.session.rollback()
        raise Error()
      else:
        return Success()
    else:
      raise ValidationError(code=400, emsg="UNAUTHORIZED! Please include valid credentials.")
    
  def put(self):
    cookie = request.headers.get('Cookie')
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      args = follow_input_fields.parse_args()
      follower = Followers.query.filter_by(from_id = user_id, to_id = args.get('unfollow')).delete()
      db.session.commit()
      return 200
    else:
      raise ValidationError(code=400, emsg="UNAUTHORIZED! Please include valid credentials.")
      
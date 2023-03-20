from flask_restful import Resource, reqparse
from flask import request 

from application.models import Followers
from application.auth import authenticate
from application.db import db
from application.responses import *

follow_input_fields = reqparse.RequestParser()
follow_input_fields.add_argument('follow')

class UnFollowAPI(Resource):
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
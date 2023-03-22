from flask_restful import Resource, reqparse
from flask import render_template
from flask_mail import Message
from sqlalchemy import exc

from application.models import User
from application.db import db
from application.responses import *
from application.mail import mail

import random
import string

user_verify_input_fields = reqparse.RequestParser()
user_verify_input_fields.add_argument('otp')

class VerifyAPI(Resource):
  def get(self, user_id):
    try: 
      user = User.query.filter_by(user_id = user_id).one()
      if len(user.fs_uniquifier) > 6:
        return 200, "User already verified"
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "User ID doesn't exist on our database.")
    else:
      mail_template = render_template('verify-account.html', user = user)
      msg = Message(subject="Verify your account | Blog Lite", recipients=[user.email], sender="noufal24rahman@gmail.com")
      msg.html = mail_template
      mail.send(msg)
      return 200, "Verification mail sent"

  def post(self, user_id):
    try: 
      user = User.query.filter_by(user_id = user_id).one()
      args = user_verify_input_fields.parse_args()
      if user.fs_uniquifier == args.get('otp'):
        user.fs_uniquifier = ''.join(random.choices(string.ascii_lowercase + string.digits, k=128))
        db.session.commit()
      else:
        user.fs_uniquifier = ''.join(random.choices(string.digits, k=6))
        db.session.commit()
        raise ValidationError(code = 400, emsg = "Incorrect OTP")
    except exc.NoResultFound:
      raise NotFoundError(code=404, emsg="Invalid User ID / Token. Please try again later")
    else:
      return user.fs_uniquifier
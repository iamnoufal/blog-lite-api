from flask import request
from flask_mail import Message
from flask_restful import Resource, reqparse

from application.auth import authenticate
from application.mail import mail

mail_input_fields = reqparse.RequestParser()
mail_input_fields.add_argument("body")
mail_input_fields.add_argument("recipients")
mail_input_fields.add_argument("")

class MailAPI(Resource):
  def post(self):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      msg = Message('TESTING', sender="noufal24rahman@gmail.com", recipients=['jnrahman12@gmail.com'])
      msg.body="I don't know what to send as an email :-)"
      mail.send(msg)
      print("sent")
      return 200
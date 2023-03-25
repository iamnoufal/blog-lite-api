from flask_restful import Resource
from flask import request

import json

from application.auth import authenticate
from application.tasks import *
from application.responses import *

class ImportContentAPI(Resource):
  def post(self):
    cookie = request.headers.get('Cookie')
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      file = request.files['file']
      data = json.load(file)
      if data['user_id'] == user_id:
        job = import_content.delay(data)
        return 200
      else:
        return ValidationError(code=401, emsg="The uploaded JSON file seems to be from a different user.")
    else:
      raise ValidationError(code=401, emsg=user_id)
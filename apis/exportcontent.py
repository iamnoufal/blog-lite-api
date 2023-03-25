from flask_restful import Resource
from flask import request

from application.auth import authenticate
from application.tasks import *
from application.responses import *

class ExportContentAPI(Resource):
  def get(self):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      job = export_content.delay(user_id)
      return str(job), 200
    else:
      raise ValidationError(code=401, emsg=user_id)
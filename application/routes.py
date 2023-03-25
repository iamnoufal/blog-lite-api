from flask import current_app as app
from .tasks import *
from apis.user import UserAPI

@app.route('/<user>')
def hello(user):
  job = export_content.delay(user)
  return str(job)
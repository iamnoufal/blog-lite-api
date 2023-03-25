import os
from flask import Flask
from flask_restful import Api
from application.db import db
from application.models import *
from application.config import LocalDevelopmentConfig
from application.workers import *
# from application.tasks import *
from flask_cors import CORS

current_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config.from_object(LocalDevelopmentConfig)
db.init_app(app)
api = Api(app)
CORS(app, resources={r"*": {"origins": "*"}}, supports_credentials=True)
celery.conf.update(
  broker_url = app.config['CELERY_BROKER_URL'],
  result_backend = app.config['CELERY_DATABASE_URL']
)
celery.Task = ContextTask
app.app_context().push()

from application.routes import *

from apis.user import UserAPI
from apis.auth import AuthAPI
from apis.post import PostAPI
from apis.profile import ProfileAPI
from apis.follow import FollowAPI
from apis.search import SearchAPI
from apis.verify import VerifyAPI
from apis.importcontent import ImportContentAPI
from apis.exportcontent import ExportContentAPI

api.add_resource(UserAPI, "/api/user", "/api/user/<user_id>")
api.add_resource(AuthAPI, '/api/auth')
api.add_resource(FollowAPI, "/api/user/follow")
api.add_resource(PostAPI, "/api/post", "/api/post/<post_id>")
api.add_resource(ProfileAPI, "/api/profile")
api.add_resource(SearchAPI, '/api/search/<pattern>', '/api/search/')
api.add_resource(VerifyAPI, '/api/<user_id>/verify')
api.add_resource(ExportContentAPI, '/api/export')
api.add_resource(ImportContentAPI, '/api/import')

if __name__ == "__main__":
  app.run(host="0.0.0.0", debug=True)
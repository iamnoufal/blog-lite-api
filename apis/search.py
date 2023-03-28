from flask_restful import Resource, fields

from application.models import User
from application.cache import cache

search_output_fields = {
  'users': fields.List(fields.Nested({'user_id': fields.String, 'name': fields.String}))
}

class SearchAPI(Resource):
  @cache.memoize(1000)
  def get(self, pattern=''):
    resp = []
    users = User.query.filter(User.name.like('%'+pattern+'%')).all()
    for i in users:
      resp.append({'user_id': i.user_id, 'name': i.name})
    return { 'users': resp }
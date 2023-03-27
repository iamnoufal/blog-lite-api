from flask_restful import Resource, fields

from application.models import User

search_output_fields = {
  'users': fields.List(fields.Nested({'user_id': fields.String, 'name': fields.String}))
}

class SearchAPI(Resource):
  def get(self, pattern=''):
    resp = []
    users = User.query.filter(User.name.like('%'+pattern+'%')).all()
    for i in users:
      resp.append({'user_id': i.user_id, 'name': i.name})
    return { 'users': resp }
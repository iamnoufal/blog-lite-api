from flask_restful import Resource, fields, marshal_with
from flask import request
from sqlalchemy import exc
from application.models import *
from application.responses import *
from application.cache import cache

user_output_fields = {
  "user_id": fields.String,
  "name": fields.String,
  "email": fields.String,
}

post_output_fields = {
  "post_id": fields.String, 
  "title": fields.String, 
  "description": fields.String,
  "image": fields.String, 
  "created": fields.String,
  "modified": fields.String,
  "user": fields.Nested(user_output_fields)
}

feed_output_fields = {
  "posts": fields.List(fields.Nested(post_output_fields))
}

class FeedAPI(Resource):
  @marshal_with(feed_output_fields)
  @cache.memoize(1000)
  def get(self, user_id):
    try:
      user = User.query.filter_by(user_id = user_id).first()
    except exc.NoResultFound:
      raise ValidationError(code=401, emg="Unauthorized request. Please include credentials")
    else:
      posts = []
      for i in user.following:
        try:
          following_user = User.query.filter_by(user_id = i.to_id).one()
        except exc.NoResultFound:
          pass
        else:
          for j in following_user.posts:
            post = Post.query.filter_by(post_id = j.post_id).one()
            posts.append(post)
      resp = {
        'posts': posts
      }
      return resp
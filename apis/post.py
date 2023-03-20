from flask_restful import Resource, fields, marshal_with, reqparse
from flask import request

import random
import string

from application.db import db
from application.models import *
from application.responses import *
from application.auth import authenticate

from sqlalchemy import exc

from datetime import datetime

from .user import other_user_output_fields

post_input_fields = reqparse.RequestParser()
post_input_fields.add_argument("title")
post_input_fields.add_argument("description")
post_input_fields.add_argument('image')

post_output_fields = {
  "post_id": fields.String, 
  "title": fields.String, 
  "description": fields.String,
  "author": fields.Nested(other_user_output_fields),
  "image": fields.String, 
  "created": fields.String,
  "modified": fields.String
}

class PostAPI(Resource):

  @marshal_with(post_output_fields)
  def get(self, post_id):
    try: 
      post = Post.query.filter_by(post_id = post_id).one()
      try:
        author = User.query.filter_by(user_id = post.user_id).one()
      except exc.NoResultFound:
        post.author = {
          "user_id": post.user_id,
          "name": "Deleted User",
          "email": None,
          "posts": []
        }
      else:
        post.author = author
    except exc.NoResultFound:
      raise NotFoundError(code = 404, emsg = "Post not found")
    else:
      return post
    
  def post(self):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      args = post_input_fields.parse_args()
      post = Post()
      post.title = args.get('title')
      post.description = args.get('description')
      post.image = args.get('image')
      post.user_id = user_id
      post.created = str(datetime.today())[:16]
      post.modified = str(datetime.today())[:16]
      post.post_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20)).lower()
      try:
        db.session.add(post)
        db.session.commit()
      except:
        db.session.rollback()
        resp = make_response()
        resp.status_code = 400
        resp.status = "Post upload failed. PLease try again"
        return resp
      else:
        resp = make_response()
        resp.status_code = 200
        return resp
    else:
      raise ValidationError(code=401, emsg=user_id)
    
  def delete(self, post_id):
    cookie = request.headers.get('Cookie')
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      try:
        post = Post.query.filter_by(post_id = post_id).one()
        if post.user_id == user_id:
          post = Post.query.filter_by(post_id = post_id).delete()
          db.session.commit()
        else:
          raise ValidationError(emsg = 'You are not allowed to delete this post', code = 401)
      except exc.NoResultFound:
        raise NotFoundError(code=404, emsg='Post not found')
      else:
        return 200
    else:
      return 400, json.dumps({'error': user_id})
    
  def put(self, post_id):
    cookie = request.headers.get("Cookie")
    is_authenticated, user_id = authenticate(cookie)
    if is_authenticated:
      args = post_input_fields.parse_args()
      try:
        post = Post.query.filter_by(post_id = post_id).one()
        post.title = args.get('title')
        post.description = args.get('description')
        post.image = args.get('image')
        post.modified = str(datetime.today())[:16]
        if post.user_id == user_id:
          db.session.commit()
      except exc.NoResultFound:
        raise NotFoundError(code=404, emsg="Post not found")
      except: 
        raise Error()
      else:
        return Success()
    else:
      raise ValidationError(code=401, emsg=user_id)
    
from flask import render_template
from flask_mail import Message

from sqlalchemy import exc
import json
from datetime import datetime

from .mail import mail
from .workers import celery
from .models import Post
from .db import db

from apis.user import UserAPI

@celery.task()
def verification_email(user_id, name, email, otp):
  mail_template = render_template('verify-account.html', user_id = user_id, name = name, otp = otp)
  msg = Message(sender="noufal24rahman@gmail.com", recipients=[email], subject="Verify your account | Blog Lite")
  msg.html = mail_template
  mail.send(msg)

@celery.task()
def export_content(user_id):
  user = UserAPI()
  data = user.get(user_id)
  user_data = dict(data)
  mail_template = render_template('export.html', user = user_data)
  msg = Message(sender="noufal24rahman@gmail.com", recipients=[user_data['email']], subject="Export content | Blog Lite")
  msg.html = mail_template
  msg.attach("blog_lite_export_{}.json".format(user_data), 'application/json', json.dumps(data, indent=2))
  # mail.send(msg)
  print("MAIL SENT TO", user_data['name'], user_data['email'])
  return {"name": user_data['name'], "email": user_data['email']}

@celery.task()
def import_content(data):
  for i in data['posts']:
    try:
      post = Post.query.filter_by(post_id = i['post_id']).one()
    except exc.NoResultFound:
      post = Post()
      post.post_id = i['post_id']
      post.title = i['title']
      post.description = i['description']
      post.image = i['image']
      post.user_id = data['user_id']
      post.created = data['created']
      post.modified = data['modified']
      try:
        db.session.add(post)
        db.session.commit()
      except:
        db.session.rollback()
    else:
      post.title = i['title']
      post.description = i['description']
      post.image = i['image']
      post.created = data['created']
      post.modified = datetime.now()[16:]
      db.session.commit()
  return "DONE IMPORT"
from flask import render_template
from flask_mail import Message

from sqlalchemy import exc
import json
from datetime import datetime, timedelta

from celery.schedules import crontab

from weasyprint import HTML

import requests

from .mail import mail
from .workers import celery
from .models import *
from .db import db

@celery.task()
def verification_email(user_id, name, email, otp):
  mail_template = render_template('verify-account.html', user_id = user_id, name = name, otp = otp)
  msg = Message(sender="noufal24rahman@gmail.com", recipients=[email], subject="Verify your account | Blog Lite")
  msg.html = mail_template
  mail.send(msg)

@celery.task()
def export_content(user_id):
  user = requests.get('http://127.0.0.1:5000/api/user/'+user_id)
  data = user.json()
  mail_template = render_template('export.html', user = data)
  msg = Message(sender="noufal24rahman@gmail.com", recipients=[data['email']], subject="Export content | Blog Lite")
  msg.html = mail_template
  msg.attach("blog_lite_export_{}.json".format(user_id), 'application/json', json.dumps(data, indent=2))
  mail.send(msg)
  return {"name": data['name'], "email": data['email'], "task": "export"}

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
      post.created = i['created']
      post.modified = i['modified']
      try:
        db.session.add(post)
        db.session.commit()
      except:
        db.session.rollback()
    else:
      post.title = i['title']
      post.description = i['description']
      post.image = i['image']
      post.created = i['created']
      post.modified = str(datetime.now())[:16]
      db.session.commit()
  mail_template = render_template('import.html', name = data['name'])
  msg = Message(sender="noufal24rahman@gmail.com", recipients=[data['email']], subject="Import content successful | Blog Lite")
  msg.html = mail_template
  mail.send(msg)
  return {"name": data['name'], "email": data['email'], "task": "import"}

@celery.task()
def create_report():
  users = User.query.all()
  for user in users:
    authors = {}
    posts = db.session.query(Post).filter(Post.created >= datetime.today().replace(day=1)).all()
    for post in posts:
      author = User.query.filter_by(user_id = post.user_id).one()
      authors[post.user_id] = author.name
    content = render_template("report.html", data = user, posts = posts, authors = authors)
    report = HTML(string=content)
    report_file = report.write_pdf()
    msg = Message(sender="noufal24rahman@gmail.com", recipients=[user.email], subject='Summary Snapshot | Blog Lite')
    mail_template = render_template('report-mail.html', name = user.name)
    msg.html = mail_template
    msg.attach("{}_blog_lite_monthly_report.pdf".format(user.user_id), 'application/pdf', report_file)
    mail.send(msg)
  return {"task": "create monthly report"}

@celery.task()
def send_remainders():
  users = User.query.all()
  for user in users:
    if datetime.strptime(user.last_login, '%Y-%m-%d %H:%M') < (datetime.today() - timedelta(days=1)):
      msg = Message(sender="noufal24rahman@gmail.com", recipients=[user.email], subject="We miss you! | Blog Lite")
      msg.html = render_template("remainder.html", name = user.name)
      mail.send(msg)
  return {'task': 'remainders'}

@celery.on_after_finalize.connect
def schedule_tasks(sender, **kwargs):
  sender.add_periodic_task(crontab(hour=1, day_of_month=1), create_report.s(), name="Send monthly report")
  sender.add_periodic_task(crontab(hour=15, minute=5), send_remainders(), name="Send Remainder everyday")

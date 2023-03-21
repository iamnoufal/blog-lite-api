from .db import db

model = db.Model
col = db.Column

class User(model):
  __tablename__ = "user"
  user_id = col(db.String, primary_key=True)
  name = col(db.String, nullable=False)
  email = col(db.String, unique=True, nullable=False)
  password = col(db.String, nullable=False)
  created_on = col(db.String)
  last_login = col(db.String)
  image = col(db.String)
  fs_uniquifier = col(db.String(128), unique=True, nullable=False) 
  verified = col(db.Integer)
  about = col(db.String)
  posts = db.relationship("Post")
  followers = db.relationship("Followers", foreign_keys="Followers.to_id")
  following = db.relationship("Followers", foreign_keys="Followers.from_id")

class Post(model):
  __tablename__ = "post"
  post_id = col(db.String, primary_key=True)
  title = col(db.String, nullable=False)
  description = col(db.String)
  user_id = col(db.String, db.ForeignKey("user.user_id"), nullable=False)
  image = col(db.String)
  created = col(db.String)
  modified = col(db.String, nullable=True)

class Followers(model):
  __tablename__ = "followers"
  id = col(db.Integer, primary_key=True, autoincrement=True)
  from_id = col(db.String, db.ForeignKey("user.user_id"), nullable=False)
  to_id = col(db.String, db.ForeignKey("user.user_id"), nullable=False)
  
import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    email = db.Column(db.String, unique=True, nullable = False)
    password = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<email_id = {self.id}> email={self.email}>'


class Image(db.Model):
    __tablename__= "images"
    
    image_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    location = db.Column(db.String)
    time = db.Column(db.DateTime)
    weather = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Activity(db.Model):
    __tablename__ = "activity"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    kind = db.Column(db.String)
    tools = db.Column(db.String)
    cost = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("image.image_id"))

def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"], echo=False):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)









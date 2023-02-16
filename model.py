import os
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model, UserMixin):
    
    __tablename__ = "users"

    id = db.Column(db.Integer,autoincrement=True,primary_key=True)
    email = db.Column(db.String(30), unique=True, nullable = False)
    username = db.Column(db.String(20), unique=True, nullable= False )
    password = db.Column(db.String, nullable = False)

    def __repr__(self):
        return f'<email_id = {self.id} email={self.email}>'

    def __init__(self, email, username,password):
        self.email = email
        self.username = username
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


    @classmethod
    def create_user(cls, email, username, password):
        return cls(email = email, username = username, password= password)
    
    @classmethod
    def check_users(cls, em, username):
        return cls.query.filter_by(email=em).first() and cls.query.filter_by(username=username).first()

    @classmethod
    def get_user_id(cls, user_id):
        return cls.query.filter_by(id = user_id).first()

    @classmethod
    def get_all_users(cls):
        return cls.query.all()


# cvs cloud inary 
class Activity(db.Model):
    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    kind = db.Column(db.String)
    tools = db.Column(db.String)
    cost = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="activities")

    def __repr__(self):
        return f'<activity_id={self.activity_id} kind={self.kind}>'

    @classmethod
    def split_tools(cls, tools):
        return tools.split(',')
            # create method for tools so they already come out as "commas"
    @classmethod
    def create_activity(cls, kind, tools, cost, user):
        return cls(kind=kind, tools=tools, cost=cost, user_id = user)
    
    @classmethod
    def get_all_activities(cls):
        return cls.query.all()


class Image(db.Model):
    __tablename__= "images"
    
    image_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    image_path = db.Column(db.String)
    location = db.Column(db.String)
    weather = db.Column(db.String)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))

    activity = db.relationship("Activity", backref="images")
    user = db.relationship("User", backref="images")

    def __repr__(self):
        return f'<image_id={self.image_id} name={self.image_path}>'
    
    @classmethod
    def create_image(cls, image_path, location, weather, user_id, activity_id):
        return cls(image_path=image_path, location= location, weather=weather, user_id=user_id, activity_id=activity_id)

    @classmethod
    def get_all_images(cls):
        return cls.query.all()


def connect_to_db(flask_app, db_uri=os.environ["POSTGRES_URI"]):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app
    connect_to_db(app)









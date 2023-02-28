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
    cost = db.Column(db.Integer)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

    user = db.relationship("User", backref="activities")
    tool = db.relationship("Tool", backref="activities", uselist=False)

    def __repr__(self):
        return f'<activity_id={self.activity_id} kind={self.kind}>'

    @classmethod
    def create_activity(cls, kind, cost, user_id):
        return cls(kind=kind, cost=cost, user_id = user_id)
    
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
    comment = db.relationship("Comment", backref="images", uselist=False)

    def __repr__(self):
        return f'<image_id={self.image_id} name={self.image_path}>'
    
    @classmethod
    def create_image(cls, image_path, location, weather, user_id, activity_id):
        return cls(image_path=image_path, location= location, weather=weather, user_id=user_id, activity_id=activity_id)

    @classmethod
    def get_all_images(cls):
        return cls.query.all()


class Tool(db.Model):
    __tablename__ = "tools"

    tool_id = db.Column(db.Integer, autoincrement=True, primary_key = True)
    name = db.Column(db.Text)

    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))

    def __repr__(self):
        return f'<tool_id={self.tool_id} name={self.name}>'

    @classmethod
    def create_tool(cls, name, activity_id):
        return cls(name = name, activity_id = activity_id)
        
    @classmethod
    def get_all_tools(cls):
        return cls.query.all()

class Comment(db.Model):
    __tablename__ = 'comments'

    comment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    comment = db.Column(db.Text)

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    image_id = db.Column(db.Integer, db.ForeignKey("images.image_id"))

    def __repr__(self):
        return f'<comment_id ={self.comment_id} name={self.comment}>'
    
    @classmethod
    def create_comment(cls, comment, user_id, image_id):
        return cls(comment = comment, user_id= user_id, image_id = image_id)


def connect_to_db(flask_app, uri=os.environ["DATABASE_URL"]):
    
    if uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = uri
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from app import app
    connect_to_db(app)









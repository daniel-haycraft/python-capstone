from flask import Flask, render_template, session, url_for, redirect, flash, session, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import timedelta
import json

from model import connect_to_db, User, UserMixin, Image, Activity, db, Tool
from forms import RegisterForm, UserForm, CreatePost
from jinja2 import StrictUndefined

app = Flask(__name__)

app.secret_key = 'dev'

import cloudinary

cloudinary.config(
  cloud_name = "dnmkry9p0",
  api_key = "312126661549849",
  api_secret = "epqOkNeGIfv4M4j5pQ_rpKAnxf4",
  secure = True
)

from cloudinary.uploader import upload
from cloudinary.utils import cloudinary_url

login_manager = LoginManager()
login_manager.init_app(app)
app.jinja_env.undefined = StrictUndefined

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    register = RegisterForm()
    email=register.email.data
    username = register.username.data
    password = register.password.data
    double_password = register.double_password.data
    if register.validate_on_submit():
        if User.check_users(email, username):
            return redirect('/register'), flash('email or username already exists')
        if password != double_password:
            return flash('passwords do not match')
        else:
            new_user = User.create_user(email, username,password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'registered! {register.email.data} successfully')
            return redirect(url_for('login'))
    return render_template('register.html',register=register)

@login_manager.user_loader
def load_user(user_id):
    """a call back function that takes in a user id and logs them in"""
    return User.get_user_id(user_id)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """log in function/ the form from forms.py takes in email: str, generate_hash(password):str, user: str"""
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email = email).first()
        if user:
            """check_password(password) takes in a hashed(password) and checks the original password """
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('home'))
        return 'wrong password or email'
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    """loging out a current user"""
    logout_user()
    return redirect(url_for("home"))

@app.route('/posts', methods = ['GET', 'POST'])
def posts():
    """using get_all_images from my class method aka(cls) in my db.Image model"""
    images = Image.get_all_images()
    return render_template('posts.html', images = images)

@app.route('/posts/<user_id>', methods=['GET','POST'])
def post_details(user_id):
    user = User.get_user_id(user_id)
    images = Image.query.filter_by(user_id = user.id).all()
    return render_template('post_details.html', imagess= images)

@app.route('/delete/<image_id>', methods=['GET','POST', ])   
def delete_post(image_id):
    img_id = Image.query.filter_by(image_id = image_id).first()
    activity_id = img_id.activity.activity_id
    tool = Tool.query.filter_by(activity_id= img_id.activity.tool.tool_id).first()
    db.session.delete(img_id.activity)
    db.session.delete(img_id)
    db.session.delete(tool)
    db.session.commit()
    return redirect(url_for('home'))

@app.route('/update/<image_id>', methods=['GET', 'POST'])
def update(image_id):
    image = Image.query.filter_by(image_id = image_id).first()
    if not image:
        return 'image not found'
    post = CreatePost()
    kind = post.activity.data
    location = post.location.data
    weather = post.weather.data
    equipment = post.equipment.data
    cost = post.cost.data
    image_file = request.files.get('image')
    if request.method == 'POST':
        if image_file is not None:
            upload_result = cloudinary.uploader.upload(image_file, folder='capstone', format='png')
            image_url = upload_result['secure_url']
            image.image_path= image_url
        image.activity.kind = kind
        image.location = location
        image.weather = weather
        image.activity.cost = cost
        image.activity.tool.name = equipment
        db.session.commit()
        return redirect(url_for('home'))
    else:
        return render_template('update.html', post=post, image = image)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    post = CreatePost()
    activity = post.activity.data
    location = post.location.data
    weather = post.weather.data
    equipment = post.equipment.data
    cost = post.cost.data
    if request.method == 'POST':
        image_file = request.files.get('image')
        if image_file is not None:
            upload_result = cloudinary.uploader.upload(image_file, folder='capstone', format='png')
            image_url = upload_result['secure_url']
            new_activity = Activity.create_activity(activity, cost, current_user.id)
            db.session.add(new_activity)
            db.session.commit()
            db.session.refresh(new_activity)
            new_tool = Tool.create_tool(equipment, new_activity.activity_id)
            new_image = Image.create_image(image_url, location, weather, current_user.id, new_activity.activity_id)
            db.session.add(new_tool)
            db.session.add(new_image)
            db.session.commit()
            return redirect(url_for("posts")), flash('uploaded!')
        else:
            flash('something went wrong')
    return render_template('upload.html', post=post)

if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port =3001, debug=True)
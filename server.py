from flask import Flask, render_template, session, url_for, redirect, flash, session, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import timedelta

from model import connect_to_db, User, UserMixin, Image, Activity, db
from forms import RegisterForm, UserForm
from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'

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
    password = register.password.data
    double_password = register.double_password.data

    ## check users check db if email exists
    if register.validate_on_submit():
        if User.check_users(email):
            return redirect('/register'), flash('email already exists')
        if password != double_password:
            return flash('passwords do not match')
        else:
            nu = User.create_user(email, password)
            db.session.add(nu)
            db.session.commit()
            flash(f'registered! {register.email.data} successfully')
            return redirect(url_for('login'))
    return render_template('register.html',register=register)

@login_manager.user_loader
def load_user(user_id):
    return User.get_user_id(user_id)
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        user = User.check_users(email)
        if user:
            if user.password == password:
                login_user(user)
                return redirect(url_for('home'))
        return 'wrong password or email'
    else:
        return render_template('login.html', form=form)



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port =3001, debug=True)
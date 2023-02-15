from flask import Flask, render_template, session, url_for, redirect, flash, session, request
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from datetime import timedelta

from model import connect_to_db

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = 'dev'

login_manager = LoginManager()
login_manager.init_app(app)

app.jinja_env.undefined = StrictUndefined




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="localhost", port = 3001, debug=True)
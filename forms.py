from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, validators, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length

class UserForm(FlaskForm):
    email = StringField("Email Here", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email Here", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    double_password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")
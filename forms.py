from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SelectField, SubmitField, validators, BooleanField, TextAreaField, RadioField
from wtforms.validators import DataRequired, InputRequired, Length
#put in forms later
# location = StringField("Location")
#     weather = StringField("Weather/Degrees")
class UserForm(FlaskForm):
    email = StringField("Email Here", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    email = StringField("Email Here", validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    double_password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

class CreatePost(FlaskForm):
    activity = StringField("What did you do?", validators=[DataRequired()])
    location = StringField("Location?", validators=[DataRequired()])
    weather = StringField("What was the weather like?", validators=[DataRequired()])
    equipment = StringField("equipment used?", validators=[DataRequired()])
    cost = StringField("how much did it cost", validators=[DataRequired()])
    comment = TextAreaField("Comment what you did!", validators=[DataRequired()])
    submit = SubmitField("Submit")

class Comments(FlaskForm):
    comment = StringField('Text')
    submit = SubmitField('submit')
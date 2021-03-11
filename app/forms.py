from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, TextField, SubmitField, DateField, PasswordField
from wtforms.validators import DataRequired, Length
from wtforms.validators import DataRequired, Length, EqualTo, Email
from wtforms_components import TimeField
import email_validator

class LoginForm(FlaskForm):
    username = StringField('Username', validators= [DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

    submit = SubmitField('Login')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Length(min=6), Email(message='Invalid email.'), DataRequired()])
    password = PasswordField('Password', validators = [DataRequired(), EqualTo('repeatpassword', message='Passwords must match')])
    repeatpassword = PasswordField('Repeat Password')

    # recaptcha = RecaptchaField()
    submit = SubmitField('Register')

class AddForm(FlaskForm):
    appointment = StringField('Appointment', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    date = DateField('Date', validators=[DataRequired()])
    time = TimeField('Time', validators=[DataRequired()])

    submit = SubmitField('Create Appointment')

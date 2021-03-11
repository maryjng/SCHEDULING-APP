from . import db
from datetime import datetime, time, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class Appointments(db.Model):
    __tablename__='Appointments'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    appt = db.Column(db.String(100))
    date = db.Column(db.Date())
    time = db.Column(db.Time())
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

    # def __init__(self, appt, date, time):
    #     self.username = username
    #     self.appt = appt
    #     self.date = date
    #     self.time = time

    def __repr__(self):
        return f"APPT({self.appt}, {self.date}, {self.time})"

class Users(UserMixin, db.Model):
    __tablename__='Users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    password = db.Column(db.String(200))
    email = db.Column(db.String(1000), unique=True, nullable=False)
    appts = db.relationship('Appointments', backref='author', lazy=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"User {self.username}"

    # def __init__(self, username, password, email):
    #     self.username = username
    #     self.password = password
    #     self.email = email

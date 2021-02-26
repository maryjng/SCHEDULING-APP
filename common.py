#test create db and add Users instance
from app import create_app
from app.extensions import db
db.create_all(app=create_app())

from app.models import Users, Appointments

user = Users(username="User1", password="kitty", email="hi@gmail.com")
db.session.add(user)
db.session.commit

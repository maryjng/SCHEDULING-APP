from flask import Blueprint, render_template, url_for, redirect, session
# from ..forms import LoginForm, RegisterForm, AddForm
from flask_login import login_required, logout_user, current_user, login_user
from ..extensions import login
import calendar
from datetime import datetime

home = Blueprint('home', __name__, url_prefix='/home')

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/login', methods=['GET', 'POST'])
def login():
#     form = LoginForm()
#     if form.validate_on_submit():
    username = request.form['username']
    password = request.form['password']
    email = request.form['email']
    user = Users.query.filter_by(email = email).first()
    if user is not None and user.check_password(password):
        login_user(user)
        return redirect(url_for('home/agenda'))

    return render_template('login.html')

@home.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home/login'))

@home.route('/register', methods=['GET', 'POST'])
def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
    user = Users.query.filter_by(email=email).first()
    if user:
        flash("Username is already registered.")
        return redirect(url_for('home/register'))

    new_user = Users(username=username, password=generate_password_hash(password), email=email)
    db.session.add(new_user)
    db.session.commit()
    flash("Account registered.")
    return redirect(url_for('home/login'))

    return render_template('register.html')

@home.route('/agenda', methods=['GET'])
# @login_required
def agenda():
    x = datetime.today()
    m = x.month
    y = x.year

    c = calendar.TextCalendar(calendar.MONDAY)
    days = c.itermonthdays(y,m)
    monthappts = Appointments.query.filter_by(date=m)

    return render_template('agenda.html', monthappts=monthappts, days=days)

@home.route('/add', methods=['GET', 'POST'])
@login_required
def add():
#     form = AddForm()
#     if form.validate_on_submit():
    appointment = request.form['appointment']
    location = request.form['location']
    date = request.form['date']
    time = request.form['time']
        new_appt = Appointments(appointment=appt, location=location, date=date, time=time)
        db.session.add(new_appt)
        db.session.commit()
        flash("Appointment added.")
        return redirect(url_for('home/agenda'))

    return render_template('add.html')

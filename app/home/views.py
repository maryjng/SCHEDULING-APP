from .. import db
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..forms import LoginForm, RegisterForm, AddForm
from ..models import Users, Appointments
from flask_login import login_required, logout_user, current_user, login_user
from datetime import datetime, date, timedelta
from sqlalchemy import extract
import calendar

home = Blueprint('home', __name__, url_prefix='/home', template_folder='templates/home')

@home.route('/')
def index():
    return render_template('index.html')

@home.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = request.form.get('username')
        user = Users.query.filter_by(username=username).first()
        if user is not None and user.check_password(request.form['password']):
            login_user(user)
            today = datetime.today()
            year, month = today.year, today.month
            return redirect(url_for('home.agenda', year=year, month=month))

    return render_template('login.html', form=form)

@home.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home.login'))

@home.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash("Username is already registered.")
            return redirect(url_for('home.register'))

        new_user = Users(username=username, password=generate_password_hash(password), email=email)
        db.session.add(new_user)
        db.session.commit()
        flash("Account registered.")
        return redirect(url_for('home.login'))

    return render_template('register.html', form=form)

def prev_month_year(year: int, month: int):
    prev_month_date = date(year, month, 1) - timedelta(days=2)
    return prev_month_date.month, prev_month_date.year

def next_month_year(year: int, month: int):
    last_day_of_month = calendar.monthrange(year, month)[1]
    next_month_date = date(year, month, last_day_of_month) + timedelta(days=2)
    return next_month_date.month, next_month_date.year

today = datetime.today()
year, month = today.year, today.month

@home.route('/agenda')
@home.route('/agenda/<year>/<month>')
@login_required
def agenda(year=year, month=month):

    y, m = int(year), int(month)

    prev_month, prev_year = prev_month_year(y, m)
    next_month, next_year = next_month_year(y, m)

    c = calendar.TextCalendar(calendar.MONDAY)
    days = c.itermonthdays(y,m)

#     monthappts = Appointments.query.filter_by(user_id == current_user).all()
    # monthappts = Appointments.query.filter_by(user_id == current_user), (extract('year', Appointments.date) == y), (extract('month', Appointments.date) == m)).all()

    return render_template('agenda.html', days=days, prev_year=prev_year, prev_month=prev_month, next_month=next_month, next_year=next_year, today=today, year=y, month=m, monthappts=monthapps)

@home.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        appt = request.form.get('appointment')
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')
        username = current_user

        new_appt = Appointments(username=username, appt=appt, location=location, date=date, time=time)
        db.session.add(new_appt)
        db.session.commit()
        flash("Appointment added.")

        return redirect(url_for('home.agenda'))

    return render_template('add.html', form=form)

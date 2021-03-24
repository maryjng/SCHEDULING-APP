from .. import db
from flask import Blueprint, render_template, url_for, redirect, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..forms import LoginForm, RegisterForm, AddForm
from ..models import Users, Appointments
from flask_login import login_required, logout_user, current_user, login_user
import calendar
from datetime import datetime, date, timedelta
from sqlalchemy import extract

home = Blueprint('home', __name__, url_prefix='/home')

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
            return redirect(url_for('home.agenda'))

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

@home.route('/agenda', methods=['GET'])
@login_required
def agenda():



    # monthappts = Appointments.query.filter(Appointments.username == current_user.username, (extract('year', Appointments.date) == y), (extract('month', Appointments.date) == m))
    # # user = Users.query.filter_by(email=current_user.email).first_or_404()
    #
    # return render_template('agenda.html', today=today, days=days, monthappts=monthappts)

def prev_month_year(year: int, month: int):
    prev_month_date = date(year, month, 1) - timedelta(days=2)
    return prev_month_date.month, prev_month_date.year

def next_month_year(year: int, month: int):
    last_day_of_month = calendar.monthrange(year, month)[1]
    next_month_date = date(year, month, last_day_of_month) + timedelta(days=2)
    return next_month_date.month, next_month_date.year

@home.route('/agenda/<year>/<month>', methods=['GET', 'POST'])
@login_required
def agenda(year: int = None, month: int = None):
    y, m = year, month
    today = datetime.today()
    year, month = today.year, today.month

    if y == None or x == None:
        return redirect(url_for('home.agenda/<year>/<month>'))

    prev_month, prev_year = prev_month_year(y, m)
    next_month, next_year = next_month_year(y, m)

    c = calendar.TextCalendar(calendar.MONDAY)
    days = c.itermonthdays(y,m)

#     monthappts = Appointments.query.filter(Appointments.username == current_user.username, (extract('year', Appointments.date) == y), (extract('month', Appointments.date) == m))
#     # user = Users.query.filter_by(email=current_user.email).first_or_404()

    return render_template('agenda.html', days=days, prev_year=prev_year, prev_month=prev_month, next_month=next_month, next_year=next_year)

@home.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = AddForm(request.form)
    if form.validate_on_submit():
        appt = request.form.get('appointment')
        location = request.form.get('location')
        date = request.form.get('date')
        time = request.form.get('time')

        conv_date = datetime.strptime(date, "%Y-%m-%d").date()

        new_appt = Appointments(author=current_user, appt=appt, location=location, date=conv_date, time=time)
        db.session.add(new_appt)
        db.session.commit()
        flash("Appointment added.")

        return redirect(url_for('home.agenda'))

    return render_template('add.html', form=form)

import secrets
from flask import render_template, url_for, flash, redirect, request
from GClass.forms import RegistrationForm, LoginForm
from GClass import app, bcrypt, login_manager
from flask_login import login_user, current_user, logout_user, login_required
from GClass.models import User
from pymongo.errors import DuplicateKeyError
from GClass.mongodbOperations import *

########################################################################################################################

@app.route('/')
@app.route('/home')
def home():
    return render_template('homepage.html')

#######################################################################################################################

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = RegistrationForm()
    
    if form.validate_on_submit():

        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')       
        user = get_user(form.username.data) 
        if user is None:
            save_user(form.username.data, form.email.data, hashed_password)
            user = get_user(form.username.data)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Account Already Exists', 'danger')

    return render_template('register.html', form = form)

########################################################################################################################

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()

    if form.validate_on_submit():
        user = get_user(form.username.data)
        if user and bcrypt.check_password_hash(user['password'], form.password.data):
            login_user(User(user['username'],user['email'],user['password']))
            return redirect(url_for('home'))
        else:
            flash('Please check your credentials!', 'danger')
    return render_template('login.html', form = form)

########################################################################################################################

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

########################################################################################################################

@login_manager.user_loader
def load_user(username):
    return get_User(username)

#########################################################################################################################

@login_required
@app.route('/dashboard')
def dashboard():
    user_rooms = get_room_for_user(current_user.username)
    if user_rooms is not None:
        has_group = True
    else:
        has_group = False
    return render_template('dashboard.html', user_rooms = user_rooms, has_group = has_group)

#########################################################################################################################

@app.route('/join')
def join():
    pass
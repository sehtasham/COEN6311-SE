from ast import Return
from crypt import methods
from ctypes import addressof

from urllib3 import Retry
from .validations import *
from unicodedata import category
from xmlrpc.client import boolean
from flask import Blueprint, render_template,request, flash, redirect, url_for,Response
from flask import json
from . import db
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again', category='error') 
        else: 
            flash('Email does not exist!', category='error')
    return render_template("login2.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    flash('logged out successfully', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmedPassword')
        gender = request.form.get('confirmedPassword')
        
        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        adress = request.form.get('adress')
        city = request.form.get('city')
        country = request.form.get('country')
        postal = request.form.get('postal')
        #userType = request.form.get('admin')
        
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Username or Email is already  exist', category='error')
        elif not email_validation(email):
            flash('Your email address is not valid!', category='error') 
        elif not name_validation(first_name):
            flash('Your name is incorrect', category='error')
        elif password != confirmed_password:
            flash('Your passwords do not match!', category='error')
        elif not password_validation(password)[0]:
            flash(password_validation(password)[1], category='error' )
        else:
            new_user = User(email = email,
                            first_name=first_name,
                            password=generate_password_hash(password, method='sha256'),
                            #gender=gender,
                            #phonenumber=phone,
                            #birthday=birthday,
                            #address= adress,
                            #city=city,
                            #country=country,
                            #postalcode=postal 
                            )
            db.session.add(new_user)
            db.session.commit()
            flash('You successfully signed up and also logged in!', category='success')
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign_up2.html", user = current_user)

@auth.route('/', methods=['GET','POST'])
def home():
     return render_template("home.html")
 
     
@auth.route('/contacts', methods=['GET','POST'])
def contacts():
     return render_template("contacts.html")
     
@auth.route('/aboutus', methods=['GET','POST'])
def aboutus():
     return render_template("about-us.html")  
     

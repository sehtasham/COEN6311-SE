from ast import Return
from crypt import methods
from ctypes import addressof
from distutils.log import error
from signal import raise_signal
from traceback import print_tb

from urllib3 import Retry
from .validations import *
from unicodedata import category
from xmlrpc.client import boolean
from flask import Blueprint, render_template,request, flash, redirect, url_for,Response
from flask import json
from . import db
from .models import User
from .models import Tickett
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
     
@auth.route('/user-account', methods=['GET','POST'])
@login_required 
def user_account():
    return render_template("user_account.html",user = current_user)

@auth.route('/search', methods=['GET'])
def dropdown():
    seat_type = ['Business', 'Economy', 'Permium']
    source = ['Montreal', 'Vancouver', 'Toronto']
    destination = ['Newyork', 'Seattle', 'Vancouver']
    return render_template('search.html', seat_type=seat_type,source=source, destination=destination, user = current_user)

@auth.route('/search', methods=['POST'])
def search_post():
    if request.method == 'POST':
        heading = ("source_name","destination_name","departure_date","return_date", "price", "airline")
        source = request.form.get('sourceid')
        destination = request.form.get('destinationid')
        source = str(source) 
        data = Tickett.query.filter_by(source_name= source,destination_name= destination).all()

        if not data:          
            flash('There is no flight available based on your filter', category='error')
            return redirect(url_for('auth.dropdown'))
        #raise ValueError(data)

    return render_template("search_result.html", heading=heading, data=data)

@auth.route('/update', methods=['GET','POST'])
def update():
    return render_template("user_account.html",user = current_user)

@auth.route('/edit', methods=['GET','POST'])
def edit():
    return render_template("user_update.html", user = current_user)  



@auth.route('/edit-user', methods=['GET','POST'])
def edit_user():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        user = User.query.filter_by(email=current_user.email).first()
        if user is None:
            raise ValueError("error the user is empty!!")
        user.first_name= first_name
        user.email = email
        db.session.commit()
        user = User.query.filter_by(email=email).first()
        return render_template("user_account.html", user=user)
    else:
        return render_template("user_account.html", user=current_user)

@auth.route('/admin', methods=['GET', 'POST'])
def edit_ticket():
    heading = ("source_name","destination_name","departure_date","return_date", "price", "airline")
    data = Tickett.query.all()
    data2 = (("Montreal","Ottawa","03/26/2022","04/01/2022","200 CAD", "Air Canada"),
            ("Montreal","Toronto","12/26/2022","23/01/2022","150 CAD", "Air Canada"),
            ("Montreal","Vancouver","05/26/2022","07/01/2022","300 CAD", "Air Canada"))

    return render_template("admin.html", heading=heading, data=data)

@auth.route('/add-ticket', methods=['GET','POST'])
def add_ticket():
    return render_template("add_ticket.html", user = current_user)  

@auth.route('/add-ticket-admin', methods=['GET', 'POST'])
def add_ticket_admin():
    if request.method == 'POST':
        source_name = request.form.get('source_name')
        destination_name = request.form.get('destination_name')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        price = request.form.get('price')
        airline = request.form.get('airline')

        if not name_validation(source_name):
            flash('Source name is incorrect', category='error')
        elif not name_validation(destination_name):
            flash('Destination name is incorrect', category='error')
        elif not name_validation(airline):
            flash('Airline name is incorrect', category='error')
        elif (price is None):
            flash('Price field is empty', category='error')
        elif (departure_date is None):
            flash('Departure date field is empty', category='error')
        elif (return_date is None):
            flash('Return date date field is empty', category='error')
        else:
            new_ticket = Tickett(source_name = source_name, 
            destination_name = destination_name, 
            departure_date = departure_date, 
            return_date = return_date,
            price = price,
            airline = airline)

            db.session.add(new_ticket)
            db.session.commit()

            flash('You successfully add new ticket', category='success')
            return redirect(url_for('auth.add_ticket'))

        return render_template("add_ticket.html", user = current_user)
 
        
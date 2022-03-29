from ast import Return
from crypt import methods
from ctypes import addressof
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
        
        is_alertifly = request.form.get('is_alertifly')

        if email == '' : return "", "500 Email is empty"
        if password == '' : return "", "500 Password is empty"
        if user:
            if check_password_hash(user.password, password):
                if is_alertifly == '1' : 
                    return render_template("login.html", user=user) 
                flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                return "", "500 Incorrect password"
        else:
            return "", "500 Email not found"
    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    flash('logged out successfully', category='success')
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET','POST'])
def sign_up():
    if request.method == 'POST':
        print ("check point 1")
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmedPassword')
        gender = request.form.get('gender')

        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        adress = request.form.get('adress')
        city = request.form.get('city')
        country = request.form.get('country')
        postal = request.form.get('postal')
        #userType = request.form.get('admin')
        
        is_alertifly = request.form.get('is_alertifly')

        user = User.query.filter_by(email=email).first()
        print ("check point 11")
        if user:
            #flash('Username or Email is already  exist', category='error')
            return "", "500 Username or Email is already  exist"
        elif not email_validation(email):
            #flash('Your email address is not valid!', category='error')
            return "", "500 Your email address is not valid!"
        elif not name_validation(first_name):
            #flash('Your name is incorrect', category='error')
            return "", "500 Your name is incorrect"
        elif password != confirmed_password:
            #flash('Your passwords do not match!', category='error')
            return "", "500 Your passwords do not match!"
        elif not password_validation(password)[0]:
            #flash(password_validation(password)[1], category='error' )
            return "", "500 " + str(password_validation(password)[1])
        elif is_alertifly == '1' : 
           return render_template("sign_up.html", user=current_user) 
        else:
            print ("check point 13") 
            new_user = User(email = email,
                            first_name=first_name,
                            password=generate_password_hash(password, method='sha256')
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
            print ("check point 15")
            flash('You successfully signed up and also logged in!', category='success')
            login_user(new_user, remember=True)
            print ("check point 2")

            return redirect(url_for('views.home'))
        #return render_template("home.html", user=user)
    else:
        print ("check point 3")
        return render_template("sign_up.html", user = current_user)


# Reza
@auth.route('/', methods=['GET','POST'])
def home():
     return render_template("home.html")


@auth.route('/contacts', methods=['GET','POST'])
def contacts():
     return render_template("contacts.html")

@auth.route('/aboutus', methods=['GET','POST'])
def aboutus():
     return render_template("about-us.html")

@auth.route('/flight_information', methods=['GET','POST'])
def flight_information():
     return render_template("flight_information.html")
 
@auth.route('/user_cart', methods=['GET','POST'])
def user_cart():
     return render_template("user_cart.html")

@auth.route('/payment', methods=['GET','POST'])
def payment():
     return render_template("payment.html")

@auth.route('/modify_tickets', methods=['GET','POST'])
def modify_tickets():
     return render_template("modify_tickets.html")

@auth.route('/user_update', methods=['GET','POST'])
def profile():
     return render_template("user_update.html")

@auth.route('/faq', methods=['GET','POST'])
def faq():
     return render_template("faq.html")

#ehtesham

@auth.route('/search', methods=['GET','POST'])
def search_flight():
    if request.method == 'POST':
        sourceLocation = request.form.get('sourceLocation')
        destinationLocation = request.form.get('destinationLocation')
        departureDate = request.form.get('departureDate')
        returnDate = request.form.get('returnDate')
        adults = request.form.get('adults')
        children = request.form.get('children')

        search_flight = Flight.query.filter_by\
            (sourceLocation=sourceLocation, destinationLocation=destinationLocation, departureDate=departureDate)\
                .first()

        if search_flight:
            return render_template('search_result.html', user = current_user, messages={\
                'sLocation' : search_flight.sourceLocation,\
                    'dLocation' : search_flight.destinationLocation,\
                        'dDate' : search_flight.departureDate,\
                            'rDate' : search_flight.returnDate,\
                                'nAdults' : search_flight.adults,\
                                    'nChildren' : search_flight.children}\
                    )
        #flash('Not Found', category='error')
        return "", "500 Not Found"
    return render_template("search_result.html", user = current_user)

@auth.route('/home', methods=['GET'])
def dropdown():
    seat_type = ['Business', 'Economy', 'Permium']
    return render_template('search.html', seat_type=seat_type, user = current_user)

@auth.route('/search_post', methods=['GET','POST'])
def search_post():
    #if request.method == 'POST':
    heading = ("Name","Price","Type","Note")
    data = (("Air Transat","CAD 251","Non-refundable","Only 3 seat left at this price"),
            ("Air Canada","CAD 200","Free cancelation","Only 1 seat left"),
            ("Flair Airlines","CAD 300","Non-refundable","Only 6 seat left at this price on our site"),
            ("WestJet Airlines","CAD 251","Non-refundable","Only 3 seat left at this price"),
            ("Air Transat","CAD 251","Non-refundable","Only 3 seat left at this price"),
            ("Air Canada","CAD 200","Free cancelation","Only 1 seat left"),
            ("Flair Airlines","CAD 300","Non-refundable","Only 6 seat left at this price on our site"),
            ("WestJet Airlines","CAD 251","Non-refundable","Only 3 seat left at this price"))
    return render_template("search_result.html", heading=heading, data=data)


# Maryam:
@auth.route('/user-account', methods=['GET','POST'])
@login_required 
def user_account():
    return render_template("user_account.html",user = current_user)

@auth.route('/update', methods=['GET','POST'])
def update():
    return render_template("user_account.html",user = current_user)

@auth.route('/edit', methods=['GET','POST'])
def edit():
    return render_template("user_update.html", user = current_user) 


@auth.route('/edit-user', methods=['GET','POST'])
def edit_user():
    if request.method == 'POST':
        print ("check point 1")
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmedPassword')
        gender = request.form.get('gender')

        phone = request.form.get('phone')
        birthday = request.form.get('birthday')
        adress = request.form.get('adress')
        city = request.form.get('city')
        country = request.form.get('country')
        postal = request.form.get('postal')
        
        is_alertifly = request.form.get('is_alertifly')
        
        user = User.query.filter_by(email=current_user.email).first()
        if user is None:
            return "", "500 Username or Email is already  exist"
        elif not email_validation(email):
            #flash('Your email address is not valid!', category='error')
            return "", "500 Your email address is not valid!"
        elif not name_validation(first_name):
            #flash('Your name is incorrect', category='error')
            return "", "500 Your name is incorrect"
        elif password != confirmed_password:
            #flash('Your passwords do not match!', category='error')
            return "", "500 Your passwords do not match!"
        elif password != "" and not password_validation(password)[0]:
            #flash(password_validation(password)[1], category='error' )
            return "", "500 " + str(password_validation(password)[1])
        elif is_alertifly == '1' : 
           return render_template("user_update.html", user=current_user)
        else:
            user.first_name= first_name
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            user.gender = gender
            user.phonenumber = phone
            user.birthday = birthday
            user.address = adress
            user.city = city
            user.country = country
            user.postalcode = postal    
            
            db.session.commit()

            db.session.commit()
            user = User.query.filter_by(email=email).first()
            flash('Your profile is updated!', category='success')

            return render_template("user_account.html", user=user)
    else:
        print ("check point 3")
        return render_template("user_update.html", user=current_user)

@auth.route('/admin', methods=['GET', 'POST'])
def edit_ticket():
    heading = ("source_name","destination_name","departure_date","return_date", "price", "airline")
    data = Tickett.query.all()
    data2 = (("Montreal","Ottawa","03/26/2022","04/01/2022","200 CAD", "Air Canada"),
            ("Montreal","Toronto","12/26/2022","23/01/2022","150 CAD", "Air Canada"),
            ("Montreal","Vancouver","05/26/2022","07/01/2022","300 CAD", "Air Canada"))
    return render_template("admin.html", heading=heading, data=data)

@auth.route('/add-ticket', methods=['GET', 'POST'])
def add_ticket():
    if request.method == 'POST':
        source_name = request.form.get('source_name')
        destination_name = request.form.get('destination_name')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        price = request.form.get('price')
        airline = request.form.get('airline')
        is_alertifly = request.form.get('is_alertifly')

        if not name_validation(source_name):
            #flash('Source name is incorrect', category='error')
            return "", "500 Source name is incorrect"
        elif not name_validation(destination_name):
            #flash('Destination name is incorrect', category='error')
            return "", "500 Destination name is incorrect"
        elif not name_validation(airline):
            #flash('Airline name is incorrect', category='error')
            return "", "500 Airline name is incorrect"
        elif (price is None):
            #flash('Price field is empty', category='error')
            return "", "500 Price field is empty"
        elif (departure_date is None):
            #flash('Departure date field is empty', category='error')
            return "", "500 Departure date field is empty"
        elif (return_date is None):
            #flash('Return date date field is empty', category='error')
            return "", "500 Return date date field is empty"
        elif is_alertifly == '1' : 
           return render_template("add_ticket.html", user=current_user)
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
            return redirect(url_for('auth.edit_ticket'))
    else :
        return render_template("add_ticket.html", user = current_user)
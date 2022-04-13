
from flask import Blueprint, render_template,request, flash, redirect, url_for,Response,session
from . import db
from .models import User
from .models import Ticket,history_ticket
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from .validations import *
auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        
        is_alertifly = request.form.get('is_alertifly')

        if email == '' : return "Email is empty" , 500
        if password == '' : return "Password is empty", 500
        if user:
            if check_password_hash(user.password, password):
                if is_alertifly == '1' : 
                    return render_template("login.html", user=user) 
                if email == "admin@besticket.ir":
                    flash('logged in successfully as an Admin!', category='success')
                else: 
                    flash('logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                return "Incorrect password" , 500
        else:
            return "Email not found" , 500
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
        postal = request.form.get('zipcode')
        #userType = request.form.get('admin')
        
        is_alertifly = request.form.get('is_alertifly')

        
        user = User.query.filter_by(email=email).first()
        if user:
            return "Username or Email is already exist", 500
        elif not email_validation(email):
            return "Your email address is not valid!", 500
        elif not name_validation(first_name):
            return "Your name is incorrect", 500
        elif password != confirmed_password:
            return "Your passwords do not match!", 500
        elif not password_validation(password)[0]:
            return str(password_validation(password)[1]),500
        elif postal != "" and  not postalValidate(postal):
            return "Your zipcode is not valid!", 500
        elif is_alertifly == '1' : 
           return render_template("sign_up.html", user=current_user) 
        else:
            new_user = User(email = email,
                            first_name=first_name,
                            password=generate_password_hash(password, method='sha256'),
                            admin=False,
                            #gender=gender,
                            phonenumber=phone,
                            #birthday=birthday,
                            #address= adress,
                            city=city,
                            country=country,
                            postalcode=postal
                            )
            db.session.add(new_user)
            db.session.commit()
            flash('You successfully signed up and also logged in!', category='success')
            login_user(new_user, remember=True)

            return redirect(url_for('views.home'))
        #return render_template("home.html", user=user)
    else:
        return render_template("sign_up.html", user = current_user)



@auth.route('/edit-user', methods=['GET','POST'])
def edit_user():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password = request.form.get('password')
        confirmed_password = request.form.get('confirmedPassword')
        gender = request.form.get('gender')

        phone = request.form.get('phone')
        #birthday = request.form.get('birthday')
        #adress = request.form.get('adress')
        city = request.form.get('city')
        country = request.form.get('country')
        postal = request.form.get('zipcode')
        
        is_alertifly = request.form.get('is_alertifly')

        user = User.query.filter_by(email=current_user.email).first()
        if user is None:
            return "Username or Email is not exist", 500
        if current_user.admin == True:
            return "You are Admin! your data can not change!!!", 500
        elif not email_validation(email):
            return "Your email address is not valid!", 500
        elif not name_validation(first_name):
            return "Your name is incorrect",500
        elif password != confirmed_password:
            return "Your passwords do not match!", 500
        elif password != "" and not password_validation(password)[0]:
            return str(password_validation(password)[1]), 500
        elif postal != "" and  not postalValidate(postal):
            return "Your zipcode is not valid!", 500
        elif is_alertifly == '1' : 
           return render_template("user_update.html", user=current_user)
        else:
            user.first_name= first_name
            user.email = email
            user.password = generate_password_hash(password, method='sha256')
            #user.gender = gender
            user.phonenumber = phone
            #user.birthday = birthday
            #user.address = adress
            user.city = city
            user.country = country
            user.postalcode = postal    
            
            db.session.commit()

            user = User.query.filter_by(email=email).first()
            flash('Your profile is updated!', category='success')

            return render_template("user_account.html", user=user)
    else:
        return render_template("user_update.html", user=current_user)

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
    user = User.query.filter_by(email=current_user.email).first()
    user_id = user.id
    heading = ()
    discp = ""
    userTickets = history_ticket.query.join(
         User, Ticket,
    ).filter(
         user_id == history_ticket.user_id,
    ).filter(
         Ticket.id == history_ticket.ticket_id,
    ).add_columns(
                  history_ticket.date,
                  Ticket.source_name,
                  Ticket.destination_name,
                  Ticket.departure_date,
                  Ticket.return_date,
                  Ticket.price,
                  Ticket.airline                
                  ).all()
    if len(userTickets) > 0 : 
        heading = ("purchase time","source_name","destination_name","departure_date","return_date", "price", "airline")
    else : 
        discp = "You have not purchase any ticket yet!"
        
    return render_template("user_cart.html" , data = userTickets , headings = heading,discp=discp)

@auth.route('/payment', methods=['GET','POST'])
def payment():   
            
    ticket_id =request.args.get('ticket_id' , None)
    ticket = Ticket.query.filter_by(id=ticket_id).first()

    if request.method == 'POST':
        cname = request.form.get('cname')
        cardnumber = request.form.get('ccnum')
        expmonth = request.form.get('expmonth')
        expyear = request.form.get('expyear')
        cvv = request.form.get('cvv')
        
        is_alertifly = request.form.get('is_alertifly')
        user = User.query.filter_by(email=current_user.email).first()

        if user is None:
            return "User is not signed in or deleted from database!", 500
        if cname is None or cname == "" :
           return "Card name is empty", 500
        if not name_validation(cname):
             return "Your name is not valid!", 500
        elif cardnumber is None or cardnumber == "" :
            return "Card number is empty", 500
        elif not cardVAlidation(cardnumber) :
             return "Card number is not valid!", 500
        #elif expmonth is None or expmonth == "" :
        #   return "Card expired month is empty", 500
        elif expyear is None or expyear == "" :
            return "Card expired year is empty", 500
        elif cvv is None or cvv == "" :
            return "Cvv is empty", 500
        
        elif is_alertifly == '1' :          
            return render_template("payment.html", user=current_user,ticket = ticket)
        else :

            new_ticket_user = history_ticket(user_id = user.id, ticket_id = ticket.id) 
            db.session.add(new_ticket_user)
            db.session.commit()       
            
            flash('You successfully buy the Ticket and it has been added to your profile', category='success')
            #return render_template("user_cart.html", user=current_user) 
            return redirect(url_for('auth.user_cart'))  
    else : 
        #session['my_var'] = 'reza'
        return render_template("payment.html" , ticket = ticket)

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


@auth.route('/home', methods=['GET'])
def dropdown():
    seat_type = ['Business', 'Economy', 'Permium']
    source = ['Montreal', 'Vancouver', 'Toronto']
    destination = ['Newyork', 'Seattle', 'Vancouver','Babolsar', 'Babol']
    return render_template('home.html', seat_type=seat_type,source=source, destination=destination, user = current_user)

# Reza
@auth.route('/', methods=['GET','POST'])
def home():
    if request.method == 'POST':
        heading = ("Source","Destination","Departure date","Return date", "Price", "Airline")
        source = request.form.get('source_name')
        destination = request.form.get('destination_name')
        seat_type = request.form.get('seat_type')
        end_date = request.form.get('end_date')
        start_date = request.form.get('start_date')
    
        is_alertifly = request.form.get('is_alertifly')
        
        
       # start_date2 = datetime.strptime(start_date, '%m-%d-%Y')
        #end_date = datetime.strptime(end_date, '%m-%d-%Y')
        
        print("reza",source,destination)
        if start_date is None or start_date == "":
            start_date = "00-00-0000"
        if end_date is None or end_date == "":
            end_date = "99-99-9999"
        data = []
        
        if source != "Choose the source" and destination != "Choose the destination":
            data = Ticket.query.filter_by( destination_name = destination,source_name = source).filter(Ticket.departure_date >= start_date, Ticket.return_date <= end_date).all()
        elif source != "Choose the source" :
            data = Ticket.query.filter_by(source_name = source).filter(Ticket.departure_date >= start_date, Ticket.return_date <= end_date).all()
        elif destination != "Choose the destination":
            data = Ticket.query.filter_by( destination_name = destination).filter(Ticket.departure_date >= start_date, Ticket.return_date <= end_date).all()
        else: 
            data = Ticket.query.filter(Ticket.departure_date >= start_date, Ticket.return_date <= end_date).all()

      
        #data = Ticket.query.filter_by(source_name = source,).filter(Ticket.departure_date >= start_date, Ticket.return_date <= end_date).all()

        #data = Ticket.query.filter(Ticket.departure_date >= start_date).all()

        
        if len(data) == 0:
            flash('There is no flight available based on your filter', category='error')
            #return "There is no flight available based on your filter", 500
            #return redirect(url_for('auth.search_post'))
            return render_template("search_result.html", headings=heading, data=data)
    
        print("check 3")
        return render_template("search_result.html", headings=heading, data=data)
    
    else :
        seat_type = ['Business', 'Economy', 'Permium','reza']
        source = ['Montreal', 'Vancouver', 'Toronto','Newyork', 'Seattle','Babol', 'Babolsar','Amol']
        destination = ['Montreal', 'Vancouver', 'Toronto','Newyork', 'Seattle','Babol', 'Babolsar','Amol']
        return render_template('home.html', seat_type=seat_type,source=source, destination=destination, user = current_user)
    
@auth.route('/search_post', methods=['GET','POST'])
def search_post():
    if request.method == 'POST':
        print("post")
    else:
        heading = ("source_name","destination_name","departure_date","return_date", "price", "airline")
        data = Ticket.query.all()       
        if len(data) == 0:
                flash('There is no flight available based on your filter', category='error')
                return render_template("search_result.html", heading=heading, data=data)
        return render_template("search_result.html", headings=heading, data=data)

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



@auth.route('/admin', methods=['GET', 'POST'])
def edit_ticket():
    if not current_user.admin :
        return  "Access denied!", 500
    heading = ("source_name","destination_name","departure_date","return_date", "price", "airline")
    data = Ticket.query.all()
    return render_template("admin.html", heading=heading, data=data)

@auth.route('/add-ticket', methods=['GET', 'POST'])
def add_ticket():
    if not current_user.admin :
        return "Access denied!", 500
    if request.method == 'POST':
        source_name = request.form.get('source_name')
        destination_name = request.form.get('destination_name')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')
        price = request.form.get('price')
        airline = request.form.get('airline')
        is_alertifly = request.form.get('is_alertifly')

        if not name_validation(source_name):
            return "Source name is incorrect", 500
        elif not name_validation(destination_name):
            return "Destination name is incorrect", 500
        #elif not name_validation(airline):
            #flash('Airline name is incorrect', category='error')
            #return "", "500 Airline name is incorrect"
        elif price is None or price == "":
            return "Price field is empty", 500
        elif departure_date is None or departure_date == "":
            return "Departure date field is empty", 500
        elif return_date is None or return_date == "":
            return "Return date date field is empty", 500
        elif price is None or price == "":
             return "Price filed is empty", 500 
        elif airline is None or airline == "": 
             return "Airline field is empty", 500
        
        elif is_alertifly == '1' : 
           return render_template("add_ticket.html", user=current_user)
        else:
            new_ticket = Ticket(source_name = source_name, 
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
        return "Not Found", 500
    return render_template("search_result.html", user = current_user)
from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import Flight
from . import db
from flask_login import login_user, login_required, logout_user, current_user
search = Blueprint('search', __name__)

@search.route('/search', methods=['GET','POST'])
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
        flash('Not Found', category='error')
    return render_template("search.html", user = current_user)


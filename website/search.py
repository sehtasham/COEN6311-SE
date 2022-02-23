from flask import Blueprint, render_template, flash, request, redirect, url_for
from .models import Ticket
from . import db
from flask_login import login_user, login_required, logout_user, current_user
search = Blueprint('search', __name__)

@search.route('/search', methods=['GET','POST'])
def search_flight():
    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        departureDate = request.form.get('departureDate')
        arrivalDate = request.form.get('arrivalDate')
        
        search_flight = Ticket.query.filter_by\
            (source=source, destination=destination, departureDate=departureDate)\
                .first()

        if search_flight:
            return render_template('search_result.html', user = current_user, messages={\
                'sLocation' : search_flight.source,\
                    'dLocation' : search_flight.destination,\
                        'dDate' : search_flight.departureDate,\
                            'rDate' : search_flight.arrivalDate}\
                    )
        flash('Not Found', category='error')
    return render_template("search.html", user = current_user)


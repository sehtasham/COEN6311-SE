from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint('views', __name__)

@views.route('/')
#@login_required
def home():
    seat_type = ['Business', 'Economy', 'Permium']
    source = ['Montreal', 'Vancouver', 'Toronto','Newyork', 'Seattle','Babol', 'Babolsar','Amol']
    destination = ['Montreal', 'Vancouver', 'Toronto','Newyork', 'Seattle','Babol', 'Babolsar','Amol']
    return render_template('home.html', seat_type=seat_type,source=source, destination=destination, user = current_user)

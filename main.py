from subprocess import Popen
from ast import literal_eval
from flask import Flask, render_template, request, redirect, flash, url_for, session
from replit import db
from bcrypt import gensalt, hashpw, checkpw
from datetime import datetime
from random import randint

app = Flask(__name__)
DEBUG = True
app.secret_key = "hiMadamRosidah!"
app.jinja_env.add_extension('jinja2.ext.loopcontrols')

# if users key not exist, initiate it.
if not db.get('users'):
    db['users'] = {}
    
# if bookings key not exist, initiate it.
if not db.get('bookings'):
    db['bookings'] = {}

SERVICES = [
    {'type':"Basic Grooming", 'image' : "grooming.jpg", 'price' : "50"},
    {'type':"Medical Examination", 'image' : "medical.jpg", 'price' : "30"},
    {'type':"Gourmet Meals", 'image' : "cat-eat.jpeg", 'price' : "25"},
    {'type':"Live CCTV Footage", 'image' : "cctv.jpg", 'price' : "15"}
]

ROOMS = {
    'Standard': {'type': "Standard Suite", 'price': "50.00", 'beds': "1", 'image' : "/static/images/Normal-room.jpg"},
    'Deluxe': {'type': "Deluxe Suite", 'price': "65.00", 'beds': "2", 'image' : "/static/images/deluxe.jpeg"},
    'Premium': {'type': "Premium Suite", 'price': "85.00", 'beds': "4", 'image' : "/static/images/Premium-room.jpg"},
    'Penthouse': {'type': "Penthouse Suite", 'price': "100.00", 'beds': "3", 'image' : "/static/images/penthouseNEW.jpg"}
}

MEMBERS = [
    {'name': "Mohammad Faisal", 'role': "Head Meow Developer", 'image':"/static/images/pfps/faicat.jpg", 'quote':"\"Cats have it all: admiration, an endless sleep, and company only when they want it.\" - Rod McKuen"},
    {'name': "Aliff Ramli", 'role': "Senior Meow Developer", 'image':"/static/images/pfps/aliffcat.jpg", 'quote':"\"If cats could talk, they wouldn't.\" - Nan Porter"},
    {'name': "Marwan Syahmi", 'role': "Junior Meow Developer", 'image':"/static/images/pfps/marcat.jpg", 'quote':"\"Sleep is the golden chain that ties health and our bodies together\" - Thomas Dekker"},
    {'name': "Rozaimi Adam", 'role': "Junior Meow Developer", 'image':"/static/images/pfps/rorocat.jpg", 'quote':"\"My cat can't see if she closed her eyes.\" "}
]

temp_user = {
    'rand@gmail.com' : {
        'fname' : 'Mohammad',
        'lname' : 'Faisal',
        'pfp' : 'faicat.jpg',
    },
}

temp_booking = {
    'rand@gmail.com' : {
        'fname' : 'Mohammad',
        'lname' : 'Faisal',
        'pfp' : 'faicat.jpg',
        'room' : 'Standard',
        'date' : '2023-03-20',
        'time' : '10:00',
        'duration' : '1 hour',
        'status' : 'Pending',
    }
}

def convert_form_dict(immutable_dict):
    # Initialize the result dictionary
    result_dict = {}
    no_cats = 0

    # Iterate over the items in the immutable dictionary
    for key, value in immutable_dict.items():
        # Check if the key starts with 'cat-'
        if key.startswith('cat-'):
            # Extract the cat number from the key
            cat_number = key.split('-')[1]
            no_cats = cat_number

            # If the cat number is not already in the result dictionary, add it
            if f'cat-{cat_number}' not in result_dict:
                result_dict[f'cat-{cat_number}'] = {}

            # Extract the cat detail type (name, gender, age, kg, breed)
            cat_detail_type = key.split('-')[2]

            # Add the cat detail to the result dictionary
            result_dict[f'cat-{cat_number}'][cat_detail_type] = value
        else:
            # For non-cat keys, directly add them to the result dictionary
            result_dict[key] = value

    return result_dict, no_cats


@app.route('/')
def index():
    return render_template('home.html', services=SERVICES, rooms=ROOMS, title="Home")

@app.route('/reserve')
def reserve():
    id = request.args.get('id', None)
    if not id:
        flash("Please select a room before reserving.")
        return redirect(url_for('rooms'))

    return render_template('reservation.html', services=SERVICES, room=ROOMS[id], id=id, title="Reservation")

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', rooms=ROOMS, title="Rooms")

@app.route('/login', methods=['GET','POST'])
def login():
    """ If request method is GET, return template for the login page.\n
        If request method is POST, validate login credentials and redirect user."""
    if request.method == 'GET':
        return render_template('login.html', title="Login", light_head=True)

    # Validate user credentials.
    if db['users'].get(request.form['email']):
        hashed_pass = db['users'][request.form['email']]['password']
        if checkpw(request.form['password'].encode(), hashed_pass.encode()):
            session['user'] = {'fname': db['users'][request.form['email']]['fname'], 'lname': db['users'][request.form['email']]['lname'], 'email': request.form['email'], 'pfp': db['users'][request.form['email']]['pfp'], 'number': db['users'][request.form['email']]['number']}
            flash("Successfully Logged In", "success")
            return redirect(url_for('dashboard'))

    # Flash invalid message if either email or password is incorrect
    flash("Invalid Login Credentials", "danger")
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    """ If request method is GET, return template for the registeration page.\n
        If request method is POST, check if email is not in database and add user details into database."""
    if request.method == 'GET':
        return render_template('registeration.html', title="Register", light_head=True)

    if not db['users'].get(request.form['email'], None):
        db['users'][request.form['email']] = {
            'number': 00000,
            'fname': request.form['fname'],
            'lname': request.form['lname'],
            'pfp': "default-pfp.jpg",
            'password': hashpw(request.form['password'].encode(), gensalt()).decode()
        }
        
        session['user'] = {'fname': db['users'][request.form['email']]['fname'], 'lname': db['users'][request.form['email']]['lname'], 'email': request.form['email'], 'pfp': db['users'][request.form['email']]['pfp'], 'number': db['users'][request.form['email']]['number']}
        flash("Registration Successful", "success")
        return redirect(url_for('dashboard'))

    # If email is already in database
    flash("Email already exists", "danger")
    return redirect(url_for('register'))

@app.route('/logout')
def logout():
    """ If user is logged in, destroy session and redirect user to login page."""
    if session.get('user'):
        session.pop('user')
        flash("Logout Successful", "success")
        return redirect(url_for('login'))

    flash("You are not logged in", "danger")
    return redirect(url_for('login'))

@app.route('/dashboard')
def dashboard():
    if not session.get('user', None):
        flash('Please login to view your profile', 'danger')
        return redirect(url_for('login'))

    if not db['bookings'].get(session['user']['email'], None):
        db['bookings'][session['user']['email']] = []

    for booking in db['bookings'][session['user']['email']]:
        room = ROOMS[booking['room-id']]
        booking['room'] = room

        date = datetime.strptime(booking['checkin'], "%Y-%m-%d")
        current = datetime.now().strftime("%Y-%m-%d")
        current_date = datetime.strptime(current, "%Y-%m-%d")
        if date == current_date:
            booking['status'] = "ONGOING"
        elif date > current_date:
            booking['status'] = "PENDING"
        else:
            booking['status'] = "COMPLETED"

        if not booking.get('uuid', None): # temporary
            booking['uuid'] = str(randint(1, 99999))

    
    return render_template('profile/dashboard.html', title="Dashboard", bookings=db['bookings'][session['user']['email']], services=SERVICES)

@app.route('/manage')
def manage():
    if not session.get('user', None):
        flash('Please login to view your profile', 'danger')
        return redirect(url_for('login'))
    return render_template('profile/manage.html', title="Manage")


@app.route('/profile')
def profile():
    return redirect(url_for('dashboard'))

@app.route('/payment', methods=['POST'])
def payment():
    room = ROOMS[request.form['room-id']]

    formatted, no_cats = convert_form_dict(request.form)
    print(formatted, room)
    
    return render_template('payment.html', title="Payment", data=formatted, room=room, no_cats=no_cats)

    
@app.route('/payment/process', methods=['POST'])
def process():
    data = literal_eval(request.form['data'])
    if not db['bookings'].get(data['email'], None):
        db['bookings'][data['email']] = []

    data['uuid'] = randint(10000,99999)
    db['bookings'][data['email']].append(data)
    
    flash("Payment Successful, you booking number is " + str(data['uuid']), "success")
    return redirect(url_for('index'))


@app.route('/about')
def aboutus():
    return render_template('about.html', members=MEMBERS, title="About Us")

@app.route('/tos')
def tos():
    return render_template('tos.html', title="Terms of Service")


@app.route('/update/name', methods=['POST'])
def update_name():
    if not session.get('user', None):
        flash("Please login to update your details", "danger")
        return redirect(url_for('login'))

    db['users'][session['user']['email']]['fname'] = request.form['fname']
    db['users'][session['user']['email']]['lname'] = request.form['lname']

    session['user']['fname'] = request.form['fname']
    session['user']['lname'] = request.form['lname']

    flash("Name updated successfully", "success")
    return redirect(url_for('manage'))

@app.route('/update/email', methods=['POST'])
def update_email():
    if not session.get('user', None):
        flash("Please login to update your details", "danger")
        return redirect(url_for('login'))

    db['users'][request.form['email']] = db['users'][session['user']['email']]
    del db['users'][session['user']['email']]

    db['bookings'][request.form['email']] = db['bookings'][session['user']['email']]
    del db['bookings'][session['user']['email']]

    session['user']['email'] = request.form['email']

    flash(f"Email updated to {request.form['email']}", "success")
    return redirect(url_for('manage'))

@app.route('/update/number', methods=['POST'])
def update_number():
    if not session.get('user', None):
        flash("Please login to update your details", "danger")
        return redirect(url_for('login'))

    db['users'][session['user']['email']]['number'] = request.form['number']

    session['user']['number'] = request.form['number']

    flash("Number updated successfully", "success")
    return redirect(url_for('manage'))

@app.route('/update/pfp', methods=['POST'])
def update_pfp():
    if not session.get('user', None):
        flash("Please login to update your details", "danger")
        return redirect(url_for('login'))

    
    img_id = str(randint(1000000, 9999999))
    db['users'][session['user']['email']]['pfp'] = img_id + request.files['pfp'].filename[-4:]

    with open("static/images/pfps/" + img_id + request.files['pfp'].filename[-4:], 'wb') as pfpFile:
        pfpFile.write(request.files['pfp'].read())
        pfpFile.close()

    session['user']['pfp'] = img_id + request.files['pfp'].filename[-4:]

    flash("Succesfully updated profile picture")
    return redirect(url_for('manage'))


@app.route('/update/password', methods=['POST'])
def update_pass():
    if not session.get('user', None):
        flash("Please login to update your details", "danger")
        return redirect(url_for('login'))

    if not checkpw(request.form['oldpass'].encode(), db['users'][session['user']['email']]['password'].encode()):
        flash("Old password is incorrect", "danger")
        return redirect(url_for('manage'))

    db['users'][session['user']['email']]['password'] = hashpw(request.form['newpass'].encode(), gensalt()).decode()
    flash("Password updated successfully", "success")
    return redirect(url_for('logout'))

@app.route("/debug")
def debug():
    print(db['users'])
    return redirect(url_for('index'))


@app.route("/debug/bookings")
def debug_bookings():
    print(db['bookings'])
    return redirect(url_for('index'))


if __name__ == '__main__':
    if DEBUG:
        Popen('npx tailwindcss -i ./static/css/home.css -o ./static/css/output.css --watch', shell=True)
    app.run(host='0.0.0.0', port=81, debug=DEBUG)

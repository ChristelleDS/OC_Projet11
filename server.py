import json
from flask import Flask,render_template,request,redirect,flash,url_for


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/showSummary',methods=['POST'])
def showSummary():
    club = [club for club in clubs if club['email'] == request.form['email']][0]
    return render_template('welcome.html',club=club,competitions=competitions)


@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def is_booking_authorized(competition, club, placesRequired):
    """
    Check if the club is authorized to book the number of places required
    :param competition: current competition dict
    :param club: current club dict
    :param placesRequired: nb of places required
    :return: True(authorized) or False, and the flash message to raise
    """
    competition = competition
    club = club
    placesRequired = placesRequired
    placesAvailable = int(competition['numberOfPlaces'])
    club_points = int(club['points'])
    # Tournament is complete
    if placesAvailable <= 0:
        message = 'Sorry, complete tournament!'
        return False, message
    # can't book more than 12 places for a competition
    elif placesRequired > 12:
        message = 'booking more than 12 places is not authorized'
        return False, message
    # Required places >= 0
    # and < available places
    elif placesRequired <= 0 or placesRequired > placesAvailable:
        message = 'Something went wrong : incorrect number of places'
        return False, message
    # club has not enough points
    elif placesRequired > club_points:
        message = 'No enough points!'
        return False, message
    # Booking conditions OK
    else:
        message = 'Great-booking complete!'
        return True, message


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    placesAvailable = int(competition['numberOfPlaces'])
    club_points = int(club['points'])
    authorized = is_booking_authorized(competition, club, placesRequired)[0]
    message = is_booking_authorized(competition, club, placesRequired)[1]
    flash(message)
    if authorized is True:
        competition['numberOfPlaces'] = placesAvailable-placesRequired
        club['points'] = club_points-placesRequired
        return render_template('welcome.html', club=club, competitions=competitions)
    else:
        return render_template('booking.html', club=club, competition=competition)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
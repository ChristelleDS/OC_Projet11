import json
from flask import Flask, render_template, request, redirect, flash, url_for
import datetime


clubs_json = 'clubs.json'
competitions_json = 'competitions.json'


def loadClubs():
    with open(clubs_json) as c:
        listOfClubs = json.load(c)['clubs']
        return listOfClubs


def loadCompetitions():
    with open(competitions_json) as comps:
        listOfCompetitions = json.load(comps)['competitions']
        return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'

competitions = loadCompetitions()
clubs = loadClubs()


@app.route('/')
def index():
    return render_template('index.html')


def convert_strToDate(date_time):
    """
    Function to convert string to datetime
    """
    datetime_str = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    return datetime_str


def get_open_competitions(competitions):
    """
    Function to return only future competitions
    :param competitions: competitions list
    :return: list of future competitions
    """
    open_comp = [c for c in competitions if convert_strToDate(c['date']) > datetime.datetime.now()]
    return open_comp


def update_points(points, bookings, club_index, compet):
    """
    Function to update points of the club
    :param points: updated points number of the club
    :param bookings: bookings of the club
    :param club_index: index of the club
    :param compet: competition name
    :return:
    """
    with open(clubs_json) as f:
        data = json.load(f)
        data['clubs'][club_index]['points'] = points
        data['clubs'][club_index]['bookings'][compet] = bookings
        json.dump(data, open(clubs_json, 'w'), indent=4)


def update_places(places, compet_index):
    """
    Function to update available places of the competition
    :param places: new number of available places
    :param compet_index: index of the competition
    """
    with open(competitions_json) as f:
        data = json.load(f)
        data['competitions'][compet_index]['numberOfPlaces'] = places
        json.dump(data, open(competitions_json, 'w'), indent=4)


@app.route('/showSummary', methods=['POST'])
def showSummary():
    # check given email is an authorized login and correct format
    try:
        club = [club for club in clubs if club['email'] == request.form['email']][0]
        # affichage des compétitions futures
        list_compet = get_open_competitions(competitions)
        if list_compet:
            return render_template('welcome.html', club=club, competitions=list_compet)
        else:
            flash("No coming competition")
            return render_template('welcome.html', club=club, competitions="")
    except IndexError:
        flash("Login error, please try again.")
        return redirect(url_for('index'))


@app.route('/book/<competition>/<club>')
def book(competition, club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html', club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong - invalid club or competition")
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
    club_bookings = int(club['bookings'][competition['name']])  # places already booked
    # Tournament is complete
    if placesAvailable <= 0:
        message = 'Sorry, complete tournament!'
        return False, message
    # can't book more than 12 places for a competition
    elif club_bookings + placesRequired > 12:
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


@app.route('/purchasePlaces', methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    club_bookings = int(club['bookings'][competition['name']])  # places already booked
    placesRequired = int(request.form['places'])
    placesAvailable = int(competition['numberOfPlaces'])
    club_points = int(club['points'])
    competitions_futures = get_open_competitions(competitions)
    authorized = is_booking_authorized(competition, club, placesRequired)[0]
    message = is_booking_authorized(competition, club, placesRequired)[1]
    flash(message)
    if authorized is True:
        # update club points + update places available in the competition
        competition['numberOfPlaces'] = placesAvailable - placesRequired
        club['points'] = club_points - placesRequired
        places_book = club_bookings + placesRequired
        update_places(places=str(competition['numberOfPlaces']),
                      compet_index=competitions.index(competition))
        update_points(points=str(club['points']),
                      bookings=str(places_book),
                      club_index=clubs.index(club),
                      compet=competition['name'])
        return render_template('welcome.html', club=club, competitions=competitions_futures)
    else:
        return render_template('booking.html', club=club, competition=competition)


@app.route('/pointsBoard')
def pointsBoard():
    """
    Display a board of all clubs and respective points,
    sorted alphabetically
    """
    sorted_list = sorted(clubs, key=lambda item: item['name'])
    return render_template('board.html', clubs=sorted_list)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))

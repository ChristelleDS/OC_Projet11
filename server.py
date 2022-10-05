import json
from flask import Flask,render_template,request,redirect,flash,url_for
import datetime


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


# Function to convert string to datetime
def convert_strToDate(date_time):
    datetime_str = datetime.datetime.strptime(date_time, '%Y-%m-%d %H:%M:%S')
    return datetime_str

def get_open_competitions(competitions):
    open_comp = [c for c in competitions if convert_strToDate(c['date']) > datetime.datetime.now()]
    return open_comp


@app.route('/showSummary',methods=['POST'])
def showSummary():
    # check given email is an authorized login
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
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    placesAvailable = int(competition['numberOfPlaces'])
    club_points = int(club['points'])
    # UC: tournoi complet
    if placesAvailable <= 0:
        flash('Sorry, complete tournament!')
        return render_template('welcome.html', club=club, competitions=competitions)
    # Nombre de place demandé >= 0 et < 12
    # et < au nombre de places disponibles
    if placesRequired <= 0 or placesRequired > 12\
            or placesRequired > placesAvailable:
        flash('Something went wrong : incorrect number of places')
        return render_template('booking.html', club=club, competition=competition)
    # UC: club n'a pas assez de points
    if placesRequired > club_points:
        flash('No enough points!')
        return render_template('booking.html', club=club, competition=competition)
    # cas passant: maj points
    competition['numberOfPlaces'] = placesAvailable-placesRequired
    club['points'] = club_points-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


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

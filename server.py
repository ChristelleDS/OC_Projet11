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
    # Nombre de place demandé doit être + et inférieur à 12
    # et inférieur au nombre de places disponibles
    elif placesRequired <= 0 or placesRequired > 12\
            or placesRequired > placesAvailable:
        flash('Something went wrong : incorrect number of places')
        return render_template('booking.html', club=club, competition=competition)
    # UC: club n'a pas assez de points
    elif placesRequired > club_points:
        flash('No enough points!')
        return render_template('booking.html', club=club, competition=competition)
    # cas passant: maj points
    else:
        competition['numberOfPlaces'] = placesAvailable-placesRequired
        club['points'] = club_points-placesRequired
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


# TODO: Add route for points display


@app.route('/logout')
def logout():
    return redirect(url_for('index'))
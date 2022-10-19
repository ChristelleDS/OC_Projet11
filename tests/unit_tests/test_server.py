from Python_Testing.server import index, logout, loadCompetitions, loadClubs, \
    book, purchasePlaces, convert_strToDate, get_open_competitions, competitions,\
    clubs, update_points, update_places, is_booking_authorized
from .conftest import auth_data, client, clubs_data, competitions_data, \
    compet_complete, compet_open, competitions_data_test, club_20, club_1, \
    compet_open_5
import pytest
import datetime
import requests
from flask import url_for
import urllib.parse

from ... import server


def test_loadClubs(mocker, clubs_data):
    """
    Mock CLUBS file with a test file equals to clubs_data fixture.
    """
    mocker.patch.object(server, "clubs_json", 'clubs_tests.json')
    loaded = loadClubs()
    assert loaded == clubs_data


def test_loadCompetitions(mocker, competitions_data):
    """
    Mock competititons file with a test file equals to competitions_data fixture.
    """
    mocker.patch.object(server, "competitions_json", 'competitions_init.json')
    loaded = loadCompetitions()
    assert loaded == competitions_data


def test_update_points():
    update_points("20", "4", 0, "Spring Festival")  # points, bookings, club_index, compet
    clubs = loadClubs()
    assert clubs[0]['points'] == '20'
    assert clubs[0]['bookings']['Spring Festival'] == '4'


def test_update_places():
    update_places("30", 0)  # places, compet_index
    competitions = loadCompetitions()
    assert competitions[0]['numberOfPlaces'] == '30'


def test_index(client):
    """
    Vérifie que la page répond bien (code 200)
    Vérifie que la page affichée est bien la page index
    """
    response = client.get('/')
    html = response.data.decode()
    assert response.status_code == 200
    assert "title>GUDLFT Registration</title>" in html
    assert "<form action=\"showSummary\" method=\"post\">" in html


def test_showSummary(client, auth_data, competitions_data):
    """
    Si l'email utilisé pour se logguer est connu,
    l'utilisateur est redirigé vers l'accueil.
    Vérifie que la page affichée est bien la page d'accueil.
    Vérifier les competitions affichées.
    """
    response = client.post('/showSummary', data={'email': auth_data["email"]})
    assert response.status_code == 200
    data = response.data.decode()
    assert "<title>Summary | GUDLFT Registration</title>" in data
    open_competitions = get_open_competitions(competitions_data)
    for c in open_competitions:
        assert c['name'] in data


def test_showSummary_noCompetition(client, auth_data, mocker, competitions_data_test):
    """
    Si l'email utilisé pour se logguer est connu,
    l'utilisateur est redirigé vers l'accueil.
    Vérifie que la page affichée est bien la page d'accueil.
    Vérifier le message affiché si aucune competition à venir.
    """
    mocker.patch.object(server, 'competitions', competitions_data_test)
    response = client.post('/showSummary', data={'email': auth_data["email"]})
    assert response.status_code == 200
    data = response.data.decode()
    assert "<title>Summary | GUDLFT Registration</title>" in data
    # test du flash message
    assert "No coming competition" in data


def test_should_not_login(client, auth_wrongdata):
    """
    Si l'email utilisé pour se logguer est inconnu (IndexError),
    une erreur doit être levée.
    L'utilisateur doit être renvoyé sur la page de connexion.
    """
    response = client.post('/showSummary', data=auth_wrongdata["email"],
                           follow_redirects=True)
    assert response.status_code == 400


def test_logout_redirect(client):
    """
    Lors d'une déconnexion l'utilisateur doit être redirigé
    vers la page index
    """
    response = client.get('/logout', follow_redirects=True)
    # Check that there was one redirect response.
    assert len(response.history) == 1
    # Check that the second request was to the index page.
    assert response.request.path == url_for("index")


def test_book_status(client):
    competition_tobook = "Spring Festival"
    club_connected = "Simply Lift"
    book_url = '/book/' + str(competition_tobook) + '/' + str(club_connected)
    response = client.get(book_url)
    assert response.status_code == 200
    assert "<title>Booking" in response.data.decode()


def test_book_wrongdata(client):
    competition_tobook = " "
    club_connected = "Simply"
    book_url = '/book/' + str(competition_tobook) + '/' + str(club_connected)
    with pytest.raises(IndexError):
        response = client.get(book_url)


@pytest.mark.parametrize("club_jdd, places_required_jdd, competition_jdd, expected_boolean, expected_message",
                         [(0, 13, 0, False, "booking more than 12 places is not authorized"),
                          (0, 2, 2, False, "Sorry, complete tournament!"),
                          (1, 6, 0, False, "Not enough points!"),
                          (0, 7, 3, False, "No more places available for this competition, incorrect number"),
                          (0, 0, 0, False, "No more places available for this competition, incorrect number"),
                          (0, 1, 0, True, "Great-booking complete!")])
def test_is_booking_authorized(club_jdd, places_required_jdd, competition_jdd,
                               expected_boolean, expected_message):
    # mocker.patch.object(server, 'competitions', competition_jdd)
    # mocker.patch.object(server, 'clubs', club_jdd)
    club = clubs[club_jdd]
    print(club)
    competition = competitions[competition_jdd]
    print(competition)
    value = is_booking_authorized(competition, club, places_required_jdd)[0]
    print(value)
    mess = is_booking_authorized(competition, club, places_required_jdd)[1]
    print(mess)
    assert value == expected_boolean
    assert mess  in expected_message


def test_purchasePlaces_OK(client):
    """
    Cas passant
    """
    club = clubs[2]
    compet = competitions[0]
    places_required = 1
    points_before = int(club['points'])
    places_before = int(compet['numberOfPlaces'])
    form = {'club': club['name'],
            'competition': compet['name'],
            'places': places_required}
    print(form)
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    data = response.data.decode()
    # 0 <= placesRequired <= 12
    # placesRequired >= points_before : le club a assez de points
    # placesRequired <= places_before : assez de places dispo
    assert data.find("Great-booking complete!") != -1
    """ verifier que le nbr de points est mis à jour"""
    updated_pts = points_before - places_required
    assert club['points'] == updated_pts
    """ vérifier que le nbr de places est mis à jour"""
    updated_places = places_before - places_required
    assert compet['numberOfPlaces'] == updated_places


def test_pointsBoard(client, clubs_data):
    response = client.get('/pointsBoard')
    assert response.status_code == 200
    data = response.data.decode()
    for c in clubs_data:
        assert c['name'] in data

from Python_Testing.server import index, logout, loadCompetitions, loadClubs, book, purchasePlaces, \
    convert_strToDate, get_open_competitions
from .conftest import auth_data, client, clubs_data, competitions_data, \
    compet_complete, compet_open, competitions_data_test, club_20, club_1, compet_open_5
import pytest
import datetime
import requests
from flask import session


def test_loadClubs(clubs_data):
    assert loadClubs() == clubs_data


def test_loadCompetitions(competitions_data):
    assert loadCompetitions() == competitions_data


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
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data
    open_competitions = get_open_competitions(competitions_data)
    for c in open_competitions:
        assert c['name'] in response.data


def test_showSummary_noCompetition(client, auth_data, competitions_data_test):
    """
    Si l'email utilisé pour se logguer est connu,
    l'utilisateur est redirigé vers l'accueil.
    Vérifie que la page affichée est bien la page d'accueil.
    Vérifier le message affiché si aucune competition à venir.
    """
    response = client.post('/showSummary', data={'email': auth_data["email"]})
    assert response.status_code == 200
    assert b"<title>Summary | GUDLFT Registration</title>" in response.data
    open_competitions = get_open_competitions(competitions_data_test)
    # test du flash message
    assert b"No coming competition" in response.data


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
    assert response.request.path == "/"


def test_book_status(client):
    print(compet_open)
    competition_tobook = "Spring Festival"
    club_connected = "Simply Lift"
    # assert club_connected in clubs_data
    # assert competition_tobook in competitions_data
    book_url = '/book/' + str(competition_tobook) + '/' + str(club_connected)
    response = client.get(book_url)
    assert response.status_code == 200
    html = response.data.decode()
    assert "<title>Booking" in html


def test_book_wrongdata(client):
    competition_tobook = " "
    club_connected = "Simply"
    book_url = '/book/' + str(competition_tobook) + '/' + str(club_connected)
    with pytest.raises(IndexError):
        response = client.get(book_url)


def test_purchasePlaces_complete(compet_complete, club_20, client):
    """
    UC: compétition complète
    """
    club = club_20
    competition = compet_complete
    places_required = 3
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    html = response.data.decode()
    if int(competition['numberOfPlaces']) <= 0:
        assert html.find("complete") != -1


def test_purchasePlaces_required0(compet_open, club_20, client):
    """
    UC1: club qui demande une réservation pour 0 place (non passant)
    """
    club = club_20
    competition = compet_open
    places_required = 0
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    html = response.data.decode()
    assert "Something went wrong" in html


def test_purchasePlaces_noMorePlaces(compet_open_5, club_20, client):
    """
    club ne peut pas réserver plus que de places disponibles
    """
    club = club_20
    competition = compet_open_5
    places_required = 7
    points_before = int(club['points'])
    places_before = int(competition['numberOfPlaces'])
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    data = response.data.decode()
    # placesRequired>places_before:
    assert data.find("Something went wrong") != -1


def test_purchasePlaces_limit12(compet_open, club_20, client):
    """
    Vérifier qu'un club ne peut pas réserver plus de 12 places
    """
    club = club_20
    competition = compet_open
    places_required = 13
    points_before = int(club['points'])
    places_before = int(competition['numberOfPlaces'])
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    data = response.data.decode()
    # placeRequired > 12
    assert data.find("Something went wrong") != -1


def test_purchasePlaces_NotEnoughPoints(compet_open, club_1, client):
    """
    UC4: club n'a pas assez de points
    """
    club = club_1
    competition = compet_open
    places_required = 2
    points_before = int(club['points'])
    places_before = int(competition['numberOfPlaces'])
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    # points_before > placesRequired
    assert b"Not enough points" in response.data


def test_purchasePlaces_OK(compet_open, club_1, client):
    """
    Cas passant
    """
    club = club_1
    competition = compet_open
    places_required = 1
    points_before = int(club['points'])
    places_before = int(competition['numberOfPlaces'])
    form = {'club': club['name'],
            'competition': competition['name'],
            'places': places_required}
    response = client.post('/purchasePlaces', data=form)
    assert response.status_code == 200
    data = response.data.decode()
    # 0 <= placesRequired <= 12
    # placesRequired >= points_before : le club a assez de points
    # placesRequired <= places_before : assez de places dispo
    assert data.find("Great-booking complete!") != -1
    """ verifier que le nbr de points est mis à jour"""
    new_points = points_before - places_required
    assert club['points'] == new_points
    message = 'Points available: ' + str(club['points'])
    assert message in data
    """ vérifier que le nbr de places est mis à jour"""
    assert competition['numberOfPlaces'] == (places_before - places_required)


def test_pointsBoard(client, clubs_data):
    response = client.get('/pointsBoard')
    assert response.status_code == 200
    data = response.data.decode()
    for c in clubs_data:
        assert c['name'] in data

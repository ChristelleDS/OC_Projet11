from Python_Testing.server import competitions, clubs, update_points, update_places
import pytest
from Python_Testing.tests.conftest import auth_data, client, clubs_data, competitions_data, \
    compet_complete, compet_open, competitions_data_test, club_20, club_1, \
    compet_open_5


def test_purchasePlaces_OK(client):
    """
    Cas passant
    """
    club = clubs[2]
    compet = competitions[0]
    club_init = int(club['bookings'][compet['name']])
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
    """ check that points number is updated"""
    updated_pts = points_before - places_required
    assert club['points'] == updated_pts
    """ check that places number is updated"""
    updated_places = places_before - places_required
    assert compet['numberOfPlaces'] == updated_places
    """ restaure initial data after the test"""
    update_places(places=str(places_before),
                  compet_index=0)
    update_points(points=str(points_before),
                  bookings=str(club_init),
                  club_index=2,
                  compet=compet['name'])

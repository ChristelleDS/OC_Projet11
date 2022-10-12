import pytest
from Python_Testing import server
from flask import template_rendered


@pytest.fixture
def client():
    new_app = server.app
    new_app.testing = True
    with new_app.test_client() as c:
        yield c


@pytest.fixture
def auth_data():
    login = {"email": "john@simplylift.co"}
    return login


@pytest.fixture
def auth_wrongdata():
    login = {"email": "notexist@yopmail.com"}
    return login


@pytest.fixture
def clubs_data():
    return [

        {

            "name":"Simply Lift",

            "email":"john@simplylift.co",

            "points":"13"

        },

        {

            "name":"Iron Temple",

            "email": "admin@irontemple.com",

            "points":"4"

        },

        {   "name":"She Lifts",

            "email": "kate@shelifts.co.uk",

            "points":"12"

        }

    ]


@pytest.fixture
def competitions_data():
    return [
        {
            "name": "Spring Festival",
            "date": "2023-03-27 10:00:00",
            "numberOfPlaces": "25"
        },
        {
            "name": "Fall Classic",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "13"
        }
    ]


@pytest.fixture
def competitions_data_test():
    return [
        {
            "name": "Past competition",
            "date": "2020-10-22 13:30:00",
            "numberOfPlaces": "30"
        }
    ]


@pytest.fixture
def compet_complete():
    compet = {"name": "Spring Festival",
            "date": "2022-10-27 10:00:00",
            "numberOfPlaces": "0"}
    return compet


@pytest.fixture
def compet_open():
    compet = {"name": "Spring Festival",
            "date": "2022-10-27 10:00:00",
            "numberOfPlaces": "20"}
    return compet


@pytest.fixture
def compet_open_5():
    compet = {"name": "Spring Festival",
            "date": "2022-10-27 10:00:00",
            "numberOfPlaces": "5"}
    return compet


@pytest.fixture
def club_20():
    club = {"name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"20"}
    return club


@pytest.fixture
def club_1():
    club = {"name":"Simply Lift",
        "email":"john@simplylift.co",
        "points":"1"}
    return club


@pytest.fixture
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)

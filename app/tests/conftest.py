import pytest
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.planet import Planet

@pytest.fixture
def app():
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def two_planets(app):
    planet1=Planet(name="Mercury", description="Smallest Planet", distance_from_sun=0.4)
    planet2=Planet(name="Venus", description="Hottest Planet", distance_from_sun=0.7)

    db.session.add(planet1)
    db.session.add(planet2)
    db.session.commit()
import pytest
import connexion

flask_app = connexion.FlaskApp(__name__)
flask_app.add_api('lingo/swagger/swagger.yaml')


@pytest.fixture(scope='module')
def client():
    with flask_app.app.test_client() as c:
        yield c


def test_health(client):
    response = client.get('/ping')
    assert response.status_code == 200


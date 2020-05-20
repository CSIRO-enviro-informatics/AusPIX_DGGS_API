import pytest
import json
from app import app

# use python -m pytest to run this test case
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_find_dggs_for_a_point_transform(client):
    res = client.get('/api/search/find_dggs_for_a_point?x=1549652.93&y=-3960378.34&epsg=3577&resolution=7')
    assert json.loads(res.data)['cell_id'] == 'R7852372'

def test_find_dggs_for_a_point(client):
    res = client.get('/api/search/find_dggs_for_a_point?x=149.124413&y=-35.307934&epsg=4326&resolution=7')
    assert json.loads(res.data)['cell_id'] == 'R7852372'

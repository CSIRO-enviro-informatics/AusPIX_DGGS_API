import json
from app import app
import unittest

# use python -m pytest to run this test case

class TestSequenceFunctions(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_find_dggs_for_a_point_transform(self):
        res = self.client.get('/api/search/find_dggs_for_a_point?x=1549652.93&y=-3960378.34&epsg=3577&resolution=7')
        assert json.loads(res.data)['dggs_cell_id'] == 'R7852372'

    def test_find_dggs_for_a_point(self):
        res = self.client.get('/api/search/find_dggs_for_a_point?x=149.124413&y=-35.307934&epsg=4326&resolution=7')
        assert json.loads(res.data)['dggs_cell_id'] == 'R7852372'

    def test_find_dggs_cells_within_polygon(self):
        geoJson = {
            "type": "Polygon",
            "coordinates": [
            [
                [
                149.07223105430603,
                -35.241045155903464
                ],
                [
                149.0769517421722,
                -35.241045155903464
                ],
                [
                149.0769517421722,
                -35.23764520319855
                ],
                [
                149.07223105430603,
                -35.23764520319855
                ],
                [
                149.07223105430603,
                -35.241045155903464
                ]
            ]
            ]
        }
        res = self.client.post('api/search/find_dggs_cells_within_polygon?resolution=10', json=geoJson)
        result = [
            "R7852344443",
            "R7852344444",
            "R7852344445",
            "R7852344446",
            "R7852344447",
            "R7852344448"
        ]
        self.assertListEqual(json.loads(res.data)['dggs_cells'], result)

if __name__ == '__main__':
    unittest.main()



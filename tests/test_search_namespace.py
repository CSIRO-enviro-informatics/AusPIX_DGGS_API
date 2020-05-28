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

    # Test Polygon
    def test_find_dggs_cells_by_geojson(self):
        geo_json = {
            "type": "FeatureCollection",
            "name": "Belconnen",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
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
                }
            ]
        }
        res = self.client.post('api/search/find_dggs_by_geojson?resolution=10', json=geo_json)
        result = [
            "R7852344443",
            "R7852344444",
            "R7852344445",
            "R7852344446",
            "R7852344447",
            "R7852344448"
        ]
        self.assertListEqual(json.loads(res.data)['dggs_cells'], result)
    # Test multi polygon
    def get_find_dggs_cells_by_geojson_multi_plygon(self):
        with open("ACT_SA1_Black_Mountain.geojson", "r") as file:
            geo_json = json.loads(file.read)
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=8', json=geo_json)
            result = [
                "R78523472",
                "R78523480",
                "R78523475",
                "R78523483",
                "R78523477"
            ]
            self.assertListEqual(json.loads(res.data)['dggs_cells'], result)
if __name__ == '__main__':
    unittest.main()



import json
from app import app
import unittest
import os
from .data.RoadsExample_geoJason_dggs_result import RoadsExampleResult
from .data.RoadsExample_geoJason_dggs_polygon_result import RoadsExamplePolygonResult
from .data.EIT_geojson_example_points_result import points_as_polygon_result, points_as_polygon_with_properties_result
from .data.ComplexPolyBasic_Result import complexPolyBasic_Result
current_dir = os.path.dirname(__file__)
print("current_dir", current_dir)
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
    def test_find_dggs_cells_by_geojson_polygon(self):
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
        res = self.client.post('api/search/find_dggs_by_geojson?resolution=10&dggs_as_polygon=False', json=geo_json)
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
    def test_find_dggs_cells_by_geojson_multi_polygon(self):
        print(os.path.dirname(__file__))
        with open(os.path.join(current_dir, "data/ACT_SA1_Black_Mountain.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=8&dggs_as_polygon=False', json=geo_json)
            result = [
                "R78523472",
                "R78523480",
                "R78523475",
                "R78523483",
                "R78523477"
            ]
            self.assertListEqual(json.loads(res.data)['dggs_cells'], result)
    # Test dggs cells for given geojson lines
    def test_find_dggs_cells_by_geojson_lines(self):
        with open(os.path.join(current_dir, "data/RoadsExample_geoJason.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=8&dggs_as_polygon=False', json=geo_json)
            self.assertEqual(json.loads(res.data)['meta']['cells_count'], 41)
            self.assertListEqual(json.loads(res.data)['dggs_cells'], RoadsExampleResult)
    # Test dggs cells as polygon features
    def test_find_dggs_cells_by_geojson_lines_as_polygon(self):
        with open(os.path.join(current_dir, "data/RoadsExample_geoJason.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=8&dggs_as_polygon=True&keep_properties=False', json=geo_json)
            self.assertListEqual(json.loads(res.data)['features'], RoadsExamplePolygonResult)

    def test_find_dggs_cells_by_geojson_points(self):
        with open(os.path.join(current_dir, "data/EIT_geojson_example_points.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=10&dggs_as_polygon=False', json=geo_json)
            self.assertListEqual(json.loads(res.data)['dggs_cells'], ["R7280344331", "R7280344334"])
    def test_find_dggs_cells_by_geojson_points_as_polygon_with_properties(self):
        with open(os.path.join(current_dir, "data/EIT_geojson_example_points.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=10&dggs_as_polygon=True', json=geo_json)
            self.assertListEqual(json.loads(res.data)['features'], points_as_polygon_with_properties_result)
    def test_find_dggs_cells_by_geojson_points_as_polygon(self):
        with open(os.path.join(current_dir, "data/EIT_geojson_example_points.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=10&dggs_as_polygon=True&keep_properties=False', json=geo_json)
            self.assertListEqual(json.loads(res.data)['features'], points_as_polygon_result)
    def test_find_dggs_cells_by_geojson_complex_polygon(self):
        with open(os.path.join(current_dir, "data/ComplexPolyBasic.geojson"), "r") as file:
            geo_json = json.loads(file.read())
            res = self.client.post('api/search/find_dggs_by_geojson?resolution=10&dggs_as_polygon=True&keep_properties=False', json=geo_json)
            print(len(json.loads(res.data)['features']), json.loads(res.data)['features'])
            print(len(complexPolyBasic_Result), complexPolyBasic_Result)
            self.assertListEqual(json.loads(res.data)['features'], complexPolyBasic_Result)
if __name__ == '__main__':
    unittest.main()



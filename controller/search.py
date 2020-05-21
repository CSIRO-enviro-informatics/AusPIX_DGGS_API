
from flask import Flask, Blueprint, request
from flask_restx import Namespace, Resource, reqparse, fields
from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
from pyproj import Transformer, exceptions
from pyshp import shapefile
import json

api = Namespace('search', description="Search from DGGS Engine", version="0.1")


bounding_box = api.model('BoundingBox', {
    'x_lat': fields.Float(),
    'y_lat': fields.Float(),
    'x_lng': fields.Float(),
    'y_lng': fields.Float(),
})

polygon = api.model('PolygonGeometry', {
    'type': fields.String(required=True, default="Polygon"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True, type="Array",
        default=[[13.4197998046875, 52.52624809700062],
                 [13.387527465820312, 52.53084314728766],
                 [13.366928100585938, 52.50535544522142],
                 [13.419113159179688, 52.501175722709434],
                 [13.4197998046875, 52.52624809700062]]
     )
})

polygon_feature = api.model('PolygonFeature', {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(polygon, required=True)
})

linestring = api.model('LineStringGeometry', {
    'type': fields.String(required=True, default="LineString"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True,
        type="Array",
        default=[[13.420143127441406, 52.515594085869914],
                 [13.421173095703125, 52.50535544522142],
                 [13.421173095703125, 52.49532344352079]]
     )
})

linestring_feature = api.model('LineStringFeature', {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(linestring, required=True)
})

point = api.model('PointGeometry', {
    'type': fields.String(required=True, default="Point"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True,
        type="Array",
        default=[13.421173095703125, 52.49532344352079]
     )
})

point_feature = api.model('PointFeature', {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(point, required=True)
})

pointerParser = reqparse.RequestParser()
pointerParser.add_argument('x', type=float, required=True, help='Coordinate X')
pointerParser.add_argument('y', type=float, required=True, help='Coordinate Y')
pointerParser.add_argument('epsg', type=int, required=True, help='spsg code, such as 4326')
pointerParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14], help='DGGS Resolution 1 to 14')

@api.route('/find_dggs_for_a_point')
class FindDGGSForPoint(Resource):
    @api.doc(parser=pointerParser)
    def get(self):
        args = pointerParser.parse_args()
        try:
            epsg_from = "epsg:{}".format(args['epsg'])
            epsg_to= "epsg:{}".format(4326)
            transformer = Transformer.from_crs(epsg_from, epsg_to, always_xy=True)
            latlong = transformer.transform( args['x'], args['y'])
            answer = latlong_to_DGGS(latlong, args['resolution'])
            sub_cells = []
            for cell in answer.subcells():
                sub_cells.append(str(cell))
            neighbors = []
            for k, v in answer.neighbors().items():
                neighbors.append(str(v))
            return {
                        "cell_id": str(answer),
                        "sub_cells": sub_cells,
                        "neighbors": neighbors
                    }
        except exceptions.CRSError:
            return api.abort(500, message='Please input a valid epsg code')

resolutionParser = reqparse.RequestParser()
resolutionParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14], help='DGGS Resolution 1 to 14')

@api.route('/find_dggs_for_a_line')
@api.doc(parser=resolutionParser)
class FindDGGSForALine(Resource):
    @api.expect(linestring_feature,  validate=True)
    def post(self):
        # no find dggs for a line function found at DGGS Engine
        pass

@api.route('/find_dggs_cells_within_polygon')
@api.doc(parser=resolutionParser)
class FindDGGSForALine(Resource):
    @api.expect(polygon_feature,  validate=True)
    def post(self):
        args = resolutionParser.parse_args()
        print(args)
        print(request.json)
        pass




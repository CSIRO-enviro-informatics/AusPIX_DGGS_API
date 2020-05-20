
from flask import Flask, Blueprint
from flask_restx import Namespace, Resource, reqparse, fields
from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
from pyproj import CRS, transform, exceptions
from model.geoJSON import linestring_feature
import json

api = Namespace('search', description="Search from DGGS Engine", version="0.1")

pointerParser = reqparse.RequestParser()
pointerParser.add_argument('x', type=float, required=True, help='Coordinate X')
pointerParser.add_argument('y', type=float, required=True, help='Coordinate Y')
pointerParser.add_argument('epsg', type=int, required=True, help='spsg code, such as 4326')
pointerParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14], help='DGGS Resolution 1 to 14')

@api.route('/find_dggs_for_a_point')
class FindDGGSForAPoint(Resource):
    @api.expect(pointerParser)
    def post(self):
        args = pointerParser.parse_args()
        try:
            crs_from = CRS.from_epsg(args['epsg'])
            crs_to = CRS.from_epsg('4326')
            latlong = transform(crs_from, crs_to, args['x'], args['y'])
            answer = latlong_to_DGGS(latlong, args['resolution'])
            sub_cells = []
            for cell in answer.subcells():
                sub_cells.append(str(cell))
            neighbors = []
            for k, v in answer.neighbors().items():
                neighbors.append(str(v))
            return {
                        "cellId": str(answer),
                        "sub_cells": sub_cells,
                        "neighbors": neighbors
                    }
        except exceptions.CRSError:
            return api.abort(500, message='Please input a valid epsg code')

lineParser = reqparse.RequestParser()
lineParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14], help='DGGS Resolution 1 to 14')
lineJeoJson = api.model('lineString',linestring_feature)
@api.route('/find_dggs_for_a_line')
class FindDGGSForALine(Resource):
    @api.expect([lineJeoJson])
    def post(self):
        args = lineParser.parse_args()
        try:
            crs_from = CRS.from_epsg(args['epsg'])
            crs_to = CRS.from_epsg('4326')
            latlong = transform(crs_from, crs_to, args['x'], args['y'])
            answer = latlong_to_DGGS(latlong, args['resolution'])
            sub_cells = []
            for cell in answer.subcells():
                sub_cells.append(str(cell))
            neighbors = []
            for k, v in answer.neighbors().items():
                neighbors.append(str(v))
            return {
                        "cellId": str(answer),
                        "sub_cells": sub_cells,
                        "neighbors": neighbors
                    }
        except exceptions.CRSError:
            return api.abort(500, message='Please input a valid epsg code')

from flask import Flask, Blueprint
from flask_restx import Namespace, Resource, reqparse
from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
from pyproj import Transformer, exceptions
import json

api = Namespace('search', description="Search from DGGS Engine", version="0.1")

pointerParser = reqparse.RequestParser()
pointerParser.add_argument('x', type=float, required=True, help='Coordinate X')
pointerParser.add_argument('y', type=float, required=True, help='Coordinate Y')
pointerParser.add_argument('epsg', type=int, required=True, help='spsg code, such as 4326')
pointerParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12], help='DGGS Resolution 1 to 12')

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


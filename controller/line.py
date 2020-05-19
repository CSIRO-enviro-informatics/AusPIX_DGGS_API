
from flask import Flask, Blueprint
from flask_restx import Namespace, Resource, reqparse
from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
import json

api = Namespace('line', description="Line operation on DGGS", version="0.1")

pointerParser = reqparse.RequestParser()
pointerParser.add_argument('lat', type=float, help='Latitude')
pointerParser.add_argument('long', type=float, help='Longitude')
pointerParser.add_argument('resolution', type=int, help='DGGS Resolution 1-8')

@api.route('/find_dggs_for_a_point')
@api.doc(params={})
class FindDGGSForPoint(Resource):
    @api.doc(parser=pointerParser)
    def post(self):
        args = pointerParser.parse_args()
        answer = latlong_to_DGGS((args['lat'], args['long']), args['resolution'])
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


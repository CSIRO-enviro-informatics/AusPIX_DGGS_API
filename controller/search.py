
from flask import Flask, Blueprint, request
from flask_restx import Namespace, Resource, reqparse, fields
from pyproj import Transformer, exceptions
from geojson.utils import coords
from shapely.geometry import Polygon, shape
from auspixdggs.callablemodules.point_DGGSvalue import latlong_to_DGGS
from auspixdggs.callablemodules.call_DGGS import poly_to_DGGS_tool
import json

api = Namespace('search', description="Search from DGGS Engine", version="0.1")

polygon = api.model('PolygonGeometry', {
    'type': fields.String(required=True, default="Polygon"),
    'coordinates': fields.List(
        fields.List(
            fields.List(fields.Float, required=True, type="Array"),
            required=True, type="Array"
     ))
})

linestring = api.model('LineStringGeometry', {
    'type': fields.String(required=True, default="LineString"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True,
        type="Array"
     )
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
            meta = {
                "point": (args['x'], args['y']),
                "epsg": args['epsg']
            }
            return {
                        "meta": meta,
                        "dggs_cell_id": str(answer),
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
    @api.expect(linestring,  validate=True)
    def post(self):
        # no find dggs for a line function found at DGGS Engine
        pass

def bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     ret = [ box[0][0], box[1][0], box[0][1], box[1][1] ]
     return ret
@api.route('/find_dggs_cells_within_polygon')
@api.doc(parser=resolutionParser)
class FindDGGSForALine(Resource):
    @api.expect(polygon,  validate=True)
    def post(self):
        args = resolutionParser.parse_args()
        polygon = shape(request.json)
        polygon.bbox = bbox(list(coords(request.json)))
        polygon.points = request.json['coordinates'][0]
        cells = poly_to_DGGS_tool(polygon, '', args.resolution) 
        meta = {
            "count": len(cells),
            "polygon": request.json
        }
        return {
            "meta": meta,
            "dggs_cells": cells
        }




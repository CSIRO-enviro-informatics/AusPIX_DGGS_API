
from flask import Flask, Blueprint, request
from flask_restx import Namespace, Resource, reqparse, fields
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon
from pyproj import Transformer, exceptions
from geojson.utils import coords
from geojson import Feature, FeatureCollection
from shapely.geometry import Polygon, shape
from auspixdggs.callablemodules import dggs_for_points_geojson_callable
from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly, get_dggs_cell_bbox
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
import json
import geojson

rdggs = RHEALPixDGGS()

api = Namespace('search', description="Search from DGGS Engine", version="0.1")
resolutionParser = reqparse.RequestParser()
resolutionParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], help='DGGS Resolution 1 to 14')
resolutionParser.add_argument('dggs_as_polygon', type=bool, choices=[True, False], default=False, help='Return geojson with DGGS cells as polygon features when set True (default False), return original geojson object when set False')
resolutionParser.add_argument('geojson', type=dict, location='json')

def bbox(coord_list):
     box = []
     for i in (0,1):
         res = sorted(coord_list, key=lambda x:x[i])
         box.append((res[0][i],res[-1][i]))
     ret = [ box[0][0], box[1][0], box[0][1], box[1][1] ]
     return ret

def geojson_to_shape(g):
    return shape(g)

def get_cells_in_feature(fea, resolution, return_cell_obj=False):
    geom = geojson_to_shape(fea['geometry'])
    curr_coords = list(coords(fea))
    thisbbox = bbox(curr_coords)
    cells = []
    if isinstance(geom, LineString) or isinstance(geom, MultiLineString): 
        res_cells = line_to_DGGS(curr_coords, resolution)
        if return_cell_obj:
            cells = res_cells
        else:
            for cell in res_cells:
                if str(cell) not in cells:
                    cells.append(str(cell))
    elif isinstance(geom, Polygon) or  isinstance(geom, MultiPolygon):
        res_cells = cells_in_poly(thisbbox, curr_coords, resolution, return_cell_obj)  
        cells = [item[0] for item in res_cells]
    else: 
        cells = cells_in_poly(thisbbox, curr_coords, resolution, return_cell_obj) 
        cells = [item[0] for item in res_cells]
    return cells

def get_cells_in_geojson(geojson, resolution, return_cell_obj=False):
    list_cells = []
    for fea in geojson['features']:  # for feature in attribute table
        res_cells = get_cells_in_feature(fea, resolution, return_cell_obj)
        list_cells = list(list_cells + res_cells)
    return list_cells 
@api.route('/find_dggs_by_geojson')
@api.doc(parser=resolutionParser)
class FindDGGSByGeojson(Resource):
    def post(self):
        args = resolutionParser.parse_args()
        geojson_obj = geojson.loads(json.dumps(request.json))
        if not hasattr(geojson_obj, 'is_valid'):
            return {
                "error": "geojson is invalid."
            }
        if not geojson_obj.is_valid:
            return {
                "error": "geojson is invalid.",
                "detail": geojson_obj.errors()
            }
        print(args.dggs_as_polygon, args.dggs_as_polygon==True)
        if args.dggs_as_polygon == False:
            cells = get_cells_in_geojson(geojson_obj, args.resolution, False)
            meta = {
                "cells_count": len(cells)
            }
            return {
                "meta": meta,
                "dggs_cells": cells,
                # "payload": geojson_obj
            }
        else:
            cells = get_cells_in_geojson(geojson_obj, args.resolution, True)
            list_features = []
            for cell in cells:
                bbox_coords = get_dggs_cell_bbox(cell)
                geom_obj = Polygon(bbox_coords)
                feat = Feature(geometry=geom_obj, properties={"dggs_cell_id": str(cell)}) 
                list_features.append(feat)

            feature_collection = FeatureCollection(list_features)
            return feature_collection
     



pointerParser = reqparse.RequestParser()
pointerParser.add_argument('x', type=float, required=True, help='Coordinate X')
pointerParser.add_argument('y', type=float, required=True, help='Coordinate Y')
pointerParser.add_argument('epsg', type=int, required=True, help='spsg code, such as 4326')
pointerParser.add_argument('resolution', type=int, required=True, choices=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16], help='DGGS Resolution 1 to 14')

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
            answer = rdggs.cell_from_point(args['resolution'], latlong)
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

# linestring = api.model('LineStringGeometry', {
#     'type': fields.String(required=True, default="LineString"),
#     'coordinates': fields.List(
#         fields.List(fields.Float, required=True, type="Array"),
#         required=True,
#         type="Array",
#         default=[[13.420143127441406, 52.515594085869914],
#                  [13.421173095703125, 52.50535544522142],
#                  [13.421173095703125, 52.49532344352079]]
#      )
# })
# @api.route('/find_dggs_for_a_line')
# @api.doc(parser=resolutionParser)
# class FindDGGSForALine(Resource):
#     @api.expect(linestring,  validate=True)
#     def post(self):
#         # no find dggs for a line function found at DGGS Engine
#         pass

# @api.route('/find_dggs_cells_within_polygon')
# @api.doc(parser=resolutionParser)
# class FindDGGSForALine(Resource):
#     @api.expect(feature_model,  validate=True)
#     def post(self):
#         args = resolutionParser.parse_args()
#         polygon = shape(request.json)
#         polygon.bbox = bbox(list(coords(request.json)))
#         polygon.points = request.json['coordinates'][0]
#         cells = poly_to_DGGS_tool(polygon, '', args.resolution) 
#         meta = {
#             "count": len(cells),
#             "polygon": request.json
#         }
#         return {
#             "meta": meta,
#             "dggs_cells": cells
#         }




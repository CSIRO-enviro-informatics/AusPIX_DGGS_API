
from flask import Flask, Blueprint, request
from flask_restx import Namespace, Resource, reqparse, fields
from shapely.geometry import shape, LineString, MultiLineString, Polygon, MultiPolygon,  Point, MultiPoint
from geojson.utils import coords
from geojson import Feature, FeatureCollection
from shapely.geometry import Polygon, shape
from auspixdggs.callablemodules.dggs_in_poly_for_geojson_callable import cells_in_poly, get_dggs_cell_bbox
from auspixdggs.callablemodules.dggs_for_points_geojson_callable import latlong_to_DGGS
from auspixdggs.callablemodules.dggs_in_line import line_to_DGGS, densify_my_line
from auspixdggs.auspixengine.dggs import RHEALPixDGGS
from auspixdggs.callablemodules.util import transform_coordinates
from auspixdggs.callablemodules.util import rdggs
import json
import geojson
import copy

api = Namespace('search', description="Search from DGGS Engine", version="0.1")
find_dggs_by_geojson_parser = reqparse.RequestParser()
find_dggs_by_geojson_parser.add_argument('resolution', type=int, required=True, choices=[4,5,6,7,8,9,10,11,12], help='DGGS Resolution 4 to 12')
find_dggs_by_geojson_parser.add_argument('dggs_as_polygon', type=str, choices=['False', 'True'], default="True", help='Return geojson with DGGS cells as polygon features when set True (default True), return original geojson object when set False')
find_dggs_by_geojson_parser.add_argument('keep_properties', type=str, choices=['False', 'True'], default="True", help='Keep the geojson features\' properties at the returned geojson when set True (default True)')
find_dggs_by_geojson_parser.add_argument('geojson', type=dict, location='json')

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
    cells = []
    if isinstance(geom, Point) or isinstance(geom, MultiPoint): 
        # return cell object for Point or multiPoint
        curr_coords = list(coords(fea))
        for coord in curr_coords:
            cells.append(latlong_to_DGGS(coord, resolution))
    elif isinstance(geom, LineString) or isinstance(geom, MultiLineString): 
        # return cell object for line
        fea['geometry']['coordinates'] = densify_my_line(fea['geometry']['coordinates'], resolution)
        curr_coords = list(coords(fea))
        cells = line_to_DGGS(curr_coords, resolution)
    elif isinstance(geom, Polygon):
        curr_coords = list(coords(fea))
        thisbbox = bbox(curr_coords)
        res_cells = cells_in_poly(thisbbox, [fea['geometry']['coordinates']], resolution, return_cell_obj)  
        cells = [item[0] for item in res_cells]
    elif isinstance(geom, MultiPolygon):
        # return cell string
        curr_coords = list(coords(fea))
        thisbbox = bbox(curr_coords)
        res_cells = cells_in_poly(thisbbox, fea['geometry']['coordinates'], resolution, return_cell_obj)  
        cells = [item[0] for item in res_cells]

    return cells

def get_cells_in_geojson(geojson, resolution, return_cell_obj=False):
    list_cells = []
    for fea in geojson['features']:  # for feature in attribute table
        res_cells = get_cells_in_feature(fea, resolution, return_cell_obj)
        list_cells = list(list_cells + res_cells)
    return list_cells
def get_cells_with_property_in_geojson(geojson, resolution, return_cell_obj=False):
    list_cells = []
    list_property = []
    for fea in geojson['features']:  # for feature in attribute table
        res_cells = get_cells_in_feature(fea, resolution, return_cell_obj)
        list_cells.append(res_cells)
        list_property.append(fea['properties'])
    # print(list_cells)
    return list_cells, list_property
def reduce_duplicate_cells_2d_array(cells):
    # input 2-d array of cells
    # return original cells (str or object)
    unique_cells = []
    unique_cells_str = []
    for cell_array in cells:
        # 1-d array
        for cell in cell_array:
            cell_id = str(cell)
            if cell_id not in unique_cells_str:
                unique_cells_str.append(cell_id)
                unique_cells.append(cell)
    return unique_cells
def reduce_duplicate_cells_properties(cells, properties):
    # return original cells (str or object)
    unique_cells = []
    unique_cells_str = []
    unique_properties = []
    for i, cell_array in enumerate(cells):
        for cell in cell_array:
            cell_id = str(cell)
            if cell_id not in unique_cells_str:
                unique_cells_str.append(cell_id)
                unique_properties.append(properties[i])
                unique_cells.append(cell)
    return unique_cells, unique_properties
@api.route('/find_dggs_by_geojson')
@api.doc(parser=find_dggs_by_geojson_parser)
class FindDGGSByGeojson(Resource):
    def post(self):
        args = find_dggs_by_geojson_parser.parse_args()
        dggs_as_polygon = "True"
        keep_properties = "True"
        if args['keep_properties']:
            keep_properties = args.keep_properties
        if args['dggs_as_polygon']:
            dggs_as_polygon = args.dggs_as_polygon
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
        if args.dggs_as_polygon == 'False':
            cells, list_properties = get_cells_with_property_in_geojson(geojson_obj, args.resolution, False)
            cells = reduce_duplicate_cells_2d_array(cells)
            meta = {
                "cells_count": len(cells)
            }
            return {
                "meta": meta,
                "dggs_cells": [str(cell) for cell in cells],
                # "payload": geojson_obj
            }
        else:
            list_cells, list_properties = get_cells_with_property_in_geojson(geojson_obj, args.resolution, True)
            list_cells, list_properties = reduce_duplicate_cells_properties(list_cells, list_properties)
            list_features = []
            for i, cell in enumerate(list_cells):
                bbox_coords = get_dggs_cell_bbox(cell)
                print(i, str(cell))
                geom_obj = Polygon(bbox_coords)
                if keep_properties == 'True':
                    properties = {}
                    properties['dggs_cell_id'] = str(cell)
                    for key in list_properties[i]:
                        properties[key] = list_properties[i][key]
                else:
                    properties = {}
                    properties['dggs_cell_id'] = str(cell)
                feat = Feature(geometry=geom_obj, properties=copy.deepcopy(properties)) 
                list_features.append(feat)

            feature_collection = FeatureCollection(list_features)
            geojson_obj['features'] = feature_collection['features']
            return geojson_obj
     
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
        answer = latlong_to_DGGS([args['x'], args['y']], args['resolution'], args['epsg'])
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

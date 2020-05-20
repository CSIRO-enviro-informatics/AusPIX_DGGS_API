from flask_restx import fields

bounding_box = {
    'x_lat': fields.Float(),
    'y_lat': fields.Float(),
    'x_lng': fields.Float(),
    'y_lng': fields.Float(),
}

polygon = {
    'type': fields.String(required=True, default="Polygon"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True, type="Array",
        default=[[
              149.02301788330078,
              -35.40472227957223
            ],
            [
              149.21424865722653,
              -35.40472227957223
            ],
            [
              149.21424865722653,
              -35.17633399264036
            ],
            [
              149.02301788330078,
              -35.17633399264036
            ],
            [
              149.02301788330078,
              -35.40472227957223
            ]]
     )
}

polygon_feature = {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(polygon, required=True)
}

line_string = {
    'type': fields.String(required=True, default="LineString"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True,
        type="Array",
        default=[[
            149.15639877319336,
            -35.18447174381222
          ],
          [
            149.12172317504883,
            -35.27813743630096
          ]]
     )
}

linestring_feature = {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(line_string, required=True)
}

point = {
    'type': fields.String(required=True, default="Point"),
    'coordinates': fields.List(
        fields.List(fields.Float, required=True, type="Array"),
        required=True,
        type="Array",
        default=[149.15639877319336,-35.18447174381222]
     )
}

point_feature = {
    'type': fields.String(default="Feature", require=True),
    'geometry': fields.Nested(point, required=True)
}
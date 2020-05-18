import logging
import _config as conf
from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
# from auspixdggs import dggs_engine_api


app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(blueprint,  doc="/doc/", version='0.1', title="DGGS Engine", description="")
app.register_blueprint(blueprint)


@api.route('/find_dggs_for_a_point')
@api.doc(params={})
class FindDGGSForPoint(Resource):
    pointWithResolution = api.model('point', {
        'lat': fields.Float,
        'long': fields.Float,
        'resolution': fields.Integer
    })
    def get(self):
        return {}
    @api.expect(pointWithResolution)
    def post(self):
        print('find_dggs_for_a_point')
        # answer = point_DGGSvalue.latlong_to_DGGS((148.9668333, -35.38275), 12)
        return {}



# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    app.run(host="0.0.0.0", port=int("3000"), debug=conf.DEBUG)
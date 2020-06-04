import logging
import _config as conf
from flask import Flask, Blueprint
from flask_restx import Api
from flask_cors import CORS
from werkzeug.middleware.proxy_fix import ProxyFix
from controller.search import api as search_api

app = Flask(__name__, template_folder=conf.TEMPLATES_DIR, static_folder=conf.STATIC_DIR)
CORS(app)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_host=1)
blueprint = Blueprint('api', __name__, url_prefix="/api")
api = Api(blueprint,  doc="/doc/", version='0.1', title="DGGS Engine", description="")
api.add_namespace(search_api)
app.register_blueprint(blueprint)


@app.route('/')
def root():
    return app.send_static_file('index.html')

@app.route('/testmap/')
def testmap():
    return app.send_static_file('testmap.html')


# run the Flask app
if __name__ == '__main__':
    logging.basicConfig(filename=conf.LOGFILE,
                        level=logging.DEBUG,
                        datefmt='%Y-%m-%d %H:%M:%S',
                        format='%(asctime)s %(levelname)s %(filename)s:%(lineno)s %(message)s')

    app.run(host="0.0.0.0", port=int("3000"), debug=conf.DEBUG)

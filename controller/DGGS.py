"""
This file contains all the HTTP routes for classes used in this service
"""
from flask import Blueprint, request, Response
# import _config as config
import requests

import json
import os

import pprint

DGGS = Blueprint('DGGS', __name__)


@DGGS.route('/dggs/find_dggs_for_a_point')
def find_dggs_for_a_point():
    print('find_dggs_for_a_point')
    return {}


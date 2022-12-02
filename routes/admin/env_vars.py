# [START imports]
from flask import Blueprint
import logging
from utils.debug_functions import *
from flask import Response
import os
# [END imports]


# [START /admin/<password>/env-vars route definition]
env_vars_bp = Blueprint('env_vars', __name__)

@env_vars_bp.route("/admin/<password>/env-vars", methods=["GET"])
def print_env_vars_to_user(password):
    if password == 'adminpass':
        logging.info(f'Scraper received a /admin/<password>/env-vars request from {get_client_request_ip_address()}.')

        d = dict()
        for key, val in os.environ.items():
            d[key] = val

        # Get UTC millisecond timestamp and format response
        ts = str(get_current_timestamp_millis_utc())
        response = f"{{'returnStatus': 'success', 'statusCode': 200, 'timestampMillisUTC': {ts}, 'message': {d}}}"


        return Response(
                    response=response,
                    status=200,
                    mimetype='application/json'
                    )

    else:
        ts = str(get_current_timestamp_millis_utc())
        fail_response = f"{{'returnStatus': 'fail', 'statusCode': 401, 'timestampMillisUTC': {ts}, 'message': 'unauthorized'}}"


        return Response(
                    response=fail_response,
                    status=401,
                    mimetype='application/json'
                    )
# [END /admin/<password>/env-vars route definition]

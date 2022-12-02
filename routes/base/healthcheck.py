# [START imports]
from flask import Blueprint
import logging
from utils.debug_functions import *
from flask import Response
# [END imports]


# [START /healthcheck route definition]
healthcheck_bp = Blueprint('healthcheck', __name__)

@healthcheck_bp.route("/healthcheck", methods=["GET"])
def health_check():

    logging.info(f'Scraper received a /healthcheck request from {get_client_request_ip_address()}. Health checking...')

    # Get UTC millisecond timestamp and format response
    ts = str(get_current_timestamp_millis_utc())
    response = f"{{'returnStatus': 'success', 'statusCode': 200, 'timestampMillisUTC': {ts}, 'message': 'alive'}}"


    return Response(
                response=response,
                status=200,
                mimetype='application/json'
                )
# [END /healthcheck route definition]

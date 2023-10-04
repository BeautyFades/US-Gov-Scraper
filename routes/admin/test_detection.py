# [START imports]
from flask import Blueprint, send_file
from time import sleep
import logging
from utils.debug_functions import *
from flask import Response
import os
# [END imports]


# [START /admin/<password>/test-detection route definition]
test_detection_bp = Blueprint('test_detection', __name__)

@test_detection_bp.route("/admin/<password>/test-detection", methods=["GET"])
def test_detectability(password):
    if password == 'adminpass':
        logging.info(f'Scraper received a /admin/<password>/test-detection request from {get_client_request_ip_address()}.')

    # Initialize Chrome and wait for it to load up
        driver = initilize_chrome()

        driver.get('https://nowsecure.nl/')
        sleep(5)
        driver.save_screenshot('test.png')
        return send_file('test.png')

    else:
        ts = str(get_current_timestamp_millis_utc())
        fail_response = f"{{'returnStatus': 'fail', 'statusCode': 401, 'timestampMillisUTC': {ts}, 'message': 'unauthorized'}}"


        return Response(
                    response=fail_response,
                    status=401,
                    mimetype='application/json'
                    )
# [END /admin/<password>/test-detection route definition]

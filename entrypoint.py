# [START imports]
from flask import Flask
from utils.logger import ScraperLogger
from routes.base.healthcheck import healthcheck_bp
from routes.api.v1.run_scraper import run_scraper_bp
from routes.admin.env_vars import env_vars_bp
from routes.admin.test_detection import test_detection_bp
import logging
# [END imports]


# [START flask and logging initialization]
app = Flask('app')
log = ScraperLogger()
logging.info('Lord forgive me for what I am about to code')
# [END flask and logging initialization]


# [START route blueprint registering]
app.register_blueprint(healthcheck_bp)
app.register_blueprint(run_scraper_bp)
app.register_blueprint(env_vars_bp)
app.register_blueprint(test_detection_bp)
# [END route blueprint registering]


# [START main trap]
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# [END main trap]

# [START imports]
from flask import Flask
from utils.logger import ScraperLogger
from routes.healthcheck import healthcheck
from routes.run_scraper import run_scraper
import logging
# [END imports]


# [START flask and logging initialization]
app = Flask('app')
log = ScraperLogger()
logging.info('Lord forgive me for what I am about to code')
# [END flask and logging initialization]


# [START route blueprint registering]
app.register_blueprint(healthcheck)
app.register_blueprint(run_scraper)
# [END route blueprint registering]


# [START main trap]
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
# [END main trap]

import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import Flask, Response, send_file
import config as config
from utils.logger import ScraperLogger
import logging
from utils.debug_functions import *
from time import sleep


app = Flask('app')
l = ScraperLogger()


logging.info('Lord forgive me for what I am about to code')


#chrome_options = uc.ChromeOptions()
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--disable-setuid-sandbox')
driver = uc.Chrome(version_main=106)

@app.route("/healthcheck", methods=["GET"])
def health_check():

    logging.info(f'Scraper received a /healthcheck request from {get_client_request_ip_address()}. Health checking...')
    ts = str(get_current_timestamp_millis_utc())
    response = "[{'returnStatus': 'success'}, {'statusCode': '200'}, {'timestampMillisUTC': '" + ts + "'}, {'message': 'alive'}]"

    return Response(
                response=response,
                status=200,
                mimetype='application/json'
                )



@app.route("/api/v1/scrape", methods=["GET"])
def scrape():

    logging.info(f'Scraper received a / request from {get_client_request_ip_address()}.')
 
    driver.get('https://www.congress.gov/members')

    elem = driver.find_element(By.XPATH, '//ol[@class="basic-search-results-lists expanded-view"]')

    all_li = elem.find_elements(By.XPATH, './/li[@class="expanded"]')

    namelist = []
    for li in all_li:
        name = li.find_element(By.XPATH, './/span/a')
        namelist.append(name.text)

    print(namelist)
    str1 = '\n'.join(str(e) for e in namelist)
    driver.quit()
    return str1


@app.route("/api/v1/google", methods=["GET"])
def google():

    logging.info(f'Scraper received a /api/v1/google request from {get_client_request_ip_address()}.')

    driver.get("https://google.com")

    html_source = driver.page_source
    print(html_source)
    driver.quit()

    return html_source


@app.route("/api/v1/test-detection", methods=["GET"])
def test_detection():

    logging.info(f'Scraper received a /api/v1/test-detection request from {get_client_request_ip_address()}.')

    driver.get('https://nowsecure.nl')

    #wait_for_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/main/h1")))
    sleep(50)
    driver.save_screenshot('detectionResult.png')
    driver.quit()

    return send_file('detectionResult.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
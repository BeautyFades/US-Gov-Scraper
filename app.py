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
import pandas as pd


app = Flask('app')
l = ScraperLogger()


logging.info('Lord forgive me for what I am about to code')


chrome_options = uc.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-setuid-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument(
    "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
)
driver = uc.Chrome(version_main=106, options=chrome_options)

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
 
    driver.get('https://www.congress.gov/members?pageSize=250')

    elem = driver.find_element(By.XPATH, '//ol[@class="basic-search-results-lists expanded-view"]')

    webelements_all_li = elem.find_elements(By.XPATH, './/li[@class="expanded"]')

    namelist = []
    job_titles = []
    for li in webelements_all_li:
        name = li.find_element(By.XPATH, './/span/a')
        names = name.text.split(' - ')
        namelist.append(names[0])
        job_titles.append(names[1])

    print(namelist)
    print(job_titles)

    rows = zip(namelist, job_titles)

    df = pd.DataFrame(rows, columns=['name', 'job_title'])
    df.to_csv('pd.csv')

    return Response(
        df.to_csv(),
        mimetype="text/csv",
        headers={"Content-disposition":
        "attachment; filename=export.csv"}
        )


@app.route("/api/v1/google", methods=["GET"])
def google():

    logging.info(f'Scraper received a /api/v1/google request from {get_client_request_ip_address()}.')

    driver.get("https://google.com")

    html_source = driver.page_source
    print(html_source)

    return html_source


@app.route("/api/v1/test-detection", methods=["GET"])
def test_detection():

    logging.info(f'Scraper received a /api/v1/test-detection request from {get_client_request_ip_address()}.')

    driver.get('https://nowsecure.nl')

    wait_for_element = WebDriverWait(driver, 60).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/main/h1")))
    driver.save_screenshot('detectionResult.png')

    return send_file('detectionResult.png', mimetype='image/png')


@app.route("/api/v1/test-session", methods=["GET"])
def test_session():

    logging.info(f'Scraper received a /api/v1/test-session request from {get_client_request_ip_address()}.')

    driver.get('https://infosimples.github.io/detect-headless/')

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    sleep(2)
    driver.switch_to.alert.accept()
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/table")))
    driver.save_screenshot('detectionResult.png')

    return send_file('detectionResult.png', mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
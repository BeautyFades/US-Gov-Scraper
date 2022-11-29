import os
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from flask import Flask, request, Response, jsonify
import config as config
from datetime import datetime
from utils.logger import ScraperLogger
import logging

app = Flask('app')
l = ScraperLogger()

print('LORD FORGIVE ME FOR WHAT I AM ABOUT TO CODE')

def get_client_ip_address():
    return request.remote_addr


@app.route("/healthcheck", methods=["GET"])
def health_check():
    logging.info(f'Scraper received a /healthcheck request from {get_client_ip_address()}. Health checking...')
    response = "{'returnStatus': 'success'}, {'statusCode': '200'}, {'message': 'alive'}"

    print(response)

    return Response(
                response=response,
                status=200,
                mimetype='application/json'
                )



@app.route("/", methods=["GET"])
def scrape():
    logging.info(f'Scraper received a / request from {get_client_ip_address()}.')

    browser = uc.Chrome(version_main=106, use_subprocess=True)
    browser.get('https://www.congress.gov/members')

    elem = browser.find_element(By.XPATH, '//ol[@class="basic-search-results-lists expanded-view"]')

    all_li = elem.find_elements(By.XPATH, './/li[@class="expanded"]')

    namelist = []
    for li in all_li:
        name = li.find_element(By.XPATH, './/span/a')
        namelist.append(name.text)

    print(namelist)
    str1 = '\n'.join(str(e) for e in namelist)
    return str1


@app.route("/google", methods=["GET"])
def google():
    logging.info(f'Scraper received a /google request from {get_client_ip_address()}.')

    browser = uc.Chrome(version_main=106, use_subprocess=True)
    browser.get("https://google.com")

    html_source = browser.page_source
    print(html_source)

    return html_source

if __name__ == '__main__':
    print('MAINTRAP')
    app.run(host='0.0.0.0', port=8000)
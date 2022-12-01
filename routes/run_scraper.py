# [START imports]
from selenium.webdriver.common.by import By
from flask import send_file, Blueprint
import config as config
import logging
from utils.debug_functions import *
import pandas as pd
import undetected_chromedriver as uc
from time import sleep
# [END imports]


# [START /api/v1/scrape route definition]
run_scraper = Blueprint('run_scraper', __name__)


@run_scraper.route("/api/v1/scrape", methods=["GET"])
def scrape():

    logging.info(f'Scraper received a / request from {get_client_request_ip_address()}.')

    # Initialize Chrome and wait for it to load up
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument(
        "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"
    )
    driver = uc.Chrome(version_main=106, options=chrome_options)
    sleep(2)


    # Go to Congress website and scrape based on XPATH
    driver.get('https://www.congress.gov/members?pageSize=250')
    elem = driver.find_element(By.XPATH, '//ol[@class="basic-search-results-lists expanded-view"]')
    webelements_all_li = elem.find_elements(By.XPATH, './/li[@class="expanded"]')

    # Format a names list and a job title list from extracted WebElement
    name_list = []
    job_titles_list = []
    for li in webelements_all_li:
        name_and_job = li.find_element(By.XPATH, './/span/a')
        names = name_and_job.text.split(' - ')
        name_list.append(names[0])
        job_titles_list.append(names[1])

    # Create .csv file
    rows = zip(name_list, job_titles_list)
    df = pd.DataFrame(rows, columns=['name', 'job_title'])
    df.to_csv('local_files/congress_members.csv')


    # Return a download to user's browser
    return send_file(
        'local_files/congress_members.csv',
        mimetype='text/csv',
        download_name='congress_members.csv',
        as_attachment=True
    )
# [END /api/v1/scrape route definition]

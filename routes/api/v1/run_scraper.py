# [START imports]
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from flask import send_file, Blueprint
import config as config
import logging
from utils.debug_functions import *
import pandas as pd
# [END imports]

# [START /api/v1/scrape route definition]
run_scraper_bp = Blueprint('run_scraper', __name__)

@run_scraper_bp.route("/api/v1/scrape", methods=["GET"])
def scrape():
    logging.info(f'Scraper received a / request from {get_client_request_ip_address()}.')

    driver = initilize_chrome()

    # Go to Congress website and scrape based on XPATH
    driver.get('https://www.congress.gov/members?pageSize=250')
    wait = WebDriverWait(driver, 5)  # Adjust the timeout as needed
    elem = wait.until(EC.presence_of_element_located((By.XPATH, '//ol[@class="basic-search-results-lists expanded-view"]')))
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

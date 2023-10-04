from flask import request
from datetime import datetime, timezone
from selenium import webdriver

def get_client_request_ip_address() -> str:
    return request.remote_addr

def get_current_timestamp_millis_utc() -> int:
    return int(datetime.now(timezone.utc).timestamp() * 1000)

def initilize_chrome() -> webdriver.Chrome:
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36")

    driver = webdriver.Chrome(options=chrome_options)
    driver.implicitly_wait(5)
    
    return driver

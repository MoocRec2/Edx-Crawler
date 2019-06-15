import time
from selenium import webdriver
import requests
from local_storage import LocalStorage

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('C:/chromedriver')

# Sign in Page
driver.get('https://courses.edx.org/login')
email_input = driver.find_element_by_name("email")
password_input = driver.find_element_by_name("password")

email_input.send_keys("smrbasil4@gmail.com")
password_input.send_keys("nvidia1024")

login_button = driver.find_element_by_class_name('login-button')
login_button.click()

cookies = driver.get_cookies()
driver.quit()

cookies_dict = {}
for cookie in cookies:
    cookies_dict[cookie.get('name')] = cookie.get('value')

subjects_url = 'https://www.edx.org/api/v1/catalog/subjects'

r = requests.get(subjects_url, cookies=cookies_dict)

response_data = r.json()

for subject in response_data['results']:
    print(subject['name'])

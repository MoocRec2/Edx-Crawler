import time
from selenium import webdriver
import requests
from local_storage import LocalStorage

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('C:/chromedriver')

# Sign in
driver.get('https://courses.edx.org/login')
email_input = driver.find_element_by_name("email")
password_input = driver.find_element_by_name("password")
email_input.send_keys("smrbasil4@gmail.com")
password_input.send_keys("nvidia1024")
login_button = driver.find_element_by_class_name('login-button')
login_button.click()

# Get Cookies
cookies = driver.get_cookies()
cookies_dict = {}
for cookie in cookies:
    cookies_dict[cookie.get('name')] = cookie.get('value')
driver.quit()

# Start
courses_url = 'https://www.edx.org/api/v1/catalog/search?selected_facets[]=subjects_exact:Computer Science'

next_url = courses_url
count = 1

while True:
    print('Iteration =', count)
    r = requests.get(next_url, cookies=cookies_dict)
    response_data = r.json()
    courses = response_data['objects']['results']
    for course in courses:
        print(course['title'])
    next_url = response_data['objects']['next']
    count += 1

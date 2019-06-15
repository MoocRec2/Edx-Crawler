import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import json
from json import JSONDecodeError
from db_connector import Thread

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

# Get Discussion URL from Course URL
course_url = 'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/'
course_url_components = course_url.split('/')
course_url_components.reverse()
index = 0
for url_component in course_url_components:
    if url_component == 'course':
        course_url_components[index] = 'discussion'
        for x in range(index):
            course_url_components.pop(x)
        break
    index += 1
course_url_components.reverse()
course_url_components.append('forum/?ajax=1&page=1&sort_key=comments&sort_order=desc')
discussion_url = '/'.join(course_url_components)

print('Discussion URL =', discussion_url)

refresh_delay = 1


def check_page_load(by, delay, element_id):
    count = 0
    while count < 10:
        try:
            my_elem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, element_id)))
            print(element_id, "Page is ready!")
            break
        except TimeoutException:
            print(element_id, 'Page is not yet ready, checking again...')
        count += 1


check_page_load(By.ID, refresh_delay, 'my-courses')

driver.get(discussion_url)

all_discussions_option = driver.find_element_by_id('all_discussions')
all_discussions_option = all_discussions_option.find_element_by_class_name('forum-nav-browse-title')
all_discussions_option.click()

check_page_load(By.CLASS_NAME, 1, 'forum-nav-thread')

for request in driver.requests:
    if request.response:
        try:
            if request.path == discussion_url:
                body = request.response.body.decode()
                json_data = json.loads(body)
                break
        except JSONDecodeError:
            pass
        except:
            print('Unhandled Exception')

print(json_data)
threads = json_data['discussion_data']

results = Thread.upsert_threads(threads)
print('Results =', results)

driver.requests.clear()

load_more_btn = driver.find_element_by_class_name('forum-nav-load-more-link')
load_more_btn.click()

time.sleep(10)
driver.quit()

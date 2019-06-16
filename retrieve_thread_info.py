import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
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
# course_url = 'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/'
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
thread_list = []

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

threads = json_data['discussion_data']
results = Thread.upsert_threads(threads)
if results:
    print('All Basic Thread Information has been saved to the database')
thread_list.extend(threads)

num_of_pages = json_data['num_pages']
current_page = json_data['page']

while current_page != num_of_pages:
    del driver.requests

    forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
    threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
    thread_count = threads.__len__()

    while True:
        try:
            load_more_btn = driver.find_element_by_class_name('forum-nav-load-more-link')
            load_more_btn.click()
            break
        except ElementClickInterceptedException:
            time.sleep(0.5)
            pass

    # count = 0
    while True:
        forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
        threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
        new_thread_count = threads.__len__()
        if new_thread_count != thread_count:
            break
        print('Threads not yet loaded, trying again...')
        time.sleep(1)

    for request in driver.requests:
        try:
            if 'application/json' in request.response.headers['Content-Type']:
                print(request.path, request.response.headers['Content-Type'])
                response_body = request.response.body.decode()
                break
        except:
            pass

    try:
        json_data = json.loads(response_body)
        print('JSON Data =', json_data)
        threads = json_data['discussion_data']
        Thread.upsert_threads(threads)
        thread_list.extend(threads)
    except JSONDecodeError:
        pass

    current_page = json_data['page']

print('All Threads Have Been Loaded to the UI')

forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
thread_elems = forum_thread_list.find_elements_by_class_name('forum-nav-thread')

# Iterating through the Elements
new_thread_info = []
print('Thread Element Count =', thread_elems.__len__())
print('Thread List Count =', thread_list.__len__())
for thread_elem in thread_elems:
    thread_title = thread_elem.find_element_by_class_name('forum-nav-thread-title').text

    for thread in thread_list:
        if thread_title == thread['title']:
            found_thread = thread
            break

    if found_thread['comments_count'] == 0:
        break

    del driver.requests
    thread_elem.click()

    while True:
        try:
            post_title_elem = driver.find_element_by_class_name('forum-response')
            break
        except:
            pass
        time.sleep(1)

    # Loop through the requests
    for request in driver.requests:
        try:
            if 'application/json' in request.response.headers['Content-Type']:
                json_data = json.loads(request.response.body.decode())
                new_thread_info.append(json_data['content'])
                break
        except:
            print('Exception Occurred, parsing as JSON')

print('Thread Information Collected, count=', new_thread_info.__len__())
Thread.upsert_threads(new_thread_info)

time.sleep(10)
driver.quit()

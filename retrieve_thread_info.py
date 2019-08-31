import time
from seleniumwire import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import selenium
import json
from json import JSONDecodeError
from db_connector import Thread
from pprint import pprint
from selenium.webdriver.chrome.options import Options


def retrieve_thread_info(course_url, driver):
    print('-----Retrieving Thread Information-----')
    print('Course URL:', course_url)

    # Authentication
    # If driver is not None, it means that authentication has already been performed
    # if driver is None:
    if driver is not None:
        driver.quit()
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome('C:/chromedriver', options=options)

    # Sign in
    print('Authenticating')
    driver.get('https://courses.edx.org/login')
    email_input = driver.find_element_by_name("email")
    password_input = driver.find_element_by_name("password")
    email_input.send_keys("smrbasil4@gmail.com")
    password_input.send_keys("nvidia1024")
    login_button = driver.find_element_by_class_name('login-button')
    login_button.click()
    driver.maximize_window()
    print('Successfully Authenticated')

    # Get Cookies
    cookies = driver.get_cookies()
    cookies_dict = {}
    for cookie in cookies:
        cookies_dict[cookie.get('name')] = cookie.get('value')
    # else:
    #     for cookie in previous_cookies:
    #         driver.add_cookie(cookie)

    # Derive Discussion URL from Course URL
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

    ''' Checks whether a page has loaded based on a specific element of the page '''

    def check_page_load(by, delay, element_id):
        print('Checking for element, parameters:', by, delay, element_id)
        count = 0
        while count < 10:
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, element_id)))
                print('Element Found')
                return True
            except TimeoutException:
                pass
            count += 1
        return False

    refresh_delay = 1
    elem_check_result = check_page_load(By.ID, refresh_delay, 'my-courses')
    if not elem_check_result:
        print('Element Not Found')
        return driver
    driver.get(discussion_url)
    print('Discussion URL:', discussion_url)

    do_discussions_exist = False

    '''
    Extracting Forum Threads
    While Loop - Loading Threads Categories to UI
    Categories include General Discussions and Chapters
    '''
    discussion_set = 0
    while not do_discussions_exist:
        discussion_set += 1

        # Checking whether discussions exist
        print('Checking whether discussions exist')
        try:
            all_discussions_option = driver.find_element_by_id('all_discussions')
            print('Discussion Set:', discussion_set)
        except selenium.common.exceptions.NoSuchElementException:
            print('Discussions not directly found')

        if discussion_set > 10:
            break

    print('Discussions Exist, Proceeding to Extract...')

    '''     Navigating into 'All Discussions'       '''
    all_discussions_option = all_discussions_option.find_element_by_class_name('forum-nav-browse-title')
    exc_count = 0
    while True:
        if exc_count > 10:
            break
        try:
            all_discussions_option.click()
            break
        except ElementClickInterceptedException:
            exc_count += 1
            time.sleep(1)

    check_page_load(By.CLASS_NAME, 1, 'forum-nav-thread')
    thread_list = []

    '''    Checking network requests for the 'Threads' Request    '''
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
    else:
        print('Error Saving to Database, Program will now exit')
        return driver
    thread_list.extend(threads)

    ''' Getting Amount of Data Available '''
    num_of_pages = json_data['num_pages']
    current_page = json_data['page']
    print('No. of Pages:', num_of_pages)

    # print('Total No. of Pages:', num_of_pages)
    print('Retrieving Detailed Information')
    while current_page != num_of_pages and current_page <= 10:
        print('Current Page:', current_page)
        del driver.requests

        forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
        threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
        thread_count = threads.__len__()

        timeout_count = 0
        while True:
            if timeout_count > 20:
                print('Timeout')
                break
            try:
                load_more_btn = driver.find_element_by_class_name('forum-nav-load-more-link')
                load_more_btn.click()
                break
            except ElementClickInterceptedException:
                print('load-more-btn click action intercepted, trying again...')
                time.sleep(0.5)
                timeout_count += 1
        timeout_count = 0
        while True:
            if timeout_count > 10:
                print('Timeout')
                break
            forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
            threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
            new_thread_count = threads.__len__()
            if new_thread_count != thread_count:
                break
            print('Threads not yet loaded, trying again...')
            time.sleep(1)
            timeout_count += 1

        for request in driver.requests:
            try:
                if 'application/json' in request.response.headers['Content-Type']:
                    # print(request.path, request.response.headers['Content-Type'])
                    response_body = request.response.body.decode()
                    break
            except:
                pass

        try:
            json_data = json.loads(response_body)
            threads = json_data['discussion_data']
            Thread.upsert_threads(threads)
            thread_list.extend(threads)
        except JSONDecodeError:
            pass
        except KeyError:
            print('KeyError: Response Data displayed below')
            pprint(json_data)

        try:
            current_page = json_data['page']
        except:
            pprint(json_data)
            break

        print('Current Page=', current_page)

    # print('All Threads Have Been Loaded to the UI, Iterations=', current_page)

    forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
    thread_elems = forum_thread_list.find_elements_by_class_name('forum-nav-thread')

    print('Starting to collect detailed thread information')
    # Iterating through the Elements
    new_thread_info = []
    # print('Thread Element Count =', thread_elems.__len__())
    # print('Thread List Count =', thread_list.__len__())
    print('Total No. of Threads:', thread_list.__len__())
    demo_count = 0
    for thread_elem in thread_elems:
        if demo_count >= 10:
            break
        thread_title = thread_elem.find_element_by_class_name('forum-nav-thread-title').text

        # found = False
        for thread in thread_list:
            if thread_title == thread['title']:
                found_thread = thread
                # found = True
                # print('Match Found')
                break
        # if not found:
        #     continue

        if found_thread['comments_count'] == 0:
            # print('no comments')
            continue

        del driver.requests
        while True:
            try:
                thread_elem.click()
                break
            except:
                print('Exception Caught: Element Not Clickable, Retrying')
                time.sleep(1)

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
        demo_count += 1

    print('No. of Threads which contain comments:', new_thread_info.__len__())
    db_action_status = Thread.upsert_threads(new_thread_info)
    if db_action_status:
        print('Detailed Thread Info. has been saved to the database')

    print('All Forum Data Retrieved')

    return driver

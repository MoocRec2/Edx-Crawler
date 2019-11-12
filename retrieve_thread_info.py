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


# import logging

# logging.basicConfig(level=logging.DEBUG)


def retrieve_thread_info(course_url):
    """ Retrieves the threads of a course and saves them in the database """
    options = Options()
    run_in_background = True
    if run_in_background:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
    print('Run In Background:', run_in_background)
    driver = webdriver.Chrome('C:/chromedriver', options=options)

    # Sign in
    print('Authentication: In Progress')
    driver.get('https://courses.edx.org/login')
    email_input = driver.find_element_by_name("email")
    password_input = driver.find_element_by_name("password")
    # email_input.send_keys("smrbasil4@gmail.com")
    email_input.send_keys("smrbasil4@hotmail.com")
    password_input.send_keys("nvidia1024")
    login_button = driver.find_element_by_class_name('login-button')
    login_button.click()
    print('Authentication: Finished')

    # Get Cookies
    # print('Getting Cookies')
    # cookies = driver.get_cookies()
    # cookies_dict = {}
    # for cookie in cookies:
    #     cookies_dict[cookie.get('name')] = cookie.get('value')

    print('Generating Discussion URL from Course URL: In Progress')
    print('Course URL:', course_url)
    # Get Discussion URL from Course URL
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

    print('Generating Discussion URL from Course URL: Finished')
    print('Discussion URL:', discussion_url)

    refresh_delay = 1

    def check_page_load(by, delay, element_id):
        print('Waiting for the page (or elements within the page) to finish loading...')
        count = 0
        while count < 10:
            try:
                WebDriverWait(driver, delay).until(EC.presence_of_element_located((by, element_id)))
                break
            except TimeoutException:
                pass
            count += 1

    check_page_load(By.ID, refresh_delay, 'my-courses')

    print('Navigating to Discussion URL')
    driver.get(discussion_url)

    try:
        print('Searching for the Discussions Section: In Progress')
        all_discussions_option = driver.find_element_by_id('all_discussions')
        print('Searching for the Discussions Section: Finished')
    except selenium.common.exceptions.NoSuchElementException:
        print(
            'Potential problems may be that the course is not enrolled to or that the discussion does not exist '
            'on the platform itself')
        driver.quit()
        # quit()
        return
    all_discussions_option = all_discussions_option.find_element_by_class_name('forum-nav-browse-title')
    while True:
        try:
            all_discussions_option.click()
            break
        except ElementClickInterceptedException:
            time.sleep(2)

    check_page_load(By.CLASS_NAME, 1, 'forum-nav-thread')
    thread_list = []

    print('Extracting Basic Information of the Threads: In Progress')
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

    print('Extracting Basic Information of the Threads: Finished')
    threads = json_data['discussion_data']

    print('Saving the Information: In Progress')
    results = Thread.upsert_threads(threads)
    if results:
        print('Saving the Information: Finished')
    else:
        print('Saving the Information: Error')
        print('Exiting Program')
        quit(-1)

    thread_list.extend(threads)

    num_of_pages = json_data['num_pages']
    current_page = json_data['page']

    # ----- Retrieving Detailed Information of Threads -----
    # print('Total No. of Pages:', num_of_pages)
    demo_page_count = 10
    print('Detailed Information, No. of Pages = ', num_of_pages)
    print('Detailed Information, Demo No. of Pages = ', demo_page_count)
    print('Retrieving Detailed Information: In Progress')
    while current_page != num_of_pages and current_page <= demo_page_count:
        # The previous requests are cleared from history so that searching for the new requests is easier
        del driver.requests

        ''' Only a subset of the threads titles are loaded to the UI
        The rest of them are loaded (by the code below) by iteratively clicking the "Load More" button 
        '''
        forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
        threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
        thread_count = threads.__len__()
        print('Retrieving Detailed Information: In Progress, Loading Details to UI')
        while True:
            try:
                load_more_btn = driver.find_element_by_class_name('forum-nav-load-more-link')
                load_more_btn.click()
                break
            except ElementClickInterceptedException:
                time.sleep(0.5)
                pass

        while True:
            forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
            threads = forum_thread_list.find_elements_by_class_name('forum-nav-thread')
            new_thread_count = threads.__len__()
            if new_thread_count != thread_count:
                break
            # print('Threads not yet loaded, trying again...')
            time.sleep(1)

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
            print('Retrieving Detailed Information: In Progress, Current Page:', current_page)
        except:
            pprint(json_data)
            break

    # print('All Threads Have Been Loaded to the UI, Iterations=', current_page)

    forum_thread_list = driver.find_element_by_class_name('forum-nav-thread-list')
    thread_elems = forum_thread_list.find_elements_by_class_name('forum-nav-thread')

    print('Starting to collect detailed thread information')
    print('Retrieving Detailed Information: In Progress, Extracting Information from the UI')
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

    print('Retrieving Detailed Information: Finished')
    print('Saving Detailed Information: In Progress')
    db_action_status = Thread.upsert_threads(new_thread_info)
    if db_action_status:
        print('Saving Detailed Information: Finished')
    else:
        print('Saving Detailed Information: Error')

    driver.quit()

    return True

from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def get_cookies():
    # Optional argument, if not specified will search path.
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    options.add_argument('log-level=3')
    driver = webdriver.Chrome('C:/chromedriver', options=options)

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

    return cookies_dict


def get_cookies_and_driver():
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
    # driver.quit()

    return cookies, driver

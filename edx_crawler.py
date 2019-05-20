import time
from selenium import webdriver

driver = webdriver.Chrome('C:/chromedriver')  # Optional argument, if not specified will search path.

# Home Page
# driver.get('https://www.edx.org/');
# nav_div = driver.find_element_by_class_name('js-user-cta')
# sign_in_button = nav_div.find_element_by_tag_name('a')
# sign_in_button.click()

# Sign in Page
# Can Directly Navigate to the Sign in Page by link
# Link = https://courses.edx.org/login

driver.get('https://courses.edx.org/login')
email_input = driver.find_element_by_name("email")
password_input = driver.find_element_by_name("password")

email_input.send_keys("smrbasil4@gmail.com")
password_input.send_keys("nvidia1024")

login_button = driver.find_element_by_class_name('login-button')
login_button.click()

time.sleep(10)

driver.get('https://www.edx.org/course')

# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5)  # Let the user actually see something!
driver.quit()

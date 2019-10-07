import time
from selenium import webdriver
import requests
from local_storage import LocalStorage

# Optional argument, if not specified will search path.
driver = webdriver.Chrome('C:/chromedriver')

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

cookies = driver.get_cookies()
cookies_dict = {}
for cookie in cookies:
    cookies_dict[cookie.get('name')] = cookie.get('value')

old_url = 'https://www.edx.org/api/v1/catalog/search?featured_course_ids=course-v1:IUx+BUKD-X590+1T2019,course-v1:GTx+ISYE6501x+2T2019a,course-v1:CurtinX+APP1x+1T2019,course-v1:UBCx+COMM220x+3T2017,course-v1:HarvardX+PH125.1x+1T2019a,course-v1:MichiganX+py4e101x+1T2019,course-v1:IBM+DA0101EN+3T2018,course-v1:MITx+6.431x+2T2019,course-v1:Microsoft+DAT248x+1T2019a&featured_programs_uuids=71c95834-f6df-4f78-8cd7-c6461dd9b1d4,7278cf26-3f5b-4852-9ae7-f26396bbaa66,a2a6a8f9-7b61-49ce-9d62-7e959b776fb7,3a8b985d-fece-4199-9534-899bbe456829,8ac6657e-a06a-4a47-aba7-5c86b5811fa1,482dee71-e4b9-4b42-a47b-3e16bb69e8f2,3c32e3e0-b6fe-4ee4-bd4f-210c6339e074,9523bd51-7f72-49cf-89ea-63a0a7a0ed05,38dde1fd-e9a4-4f4b-9c87-87a3d0161830'

courses_url = 'https://www.edx.org/api/v1/catalog/search?selected_facets[]=subjects_exact:Computer Science'


r = requests.get(courses_url, cookies=cookies_dict)

response_data = r.json()

print(response_data.keys())

print(response_data)

print(response_data['objects'])

courses = response_data['objects']['results']
print('FIRST PAGE')
for course in courses:
    print(course['title'])

next_url = response_data['objects']['next']

print(next_url)

r = requests.get(next_url)
response_data = r.json()
courses = response_data['objects']['results']
print('SECOND PAGE')
for course in courses:
    print(course['title'])
course_list = []

time.sleep(10)

# search_box.send_keys('ChromeDriver')
# search_box.submit()
# time.sleep(5)  # Let the user actually see something!
driver.quit()

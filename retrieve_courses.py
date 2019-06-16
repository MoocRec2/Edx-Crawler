import authenticate
import requests
from pprint import pprint
from db_connector import Course

# from db_connector

cookies = authenticate.get_cookies()

# Start
courses_url = 'https://www.edx.org/api/v1/catalog/search?selected_facets[]=subjects_exact:Computer Science'

next_url = courses_url
count = 1

while True:
    print('Iteration =', count)
    r = requests.get(next_url, cookies=cookies)
    response_data = r.json()
    courses = response_data['objects']['results']
    result = Course.upsert_courses(courses)
    if result:
        print('Saved/Updated', courses.__len__(), ' Courses')
    next_url = response_data['objects']['next']
    count += 1

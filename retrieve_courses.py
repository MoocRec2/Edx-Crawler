import authenticate
import requests
from pprint import pprint
from db_connector import Course
import time

# from db_connector

start_time = time.time()

cookies = authenticate.get_cookies()

# Start
# courses_url = 'https://www.edx.org/api/v1/catalog/search?selected_facets[]=subjects_exact:Computer Science'
courses_url = 'https://www.edx.org/api/v1/catalog/search'

next_url = courses_url
count = 1
course_count = 0

while True:
    print('Iteration =', count)
    if next_url is None:
        break
    r = requests.get(next_url, cookies=cookies)
    response_data = r.json()
    courses = response_data['objects']['results']
    result = Course.upsert_courses(courses)
    if result:
        courses_len = courses.__len__()
        print('Saved/Updated', courses_len, ' Courses')
        course_count += courses_len
    next_url = response_data['objects']['next']
    count += 1

print('Retrieved {} Courses'.format(course_count))

end_time = time.time()

elapsed_time = end_time - start_time

print('Elapsed Time:', elapsed_time)

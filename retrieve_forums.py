import authenticate
import requests

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
    for course in courses:
        print(course['title'])
    next_url = response_data['objects']['next']
    count += 1

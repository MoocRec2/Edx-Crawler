from retrieve_thread_info import retrieve_thread_info
import db_connector
from pprint import pprint

'''
    MAIN Script
    
    Process:
    1 - Get Courses
    2 - Iterate Courses and Get their Threads
'''

courses_alt = list(db_connector.Course.get_edx_courses())

courses = db_connector.Course.get_courses_alt()

total = courses_alt.__len__()
print('No. of Edx Courses in Database: ', total)

print('Enter No. of Courses to Process:')
num = input()
num = int(num)

count = 0
driver = None
for course in range(num):
    count += 1
    print('------ Iteration', count, '------')
    driver = retrieve_thread_info(courses[course], driver)
    is_authenticated = True
    print('------- Overall progress:', (count / total) * 100, '%')

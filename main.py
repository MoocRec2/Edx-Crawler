from retrieve_thread_info import retrieve_thread_info
import db_connector
from pprint import pprint
import time

'''
    MAIN Script
    
    Process:
    1 - Get Courses from Database
    2 - Iterate Courses and Get their Threads
    
    Note: Courses retrieving logic exists in the retrieve_courses.py script
'''

start_time = time.time()

courses_alt = list(db_connector.Course.get_edx_courses())

courses = db_connector.Course.get_courses_alt()

total = courses_alt.__len__()
print('No. of Edx Courses in Database: ', total)

print('Enter No. of Courses to Process:')
num = input()
num = int(num)

count = 0
driver = None

tracking_array = list(range(num))

for x in tracking_array:
    count += 1
    print('------ Course No.:', count, '------')
    driver = retrieve_thread_info(courses[x % courses.__len__()], driver)
    is_authenticated = True
    print('------- Overall progress:', (count / total) * 100, '%')

end_time = time.time()
time_elapsed = end_time - start_time
print('Time Elapsed:', time_elapsed, 'seconds')

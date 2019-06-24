from retrieve_thread_info import retrieve_thread_info
from db_connector import Course
from pprint import pprint

course_one = 'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/'  # Approx. 5 Threads
course_two = 'https://courses.edx.org/courses/course-v1:UCSanDiegoX+DSE200x+1T2019a/course/'  # Approx. 180 Threads
course_three = 'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/'
course_four = 'https://courses.edx.org/courses/course-v1:HarvardX+PH125.8x+2T2018/course/'  # Approx. 99 Threads

# courses = Course.get_courses()
# for course in courses:
#     pprint(course)
#     retrieve_thread_info(course['marketing_url'])

retrieve_thread_info(course_four)

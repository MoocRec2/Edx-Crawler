from retrieve_thread_info import retrieve_thread_info
from db_connector import Course
from pprint import pprint


def prepare_course_url(course_key):
    course_url = 'https://courses.edx.org/courses/' + course_key + '/course/'
    return course_url


courses = list(Course.get_courses())
# print('No. of Courses:', courses.__len__())
limit = 10
count = 0
for course in courses:
    if count > limit:
        break
    # pprint(course)
    retrieve_thread_info(course['marketing_url'])
    count += 1

# retrieve_thread_info(course_four)

# retrieve_thread_info(course_5)

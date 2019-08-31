from retrieve_thread_info import retrieve_thread_info
from db_connector import Course
from pprint import pprint

course_one = 'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/'  # Approx. 5 Threads
course_two = 'https://courses.edx.org/courses/course-v1:UCSanDiegoX+DSE200x+1T2019a/course/'  # Approx. 180 Threads
course_three = 'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/'
course_four = 'https://courses.edx.org/courses/course-v1:HarvardX+PH125.8x+2T2018/course/'  # Approx. 99 Threads
course_five = 'https://courses.edx.org/courses/course-v1:HarvardX+CS50+X/course/'  # Discussions do not exist
course_six = 'https://www.edx.org/course/introduction-to-kubernetes'
# courses = Course.get_courses()
# for course in courses:
#     pprint(course)
#     retrieve_thread_info(course['marketing_url'])

courses = [
    # 'https://courses.edx.org/courses/course-v1:HKUSTx+ELEC3500.1x+2T2019/course/',
    'https://courses.edx.org/courses/course-v1:BerkeleyX+GG101x+3T2019/course/', # Error
    'https://courses.edx.org/courses/course-v1:LinuxFoundationX+LFS158x+2T2019/course/', # Error
    'https://courses.edx.org/courses/course-v1:HarvardX+CS50+X/course/', # Error
    'https://courses.edx.org/courses/course-v1:MichiganX+py4e101x+1T2019/course/',
    # ''
]

# courses = list(Course.get_edx_courses())
total = courses.__len__()
print('No. of Edx Courses in Database: ', total)

count = 0
driver = None
for course in courses:
    count += 1
    print('------ Iteration', count, '------')
    # url = 'https://courses.edx.org/courses/' + course['key'] + '/course'
    # driver = retrieve_thread_info(course['marketing_url'], driver)
    driver = retrieve_thread_info(course, driver)
    is_authenticated = True
    print('------- Overall progress:', (count / total) * 100, '%')

# retrieve_thread_info(course_four, None)

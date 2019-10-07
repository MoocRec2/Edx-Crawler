from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import json

platform_to_collection_mapping = {
    'Edx': 'threads',
    'FutureLearn': 'future_learn_threads',
    'Coursera': 'coursera_threads'
}

# with open('./db_credentials.json', 'r') as f:
#     db_credentials = json.load(f)
#
# connection_string = db_credentials['connectionString']

# client = MongoClient('mongodb://api:backendapi1@ds157901.mlab.com:57901/moocrecv2?retryWrites=false')
client = MongoClient('mongodb://localhost:27017/moocrecv2')
# client = MongoClient(connection_string)
# client = MongoClient('mongodb://user:password@52.66.18.67:27017/moocrec-v2')

database = client['moocrec-v2']


class Thread:

    @staticmethod
    def save_threads(threads):
        try:
            result = database.threads.insert(threads)
            return result
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
        except:
            print('An Error Occurred')

    @staticmethod
    def upsert_threads(threads):
        try:
            for thread in threads:
                database.threads.update_one({'id': thread['id']}, {"$set": thread}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_discussion_threads_with_responses(course_id):
        try:
            results = database.threads.find(
                {
                    'course_id': course_id,
                    'thread_type': 'discussion',
                    '$or': [
                        {'children': {'$exists': 'true'}},
                        {'non_endorsed_responses': {'$exists': 'true'}}
                    ]
                }
            ).limit(100)
            return results
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return

    @staticmethod
    def get_sentiment_analyzed_threads():
        try:
            results = database.Threads.find({
                'course_id': 'course-v1:UCSanDiegoX+DSE200x+1T2019a',
                'thread_type': 'discussion',
                '$or': [
                    {'children': {'$exists': 'true'}},
                    {'non_endorsed_responses': {'$exists': 'true'}}
                ],
                '$and': [{'is_sentiment_analyzed': {'$exists': 'true'}}, {'sentiment_score': {'$exists': 'true'}}]
            }, {'is_sentiment_analyzed': 1, 'sentiment_score': 1}).sort({'sentiment_score': -1})
            return results
        except:
            return []


class Course:

    @staticmethod
    def upsert_courses(courses):
        try:
            for course in courses:
                database.courses.update_one({'key': course['key']}, {"$set": course}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

    @staticmethod
    def get_course(course_key):
        try:
            courses = database.courses.find({'key': course_key})
            return courses[0]
        except:
            return None
            pass

    @staticmethod
    def get_courses():
        try:
            courses = database.courses.find({'platform': 0})
            return courses
        except:
            return None
            pass

    @staticmethod
    def get_edx_courses():
        try:
            courses = database.courses.find({'platform': 'Edx'})
            return courses
        except:
            print('An Error Occurred')

    @staticmethod
    def get_courses_alt():
        courses_alt = [
            'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/',  # Approx. 5 Threads
            'https://courses.edx.org/courses/course-v1:UCSanDiegoX+DSE200x+1T2019a/course/',  # Approx. 180 Threads
            'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/',
            'https://courses.edx.org/courses/course-v1:HarvardX+PH125.8x+2T2018/course/',  # Approx. 99 Threads
            'https://courses.edx.org/courses/course-v1:HarvardX+CS50+X/course/',  # Discussions do not exist
            'https://www.edx.org/course/introduction-to-kubernetes'
        ]
        courses_alt = [
            'https://courses.edx.org/courses/course-v1:HKUSTx+ELEC3500.1x+2T2019/course/',
            'https://courses.edx.org/courses/course-v1:BerkeleyX+GG101x+3T2019/course/',
            'https://courses.edx.org/courses/course-v1:LinuxFoundationX+LFS158x+2T2019/course/',
            'https://courses.edx.org/courses/course-v1:HarvardX+CS50+X/course/',
            'https://courses.edx.org/courses/course-v1:MichiganX+py4e101x+1T2019/course/'
        ]
        courses_key = [
            'course-v1:HKUSTx+ELEC3500.1x+2T2019',
            'course-v1:BerkeleyX+GG101x+3T2019',
            'course-v1:LinuxFoundationX+LFS158x+2T2019',
            'course-v1:HarvardX+CS50+X',
            'course-v1:MichiganX+py4e101x+1T2019',
        ]
        try:
            courses_al = list(database.courses.find({'platform': 0}))
            length = courses_al.__len__()
            return courses_alt
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occured - DB Connector')
            return None
            pass


class Subject:

    @staticmethod
    def upsert_subjects(subjects):
        try:
            for subject in subjects:
                database.subjects.update_one({'key': subject['uuid']}, {"$set": subject}, upsert=True)
            return True
        except ServerSelectionTimeoutError:
            print('Error Connecting to Database')
            return False
        except:
            print('An Error Occurred')
            return False

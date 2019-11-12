from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import copy

# client = MongoClient('mongodb://forum_analyzer:admin123@ds157901.mlab.com:57901/moocrecv2')
client = MongoClient('mongodb://localhost:27017/moocrecv2')

database = client.moocrecv2


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


class db_client:
    class courses:
        @staticmethod
        def find(x):
            courses = [
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/'},
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:UCSanDiegoX+DSE200x+1T2019a/course/'},
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/'},
                {
                    'marketing_url': 'https://courses.edx.org/courses/course-v1:UWashingtonX+PM-IT-002x+2T2019/course/'},
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:Microsoft+DAT236x+1T2019a/course/'},
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:UCSanDiegoX+DSE200x+1T2019a/course/'},
                {'marketing_url': 'https://courses.edx.org/courses/course-v1:UPValenciaX+TGV201x.2+2T2019/course/'},
            ]
            new = []
            for x in range(3500):
                new.append(copy.deepcopy(courses[x % courses.__len__()]))
            return new


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
            courses = db_client.courses.find({'platform': 'Edx'})
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

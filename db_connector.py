from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError

client = MongoClient('mongodb://forum_analyzer:admin123@ds157901.mlab.com:57901/moocrecv2')

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

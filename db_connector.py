from pymongo import MongoClient

client = MongoClient('localhost:27017')

database = client.moocrecv2

server_status_result = database.command('serverStatus')

print(server_status_result)


class Thread:

    @staticmethod
    def save_threads(threads):
        result = database.threads.insert(threads)
        return result

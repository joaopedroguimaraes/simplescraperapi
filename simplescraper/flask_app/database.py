from pymongo import MongoClient

from .credentials import MONGO_URI, MONGO_DATABASE


class Database:

    def __init__(self):
        self.mongo = MongoClient(MONGO_URI).\
            get_database(MONGO_DATABASE)
        self.codes = self.mongo.codes

    def insert(self, codes):
        return self.codes.insert(codes)

    def find_all(self):
        return [file for file in self.codes.find()]

    def find_one(self, code_number):
        return self.codes.find_one({'code_number': code_number})

    def delete_one(self, code_number):
        return self.codes.delete_one({'code_number': code_number})

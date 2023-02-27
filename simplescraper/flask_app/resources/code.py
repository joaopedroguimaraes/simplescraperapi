from bson.json_util import dumps
from flask import render_template, make_response, jsonify
from flask_api import status
from flask_restful import Resource

from ..code_scraper_trigger import CodeScraperTrigger
from ..database import Database


class Code(Resource):
    __slots__ = ("DEFAULT_HEADERS",)

    def __init__(self):
        self.DEFAULT_HEADERS = {'Content-Type': 'text/html'}
        self.database = Database()
        self.trigger = CodeScraperTrigger()

    def get(self, code_number):
        result = self.database.find_one(code_number)
        if result is None:
            result = self.trigger.parse_data(code_number)
        return self.__sanitize_item(result)

    @staticmethod
    def __sanitize_item(code_item):
        if code_item is not None:
            code_item.pop('_id')
        return code_item

from flask import make_response, render_template
from flask_restful import Resource, reqparse

from .code import Code

parser = reqparse.RequestParser()
parser.add_argument('code_number', type=str, location='form')


class Search(Resource):
    __slots__ = ("DEFAULT_HEADERS",)

    def __init__(self):
        self.DEFAULT_HEADERS = {'Content-Type': 'text/html'}
        self.api = Code()

    @staticmethod
    def get():
        return make_response(
            render_template("index.html", has_code_number=False))

    def post(self):
        args = parser.parse_args()
        code_number = args['code_number']
        file_infos = self.api.get(code_number)['file_infos']
        return make_response(
            render_template("index.html",
                            has_code_number=True,
                            code_number=code_number,
                            file_infos=file_infos
                            ))

from flask import make_response, jsonify

from .resources.download import Download
from .resources.search import Search
from .resources.code import Code
from .settings import APP, API


@APP.errorhandler(400)
def handle_400_error(_error):
    return make_response(jsonify({'error': 'Misunderstood'}), 400)


@APP.errorhandler(404)
def handle_404_error(_error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@APP.errorhandler(500)
def handle_500_error(_error):
    return make_response(jsonify({'error': 'Server error'}), 500)


API.add_resource(Code, "/api/codes/<code_number>", endpoint="codes")
API.add_resource(Download,
                 "/api/download/<code_number>/<filename>",
                 endpoint="download")
API.add_resource(Search, "/", endpoint="")


def start():
    APP.run(debug=True)

# if __name__ == "__main__":
#

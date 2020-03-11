import json
from json import JSONEncoder


class HttpResponse(JSONEncoder):
    def __init__(self, data, headers, status_code):
        self.data = data
        self.headers = headers
        self.status_code = status_code

    def __repr__(self):
        return json.dumps(self, default=vars, indent=4)
import json
from json import JSONEncoder


class HttpRequest(JSONEncoder):
    def __init__(self, method, api, content_type, body, client_ip, headers, query_param):
        self.method = method
        self.api = api
        self.content_type = content_type
        self.body = body
        self.client_ip = client_ip
        self.headers = headers
        self.query_param = query_param

    def __repr__(self):
        return json.dumps(self, default=vars, indent=4)
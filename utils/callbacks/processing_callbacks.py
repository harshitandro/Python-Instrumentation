from models.http_request import HttpRequest
from utils.callbacks.callback_utils import extract_headers_from_environ, extract_client_ip_from_environ, \
    print_http_intercept, print_db_call_intercept


def django_request_processing_callback(source, threadID, *args, **kwargs):

    method = args[1].method
    api = args[1].path
    content_type = args[1].content_type
    body = args[1].body.decode("utf-8")
    client_ip = extract_client_ip_from_environ(args[1].environ)
    headers = extract_headers_from_environ(args[1].environ)
    query_param = getattr(args[1], method)

    request = HttpRequest(method, api, content_type, body, client_ip, headers, query_param)

    print_http_intercept("Django", threadID, request)


def django_request_static_processing_callback(source, threadID, *args, **kwargs):
    method = args[1].method
    api = args[1].path
    content_type = args[1].content_type
    body = args[1].body.decode("utf-8")
    client_ip = extract_client_ip_from_environ(args[1].environ)
    headers = extract_headers_from_environ(args[1].environ)
    query_param = getattr(args[1], method)

    request = HttpRequest(method, api, content_type, body, client_ip, headers, query_param)
    print_http_intercept("Django Static", threadID, request)


def flask_request_processing_callback(source, threadID, *args, **kwargs):
    self = args[0]

    # Extract base environ
    ctx = self.request_context(args[1])
    req = ctx.request

    method = req.method
    api = req.path
    content_type = req.content_type
    body = req.data.decode("utf-8")
    client_ip = extract_client_ip_from_environ(req.environ)
    headers = extract_headers_from_environ(req.environ)
    query_param = req.query_string.decode("utf-8")

    request = HttpRequest(method, api, content_type, body, client_ip, headers, query_param)

    print_http_intercept("Flask", threadID, request)


def mysql_processing_callback(source, threadID, *args, **kwargs):
    self = args[0]
    query = args[1]
    if len(args) >= 3:
        params = args[2]
        print_db_call_intercept("MySQL", threadID, query, params)
    else:
        print_db_call_intercept("MySQL", threadID, query, None)


def empty_processing_callback(source, threadID, *args, **kwargs):
    # print_generic_intercept(source, threadID, args, kwargs)
    pass
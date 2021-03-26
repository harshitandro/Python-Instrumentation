from models.http_response import HttpResponse
from utils.callbacks.callback_utils import print_http_response_intercept


def django_ret_processing_callback(source, threadID, *ret_val):
    pass


def django_static_ret_processing_callback(source, threadID, *ret_val):
    pass


def flask_ret_processing_callback(source, threadID, *ret_val):
    pass


def empty_ret_processing_callback(source, threadID, *ret_val):
    pass


def flask_ret_processing_callback(source, threadID, *ret_val):
    pass


def flask_ret_response_processing_callback(source, threadID, *ret_val):
    # print("flask args : ", *ret_val)
    status_code = getattr(ret_val[0], "status")
    # print("flask status_code : ", status_code)
    data = None
    if ret_val[0].direct_passthrough is False:
        data = (ret_val[0].get_data()).decode("utf-8")
    response = HttpResponse(data, None, status_code)
    print_http_response_intercept("Flask", threadID, response)
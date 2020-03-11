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


def flask_ret_processing_callback(source, threadID, *args, **kwargs):
    response = HttpResponse(args[1].get_data(), None ,args[1]._get_status())
    print_http_response_intercept("Flask", threadID, response)

def extract_headers_from_environ(environ) -> dict :
    headers = {}
    for header_entry in environ.items():
        if header_entry[0].startswith("HTTP_"):
            key = header_entry[0].partition("_")[2]
            val = header_entry[1]
            if key != "":
                headers[key] = val
    return headers


def extract_client_ip_from_environ(environ) -> dict :
    return environ["REMOTE_ADDR"]


def print_http_intercept(server_name, threadID, request):

    data = '''
        --------------------------------------------------------------------------------------------------------------------
        Intercepted {} HTTP request on thread {}
        --------------------------------------------------------------------
        {}
        --------------------------------------------------------------------------------------------------------------------
    '''

    print(data.format(server_name, threadID, request))


def print_http_response_intercept(server_name, threadID, response):

    data = '''
        --------------------------------------------------------------------------------------------------------------------
        Intercepted {} HTTP response on thread {}
        --------------------------------------------------------------------
        {}
        --------------------------------------------------------------------------------------------------------------------
    '''

    print(data.format(server_name, threadID, response))


def print_db_call_intercept(db_server_name, threadID, query, parameters):
    data = '''
        --------------------------------------------------------------------------------------------------------------------
        Intercepted {} DB query on thread {}
        --------------------------------------------------------------------
        Query  : {}
        Parameters : {}
        --------------------------------------------------------------------------------------------------------------------
    '''

    print(data.format(db_server_name, threadID, query, parameters))


def print_generic_intercept(source, threadID, args, kvargs):
    data = '''
        --------------------------------------------------------------------------------------------------------------------
        Intercepted hooked API '{}' on thread {}
        ------------------------------------------------------------------------------
        Arguments           : {}
        Key Value Arguments : {}
        --------------------------------------------------------------------------------------------------------------------
    '''

    print(data.format(source, threadID, args, kvargs))
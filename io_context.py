"""TODO."""

from http.cookies import SimpleCookie
from pprint import pprint


class IOContext(object):
    """TODO."""

    host = None  # host that is requested
    path = None  # path that is requested
    command = None  # z.B. GET, POST, …

    query_parameters = {}  # URL parameter, i.e. www.example.com?key=value

    post_parameters = {}  # POST parameter, i.e. from a web form or AJAX call

    def __init__(self,
                 host: str,
                 path: str,
                 command: str,
                 query_parameters: dict,
                 cookies,
                 user=None,
                 original_path=None,
                 force_response_code=None,
                 cookies_accepted: bool = False,
                 cookies_rejected: bool = False,
                 is_ajax_request: bool = False,
                 is_json_request: bool = False,
                 post_parameters: dict = None
                 ):
        self.host = host
        self.path = path
        self.command = command
        self.query_parameters = query_parameters
        self.cookies = cookies
        self.user = user
        self.original_path = original_path
        self.force_response_code = force_response_code
        self.cookies_accepted = cookies_accepted
        self.cookies_rejected = cookies_rejected
        self.is_ajax_request = is_ajax_request
        self.is_json_request = is_json_request
        self.post_parameters = post_parameters

        self.response_status = None
        self.response_body = None
        self.response_headers = []

    @staticmethod
    def fill_env_query_params(query_string):
        return dict(param.split("=") for param in query_string.split("&"))

    @classmethod
    def init_from_gunicorn_environ(cls, environ):
        pprint(environ)
        return cls(
            host=environ.get('HTTP_HOST'),
            path=environ.get('PATH_INFO'),
            command=environ.get('REQUEST_METHOD'),
            query_parameters=cls.fill_env_query_params(
                environ.get('QUERY_STRING')),
            # TODO fill cookie
            cookies=environ.get('HTTP_COOKIE')
        )

    @property
    def request_parameters(self):
        """TODO."""
        return dict(
            list(self.query_parameters.items()) +
            list(self.post_parameters.items())
        )

    @request_parameters.setter
    def request_parameters(self, value):
        """TODO."""
        raise NotImplementedError

    is_ajax_request = False  # set to True if request is AJAX call
    is_json_request = False  # set to True if request is JSON data

    user = None  # user object that is identified or authenticated

    cookies = SimpleCookie()  # cookies provided by the browser
    cookies_accepted = False  # set to True, if user actively accepts cookies
    cookies_rejected = False  # set to False, if user actively accepts cookies

    force_response_code = None  # HTTP response code in case of routing error
    original_path = None  # original request path in case of routing error

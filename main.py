import multiprocessing
from pprint import pprint

import gunicorn.app.base

from io_context import IOContext


def number_of_workers():
    return (multiprocessing.cpu_count() * 2) + 1


class WsgiWrapper(object):
    # hkk_app = Hkkapp(params)
    def __init__(self, hkk_app=None):
        self.environ = None
        self.io_context = None
        self.start_response = None
        # self.hkk_app = hkk_app

    def __call__(self, *args, **kwargs):
        self.environ = None
        self.io_context = None
        self.start_response = None
        return self.handler_app(*args)

    def handler_app(self, environ, start_response):
        self.environ = environ
        self.start_response = start_response
        self.io_context = IOContext.init_from_gunicorn_environ(environ)

        # start_response, response_body = self.hkk_app.handle_request(self.io_context)

        response_body = "<html>\n<body>\n<h1>Not Found Error</h1>\n<pre><src>" \
                        "</src></pre>\n</body>\n</html>\n".encode('utf-8')
        status = '200 OK'

        response_headers = [
            ('Content-Type', 'text/plain'),
        ]

        start_response(status, response_headers)

        return [response_body]


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super().__init__()

    def load_config(self):
        config = {key: value for key, value in self.options.items()
                  if key in self.cfg.settings and value is not None}
        for key, value in config.items():
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


if __name__ == '__main__':
    handler_app = WsgiWrapper()
    options = {
        'bind': '%s:%s' % ('127.0.0.1', '8080'),
        'workers': number_of_workers(),
    }
    StandaloneApplication(handler_app, options).run()

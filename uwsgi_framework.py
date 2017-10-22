import http.client
import re
import json


class UwsgiApp:
    def __init__(self):
        self.handlers = {}

    def __call__(self, environ, start_response):
        print(environ)
        url = environ['PATH_INFO']
        method = environ['REQUEST_METHOD']

        handler, url_args = self.get_handler(url, method)

        status_code, extra_headers, response_content = handler(environ, url_args)

        content_type = 'text/html'
        if not type(response_content) is str:
            response_content = json.dumps(response_content, indent=4)
            content_type = 'text/json'

        headers = {
            'Content-Type': content_type,
            'charset': 'utf-8'
        }
        headers.update(extra_headers)

        start_response('%s %s' % (status_code, http.client.responses[status_code]),
                       list(headers.items()))

        return [response_content.encode('utf-8')]

    def get_handler(self, url, method):
        handler = None
        url_args = None

        if not url.endswith('/'):
            handler = UwsgiApp.no_trailing_slash_handler
        else:
            for url_regexp, (current_handler, current_methods) in self.handlers.items():
                match = re.match(url_regexp, url)
                if match is None:
                    continue
                url_args = match.groupdict()
                if method not in current_methods:
                    handler = UwsgiApp.method_not_allowed
                    continue
                handler = current_handler
                break
            if handler is None:
                handler = UwsgiApp.page_not_found_handler
        return handler, url_args

    def add_handler(self, url, methods=None):
        methods = methods or ['GET']

        def wrapper(handler):
            self.handlers[url] = handler, methods
        return wrapper

    @staticmethod
    def no_trailing_slash_handler(environ, url_args):
        return (
            301,
            {'Location': '%s/' % environ['PATH_INFO']},
            'Redirect to URL with trailing slash'
        )

    @staticmethod
    def page_not_found_handler(environ, url_args):
        response_content = 'Page ' + environ['HTTP_HOST'] + environ['PATH_INFO'] + ' not found'
        return 404, {}, response_content

    @staticmethod
    def method_not_allowed(environ, url_args):
        response_content = 'Method ' + environ['REQUEST_METHOD'] + ' not allowed'
        return 405, {}, response_content

    @staticmethod
    def plain_text_to_html(text):
        return '<html><head></head><body>' + text + '</body></html>'

    @staticmethod
    def text_to_html_link(link, text):
        return '<p><a href=' + link + '>' + text + '</a></p>'

    @staticmethod
    def text_to_html_paragraph(text):
        return '<p>' + text + '</p>'

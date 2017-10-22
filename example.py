import http.client
from uwsgi_framework import UwsgiApp

application = UwsgiApp()


@application.add_handler(r'^/$')
def index_handler(environ, url_args):
    text = UwsgiApp.text_to_html_paragraph('Index page')
    text += UwsgiApp.text_to_html_paragraph('Links:')
    text += UwsgiApp.text_to_html_link('/', 'Index page')
    text += UwsgiApp.text_to_html_link('info/', 'Info page')
    text += UwsgiApp.text_to_html_link('products/', 'Link to products')
    text += UwsgiApp.text_to_html_link('products/123/', 'Link to product #123')
    status_code = 200

    return status_code, {}, UwsgiApp.plain_text_to_html(text)


@application.add_handler(r'^/info/$')
def info_handler(environ, url_args):
    host = environ['HTTP_HOST']
    path = environ['PATH_INFO']
    method = environ['REQUEST_METHOD']
    user_ip = environ['REMOTE_ADDR']
    browser = environ['HTTP_USER_AGENT']
    status_code = 200
    result_dict = {
        'URL': host + path,
        'Method': method,
        'Your IP': user_ip,
        'Browser': browser,
        'Status code': str(status_code) + ' ' + http.client.responses[status_code]
    }

    return status_code, {}, result_dict


@application.add_handler(r'^/products/(?P<product_id>\d+)?/?$')
def products_handler(environ, url_args):
    result_dict = {
        'Product ID': 'Product is not selected'
    }
    if url_args['product_id']:
        result_dict['Product ID'] = url_args['product_id']

    status_code = 200

    return status_code, {}, result_dict

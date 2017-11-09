# coding=utf-8
import time


def static_request_handler():
    return b'hello world I am from WSGI application'


def auto_request_handler():
    return time.ctime().encode()


class Applicaiton(object):
    HTML_ROOT_PATH = "."

    def __init__(self, urllist):
        self.url_list = urllist

    def __call__(self, envrion, start_response):
        head_list = [("Server", "HTTPServerByPython6.0")]
        file_name = envrion["FILE_NAME"]

        for url, func in self.url_list:
            if file_name.startswith(url):
                start_response("200 OK", head_list)
                return func()
        if file_name.endswith('.py'):
            try:
                module = __import__(file_name[1:-3])
            except Exception as e:
                start_response('404 Not Found', head_list)
                response_body = ('%s' % str(e)).encode()
            else:
                start_response('200 OK', head_list)
                response_body = module.application()

        else:
            try:
                date_file = open(self.HTML_ROOT_PATH+file_name, 'rb')
            except Exception as e:
                start_response('404 Not Found', head_list)
                response_body = ('%s '% str(e)).encode()

            else:
                start_response('200 OK', head_list)
                file_data = date_file.read()
                date_file.close()
                response_body = file_data
        return response_body

        start_response("200 OK", head_list)
        return b"hello world I am from WSGI application"


# 路由列表
url_list = [
    (r"/static/", static_request_handler),
    (r"/python/", auto_request_handler)
]


app = Applicaiton(url_list)
# app()   app.__call__()
# (源端口,源IP,目的端口,目的IP)

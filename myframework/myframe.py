# coding=utf-8
import time
import sys



# def static_request_handler(file_name, start_response):
def static_request_handler():
    head_list = [("Server", "HTTPServerByPython6.0")]
    # print(file_name)
    # print('hello world I am from WSGI application')
    return b'hello world I am from WSGI application'
    # try:
    #     data_file = open(HTML_ROOT_PATH + file_name, "rb")
    #     print(HTML_ROOT_PATH + file_name)
    # except FileNotFoundError as e:
    #     # 文件没找到
    #     start_response("404 Not Found", head_list)
    #     return ("R U form MARS %s " % str(e)).encode()
    # else:
    #     # 如果文件比较大 不适合这种场景
    #     file_data = data_file.read()
    #     data_file.close()
    #     start_response("200 OK", head_list)
    #     return file_data


# def auto_request_handler(file_name, start_response):
def auto_request_handler():

    head_list = [("Server", "HTTPServerByPython6.0")]
    return time.ctime().encode()
    # """处理以.py为结尾的文件"""
    #
    # try:
    #     module_name = __import__(file_name[1:-3])
    #     response_body = module_name.application()
    # except (ImportError, AttributeError) as e:
    #     start_response("404 Not Found", head_list)
    #     return ("R U form MARS %s " % str(e)).encode()
    #
    # else:
    #     start_response("200 OK", head_list)
    #     return response_body


class Applicaiton(object):
    HTML_ROOT_PATH = "."

    def __init__(self, urllist):
        self.url_list = urllist

    def __call__(self, envrion, start_response):
        head_list = [("Server", "HTTPServerByPython6.0")]
        file_name = envrion["FILE_NAME"]
        # file_name = environ["file_name"]
        flag = 0
        for url, func in self.url_list:
            if file_name.startswith(url):
                start_response("200 OK", head_list)
                # response_body = func(file_name, start_response)
                # return response_body
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


        # if flag == 0:
        #     start_response("404 Not Found", head_list)
        #     return b"request error"

        # head_list.append(("Conntent-Type","text/html"))
        start_response("200 OK", head_list)
        return b"hello world I am from WSGI application"
        # /static/
        # /python/


# 路由列表
url_list = [
    (r"/static/", static_request_handler),
    (r"/python/", auto_request_handler)
]


app = Applicaiton(url_list)
# app()   app.__call__()
# (源端口,源IP,目的端口,目的IP)

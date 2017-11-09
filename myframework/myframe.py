# coding=utf-8
import time


def static_request_handler():
    """静态内容显示，也可以是一个单独的文件，由下面的路径导入使用"""
    return b'hello world I am from WSGI application'


def auto_request_handler():
    """动态函数的功能，这里用一个函数来表示，也可以是一个单独的文件，由下面的路径导入使用"""
    return time.ctime().encode()


class Applicaiton(object):
    """应用框架的核心"""
    HTML_ROOT_PATH = "."

    def __init__(self, urllist):
        """路由列表"""
        self.url_list = urllist

    def __call__(self, envrion, start_response):
        head_list = [("Server", "HTTPServerByPython6.0")]
        file_name = envrion["FILE_NAME"]

        # 遍历路由，执行路由对应的函数
        for url, func in self.url_list:
            if file_name.startswith(url):
                start_response("200 OK", head_list)
                return func()

        if file_name.endswith('.py'):
            # 动态文件的处理
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
        # return b"hello world I am from WSGI application"


# 路由列表
url_list = [
    (r"/static/", static_request_handler),
    (r"/python/", auto_request_handler)
]


app = Applicaiton(url_list)
# app()   app.__call__()
# (源端口,源IP,目的端口,目的IP)

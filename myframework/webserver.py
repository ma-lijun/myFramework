# coding=utf-8
"""
1 创建用以监听的套接字
2 从已就绪队列中获取到一个客户端套接字 用以和客户端通信
3 解析用户请求
4 根据具体请求 是否能够被服务器满足 返回不同的状态码 200 OK / 404 Not Found
实现 能响应动态请求和静态请求的版本的 WSGI协议的web服务器
"""
import socket
from multiprocessing import Process
import re
import sys

HTML_ROOT_PATH = "."


class HTTPServer(object):
    """这是一个处理HTTP的相关类"""

    def __init__(self, app):
        self.app = app
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 保存响应行和响应头数据
        self.response_line_header = ""

    def bind_and_listen(self, port=8080):
        # 绑定端口 关联进程服务 和 端口
        server_address = ("", port)
        self.listen_socket.bind(server_address)
        # 监听
        self.listen_socket.listen(128)

    def start(self):
        # 取出一个客户端套接字
        while True:
            client_socket, client_address = self.listen_socket.accept()
            print("accept from %s's connect" % str(client_address))

            # 创建一个进程为客户端服务
            process = Process(target=self.request_handler, args=(client_socket, client_address))
            process.start()
            client_socket.close()  # 在父进程中不需要使用这个套接字通信

    def start_response(self, status, header_list):
        """设定响应行和响应头"""
        response_line = "HTTP/1.1 %s\r\n" % status
        response_headers = ""
        for header_name, header_value in header_list:
            response_headers += "%s: %s\r\n" % (header_name, header_value)

        # 拼接响应头和响应行数据
        self.response_line_header = response_line + response_headers

    def request_handler(self, client_socket, client_address):

        request_data = client_socket.recv(4096)
        # print(request_data)
        request_string_data = request_data.decode()

        # 将接收到的数据进行按行切割
        lines_list = request_string_data.split("\r\n")

        # 第0个元素就是请求行数据 "GET /index.html HTTP/1.1"
        request_line = lines_list[0]
        result = re.match(r"\w+\s+(/[^ ]*) +", request_line)
        if not result:
            return

        file_name = result.group(1)
        # 在web服务器中一般请求/  默认设置为/index.html
        if file_name == "/":
            file_name = "/index.html"
        env = {
            "FILE_NAME": file_name
        }
        # print(file_name)
        # .    + /index.html  ======> ./index.html
        # if file_name.endswith(".py"):
        # 代表用于请求的是一个.py文件  作为动态请求
        # response_body = module_name.application()

        response_body = self.app(env, self.start_response)
        response_data = (self.response_line_header + "\r\n").encode() + response_body
        # print(response_data)

        client_socket.send(response_data)
        client_socket.close()


"""
面向过程 吃(屎,狗)
面向对象 狗.吃(屎)
"""


def main():
    if len(sys.argv) == 1:
        print("参数错误 使用释放 python3 webxxx.py MyApp:app")
        return
    module_name_app_name = sys.argv[1]
    module_app_list = module_name_app_name.split(":")
    # len(module_name) == 1
    module_name = module_app_list[0]
    app_name = module_app_list[1]
    try:
        # import re ===  re = __import__("re")
        module_name = __import__(module_name)

        # module_name表示需要获取属性的对象  app_name表示属性的字符串形式
        # A fun    fun = getattr(a,"fun")
        app = getattr(module_name, app_name)

    except (ImportError, AttributeError) as e:
        print("输入参数错误")
        exit()

    # 服务器的启动入口，传参数"app"进入自己的框架
    http_server = HTTPServer(app)
    http_server.bind_and_listen(8080)
    http_server.start()


if __name__ == '__main__':
    main()

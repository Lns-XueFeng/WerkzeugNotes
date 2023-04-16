from wsgiref.simple_server import make_server


"""
Werkzeug是一个WSGI 工具包
WSGI是一个Web应用和服务器通信的协议, Web应用可以通过WSGI一起工作
WSGI规范了应用程序的编写, environ和start_response都是WSGI规范中定义的参数
"""


"""
可见, HTTP的请求报文、响应报文通过符合WSGI规范的服务器程序均已帮助我们处理
我们仅需将精力着眼于具体的web逻辑实现, 而不必要像之前那样什么都亲历亲为了

environ: 是一个包含所有HTTP请求信息的字典对象, 可以从此对象中获取信息构建响应
start_response: 是一个可调用对象, 
  它接收两个参数, 一个是HTTP响应码, 另一个是一组list表示的HTTP Header, 
  每个Header用一个包含两个str的tuple表示, 可以使用这个函数来发送HTTP响应的Header
function返回值将作为HTTP响应的Body发送给浏览器
"""


# 一个基本的 “Hello World” WSGI 应用
def wsgi_apl(environ, start_response):
    environ_text = "Hello Environ\n\n"
    for k, v in sorted(environ.items()):
        ele = str(k) + "=" + str(v)
        environ_text = environ_text + ele + "\n"
    start_response("200 OK", [("Content-Type", "text/plain; charset=utf-8")])
    return [environ_text.encode("utf-8")]


if __name__ == "__main__":
    # make_server所做的工作之一便是将HTTP请求报文解析为WSGI环境变量
    # 然后将这些环境变量传入wsgi_apl(WSGI应用程序函数), 即environ供用户使用
    with make_server("", 8000, wsgi_apl) as http_server:
        import webbrowser
        webbrowser.open('http://localhost:8000/xyz?abc')
        http_server.handle_request()   # 仅处理一次请求, 然后退出

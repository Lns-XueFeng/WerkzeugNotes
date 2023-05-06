from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple


def application_one(environ, start_response):
    request = Request(environ)
    text = f"<h1>Hello {request.args.get('name', 'Werkzeug')}!</h1>"
    response = Response(text, mimetype='text/html')
    return response(environ, start_response)


@Request.application
def application_two(request):
    text = f"<h1>Hello {request.args.get('name', 'Werkzeug')}!</h1>"
    response = Response(text, mimetype="text/html")
    return response


run_simple(
    "127.0.0.1",
    8000,
    application_one,
    use_reloader=True,
    use_debugger=True
)


# 仅列举了一些我个人觉得常用的
# 更多可以去看Werkzeug的源代码
def request_args_example(environ):
    request = Request(environ)
    url = request.url
    method = request.method
    path = request.path
    headers = request.headers
    args = request.args
    form = request.form
    cookies = request.cookies
    files = request.files


class Response(_SansIOResponse):
    def __init__(
            self,
            response=None,
            status=None,
            headers=None,
            mimetype=None,
            content_type=None,
            direct_passthrough=False,
    ):
        pass

# response: 响应的正文内容，可以是字符串、固定长度的字节、元组或字符串或字节列表响应，或任何其他字符串或字节的可迭代对象流式处理响应
# status: 响应的状态码，比如200为成功、304为重定向、404为禁止访问、500为服务器错误等
# headers: 一般不用......
# mimetype: 响应的返回类型，可以是text/plain、text/html、application/json等
# content_type: 响应的完整内容类型。如果设置的话便覆盖从mimetype构建的值
# direct_passthrough: 一般不用......
# 以上参数默认均为None

from werkzeug.wrappers import Response, Request


"""
Werkzeug是一个WSGI工具库, 它可以作为一个Web框架的底层库
它提供了用于操作WSGI环境变量和响应头的实用程序, 用于实现WSGI服务器的基类, 一个演示HTTP服务器, 
该服务器提供WSGI应用程序, 用于静态类型检查的类型以及验证工具, 该工具检查WSGI服务器和应用程序是否符合WSGI规范
它包括一个交互式调试器, 允许在浏览器中检查堆栈跟踪和源代码, 并为堆栈中的任何帧提供交互式解释器
"""


"""
通过Werkzeug你可以不必直接处理请求或者响应这些底层的东西, 它已经为你封装好了这些
请求数据需要环境对象, Werkzeug允许你以一个轻松的方式访问数据, 响应对象是一个WSGI应用, 提供了更好的方法来创建响应

另外提一嘴, Flask基于WSGI, Werkzeug, Jinja2, click提供了一个更为方便且安全的开发环境
使用Flask可以更为方便的构建大型的Web页面, 当然用Werkzeug亦可以构建

Click提供了命令行相关的工具
Jinja2是一个模板引擎, 它能让你在HTML中利用它预设的占位符来编写代码, 而后经其渲染成一个HTML文档

response(environ, start_response)调用了Response类的__call__方法
这个方法接受environ和start_response作为参数, 并使用它们来生成符合WSGI规范的HTTP响应
"""


def werk_apl(environ, start_response):
    request = Request(environ)   # 利用Request解析environ
    name = request.args.get("name", "Programmer")
    text = f"Hello {name}!"
    response = Response(text, mimetype="text/plain")   # 利用Response生成响应对象
    return response(environ, start_response)   # response回调产生符合WSGI规范的HTTP响应


if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("127.0.0.1", 8000, werk_apl)

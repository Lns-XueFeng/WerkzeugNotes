from werkzeug.wrappers import Request, Response
from werkzeug.serving import run_simple
from werkzeug.routing import Map, Rule


# 视图函数index
def index(environ, start_response):
    text = f"<h1>This is Index</h1>"
    response = Response(response=text, mimetype="text/html")
    return response(environ, start_response)


# 视图函数hello
def hello(environ, start_response):
    request = Request(environ)
    text = f"<h1>Hello {request.args.get('name', 'Werkzeug')}!</h1>"
    response = Response(response=text, mimetype="text/html")
    return response(environ, start_response)


# 视图函数say
def say(environ, start_response, name="Hello"):
    text = f"<h1>Say {name}</h1>"
    response = Response(response=text, mimetype="text/html")
    return response(environ, start_response)


# 分发函数, 找到请求路径对应的端点
def dispatch(environ, start_response):
    # 因为Map对象必须要知道前端传来的path
    # 所以需要调用bind_to_environ传入environ参数
    # 拿到对应path的MapAdapter对象
    urls = urls_map.bind_to_environ(environ)
    try:
        # 调用MapAdapter的match方法拿到endpoint和args
        # args会以字典形式存储转换器定义的名字为键，以具体传入的url中的参数为值
        # 比如如果访问http://127.0.0.1:8000/say/no, 那么args为{"name": "no"}
        endpoint, args = urls.match()
    except HTTPException as e:
        raise "urls match fail..."
    return endpoint, args


# 符合wsgi的应用程序
# 编写具体适用与每一个视图函数的调用逻辑
def wsgi_apl(environ, start_response):
    endpoint, args = dispatch(environ, start_response)
    if not args:
        return view_map[endpoint](environ, start_response)
    return view_map[endpoint](environ, start_response, name=args["name"])


# 构建url与endpoint的映射
urls_map = Map([
    Rule("/", endpoint="index", methods=['GET']),
    Rule("/hello", endpoint="hello", methods=['GET']),
    Rule("/say/<string:name>", endpoint="say", methods=['GET'])
])

# 构建endpoint与视图函数的映射
view_map = {
    "index": index,
    "hello": hello,
    "say": say
}

run_simple(
    "127.0.0.1",
    8000,
    wsgi_apl,
    use_reloader=True,
    use_debugger=True
)

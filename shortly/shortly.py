"""
版本：python3.9
预先配置好redis服务并启动, 而后安装第三方库, 最后启动shortly
"""

import os
import redis

from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.middleware.shared_data import SharedDataMiddleware
from werkzeug.utils import redirect
from jinja2 import Environment, FileSystemLoader

from utils import base36_encode, is_valid_url


class Shortly(object):

    def __init__(self, config):
        # 连接Redis
        self.redis = redis.Redis(config['redis_host'], config['redis_port'])
        # 渲染模板
        template_path = os.path.join(os.path.dirname(__file__), 'templates')
        self.jinja_env = Environment(loader=FileSystemLoader(template_path),
                                     autoescape=True)
        # 路由：通过路由匹配与解析URL
        self.url_map = Map([
            Rule('/', endpoint='new_url'),
            Rule('/<short_id>', endpoint='follow_short_link'),
            Rule('/<short_id>+', endpoint='short_link_details')
        ])

    def render_template(self, template_name, **context):
        """渲染模板 返回响应对象"""
        t = self.jinja_env.get_template(template_name)
        return Response(t.render(context), mimetype='text/html')

    def insert_url(self, url):
        """向数据库中插入url"""
        short_id = self.redis.get('reverse-url:' + url)
        if short_id is not None:
            return short_id
        url_num = self.redis.incr('last-url-id')
        short_id = base36_encode(url_num)
        self.redis.set('url-target:' + short_id, url)
        self.redis.set('reverse-url:' + url, short_id)
        return short_id

    def on_short_link_details(self, request, short_id):
        """视图函数"""
        link_target = self.redis.get('url-target:' + short_id)
        if link_target is None:
            raise NotFound()
        click_count = int(self.redis.get('click-count:' + short_id) or 0)
        return self.render_template('short_link_details.html',
                                    link_target=link_target,
                                    short_id=short_id,
                                    click_count=click_count
                                    )

    def on_follow_short_link(self, request, short_id):
        """视图函数"""
        link_target = self.redis.get('url-target:' + short_id)
        if link_target is None:
            raise NotFound()
        self.redis.incr('click-count:' + short_id)
        return redirect(link_target)

    def on_new_url(self, request):
        """视图函数"""
        error = None
        url = ''
        if request.method == 'POST':
            url = request.form['url']
            if not is_valid_url(url):
                error = 'Please enter a valid URL'
            else:
                short_id = self.insert_url(url)
                return redirect('/%s+' % short_id)
        return self.render_template('new_url.html', error=error, url=url)

    def dispatch_request(self, request):
        """将endpoint与视图函数绑定
        并试图启动得到经渲染的响应"""
        adapter = self.url_map.bind_to_environ(request.environ)
        try:
            # 得到当前请求的endpoint, values
            endpoint, values = adapter.match()
            # 启动相应的视图函数并返回其已渲染的响应
            return getattr(self, 'on_' + endpoint)(request, **values)
        except HTTPException as e:
            return e

    def wsgi_app(self, environ, start_response):
        """wsgi应用程序函数
        解析environ -> wsgi环境变量
        根据当前请求找到对应的视图函数并启动得到响应对象
        最后调用此对象返回HTTP响应报文
        """
        request = Request(environ)
        response = self.dispatch_request(request)
        return response(environ, start_response)

    def __call__(self, environ, start_response):
        return self.wsgi_app(environ, start_response)


def create_app(redis_host='localhost', redis_port=6379, with_static=True):
    shortly = Shortly({
        'redis_host': redis_host,
        'redis_port': redis_port
    })
    if with_static:
        shortly.wsgi_app = SharedDataMiddleware(shortly.wsgi_app, {
            '/static': os.path.join(os.path.dirname(__file__), 'static')
        })
    return shortly


if __name__ == '__main__':
    from werkzeug.serving import run_simple

    app = create_app()
    run_simple('127.0.0.1', 5000, app, use_debugger=True, use_reloader=True)

# 当一个请求来时
# 调用app实例, wsgi_app会启动
# Request会解析environ
# dispatch_request会匹配以及执行对应的视图函数并返回已渲染的响应对象
# response回调产生符合WSGI规范的HTTP响应
# 最后由server将响应传输给浏览器(client)

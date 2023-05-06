# 用来模拟HTTP请求的测试客户端
from werkzeug.test import Client
# 这个是Werkzeug提供的一个test_app用作示范
# 实际我们给自己的应用测试时传入自己的即可
from werkzeug.testapp import test_ap



# 建立对应app的模拟客户端
client = Client(test_app)
# 发起get请求并拿到响应对象
response = client.get("/")
# 拿取相应的属性
text = response.text
status = response.status
headers = response.headers

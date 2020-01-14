#-*-coding:utf-8 -*-
import tornado
import logging
from py_eureka_client import eureka_client
from tornado.options import define, options
from weather.controller.weatherController import WeatherHandle
from weather.resource.mylogging import Logging
app_name = 'SpiderService'

define("port", default=8085, help="run on the given port", type=int)
my_eureka_url = 'http://localhost:8761/eureka'
log = Logging('weatherTast.log',logging.ERROR,logging.DEBUG)

#启动eureka服务注册，提供查询服务
def weatherEurekaService():
    tornado.options.parse_command_line()
    log.info('开始向eureka服务器注册')
    # 注册eureka服务
    eureka_client.init_registry_client(my_eureka_url, app_name, instance_port=8085)
    # API服务接口
    log.info('创建服务controller接口')
    app = tornado.web.Application(handlers=[(r"/city/", WeatherHandle)])
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    # startScheduler()
    weatherEurekaService()
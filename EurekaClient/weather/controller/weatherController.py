#-*-coding:utf-8 -*-
from tornado.web import RequestHandler
import time
from weather.service.GaodeWeatherService import GaodeWeather

class TestHandle(RequestHandler):
    def get(self):
        name = self.get_argument("name", "kin")
        age = self.get_argument("age", "18")
        print("外部请求调用开始姓名:{},年龄:{}".format(name,age))
        time.sleep(10)
        print("休眠时间{}".format(10))
        self.write("hello world   welcome to you")

class WeatherHandle(RequestHandler):

    def get(self):
        cityid = self.get_argument('cityid')
        wea = GaodeWeather()
        res =wea.getGaodeWeatherFromRedis(cityid)
        self.write(res)



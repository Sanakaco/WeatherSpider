#-*-coding:utf-8 -*-
import urllib
import redis
from apscheduler.schedulers.blocking import BlockingScheduler
from py_eureka_client import eureka_client
from weather.resource.mylogging import Logging
from weather.service.GaodeWeatherService import GaodeWeather
import logging

my_eureka_url = 'http://localhost:8761/eureka'

class UpdataRedis:


    eureka_client.init_discovery_client(my_eureka_url)
    def __init__(self):
        self._pool = redis.ConnectionPool(host='node002',port=6379)
        self._redis = redis.Redis(connection_pool=self._pool)
        self._wea= GaodeWeather()
        self._log = Logging('apsTask.log',logging.ERROR,logging.DEBUG)
        self._appname = 'aspUpdataRedis'

    def __job(self):

        try:
            #调用服务内容
            citylist = eureka_client.do_service("cityservice","/citylist",return_type='json')
            for city in citylist:
                key = city['adcode']
                self._wea.getGaodeWeatherFromRedis(key)
                self._log.info("%s 刷新完成"% key)
        except urllib.request.HTTPError as e:
            self._log.info(e)

    def test(self):
        print('sad')

    def chedulerJob(self):
        sche = BlockingScheduler()
        sche.add_job(self.__job, 'interval', seconds=2)
        sche.start()

if __name__ == '__main__':
    up = UpdataRedis()
    up.chedulerJob()
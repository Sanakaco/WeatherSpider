#-*-coding:utf-8 -*-
import urllib.request
import json
import redis

WEATHER_API_URL = 'https://restapi.amap.com/v3/weather/weatherInfo?' \
                  'key=0f124fa5f31ac71f4444f35cbaacd8a5&extensions=all&city='
import logging
from weather.resource.mylogging import Logging
class GaodeWeather:

    def __init__(self):
        self._pool = redis.ConnectionPool(host ='node002', port = 6379)
        self._weaRedis = redis.Redis(connection_pool=self._pool)
        self._log = Logging('weatherAPI.log',logging.ERROR,logging.DEBUG)

    def __getGaodeWeatherDataFromUrl(self,cityid):
        url = WEATHER_API_URL + cityid
        response = urllib.request.urlopen(url)
        body = response.read()
        res = bytes.decode(body)
        return res

    def getGaodeWeatherFromRedis(self,cityid):
        result =self._weaRedis.get(cityid)
        if(result==None):
            self._log.info("%s 从网络获取"% cityid)
            result=self.__getGaodeWeatherDataFromUrl(cityid)
            self._log.info('%s 数据写入redis'% cityid)
            self.__setGaodeWeatherToRedis(cityid, result)
        self._log.info('%s 从redis返回'% cityid)
        return result

    def __setGaodeWeatherToRedis(self,cityid, obj):
        self._weaRedis.append(key=cityid,value=obj)

#测试
if __name__ == '__main__':
    id = '340506'
    wea = GaodeWeather()
    js = wea.getGaodeWeatherFromRedis(id)
    print(js)


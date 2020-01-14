import urllib.request
from bs4 import BeautifulSoup
import re
import json

# 获取天气的URL
from weather.entity.weather import *

weatherType_map = {'00':'晴', '01':'多云', '02':'阴', '03':'阵雨',
             '04': '雷阵雨','05':'雷阵雨并伴有冰雹','06':'雨夹雪','07':'小雨',
             '08':'中雨', '09':'大雨','10':'暴雨','11':'大暴雨',
             '12':'特大暴雨','13':'阵雪','14':'小雪','15':'中雪',
             '16':'大雪','17':'暴雪','18':'雾','19':'冻雨',
             '20':'沙尘暴','21':'小雨-中雨','22':'中雨-大雨','23':'大雨-暴雨',
             '24':'暴雨-大暴雨','25':'大暴雨-特大暴雨','26':'小雪-中雪','27':'中雪-大雪',
             '28':'大雪-暴雪','29':'浮尘','30':'扬沙','31':'强沙尘暴',
             '53':"霾",'99':"无",'32':"浓雾",'49':"强浓雾",'54':"中度霾",
             '55':"重度霾",'56':"严重霾",'57':"大雾",'58':"特强浓雾",
             '97':"雨",'98':"雪",'301':"雨",'302':"雪"}

windDir=["无持续风向","东北风","东风","东南风","南风","西南风","西风","西北风","北风","旋转风"]
windPower=["<3级","3-4级","4-5级","5-6级","6-7级","7-8级","8-9级","9-10级","10-11级","11-12级"]


WEATHER_SEVENDAY_URL = 'http://www.weather.com.cn/weathern/'
WEATHER_ONEDAY_URL = 'http://www.weather.com.cn/weather1dn/'

# 获取此时的天气信息,返回dom
def getNowBSoupByCityid(cityid):
    url= WEATHER_ONEDAY_URL+cityid+'.shtml'
    response = urllib.request.urlopen(url)
    domTree = response.read()
    bsObj = BeautifulSoup(domTree, 'lxml')
    return bsObj

#获取七天天气预告信息
def getSevenBSoupByCityid(cityid):
    url = WEATHER_SEVENDAY_URL+cityid+'.shtml'
    response = urllib.request.urlopen(url)
    domTree = response.read()
    bsObj = BeautifulSoup(domTree, 'lxml')
    return bsObj

#解析地理位置信息
def getAddress(now):
    area_list = now.find_all('div','areaSelect webox')
    area = now.find('div','webox areaSelect')
    provincial =''
    town = ''
    if(len(area_list)>1):
        provincial =area_list[0].find('a').text
        city = area_list[1].find('a').text
    else:
        city = area_list[0].find('a').text
    district = area.find('a').text
    return Address(provincial, city, district, town)

def getNowWeather(now):
    dom=now.find('div', 't')
    sk=dom.find('div','sk')
    uptime = sk.find('p', 'time').find('span').text
    now_tem = sk.find('div', 'tem').find('span').text
    humidity = sk.find('div', 'zs h').find('em').text
    air_coe = sk.find('a', '_blank').text
    clearfix=dom.find('ul', 'clearfix')

def getForecast7Day(bsoup):
    sky = bsoup.find_all()
    fore=[]
    for index in range(0,7):
        date= sky[index].find('h1').text
        type = sky[index].find('p','wea').text
        high_tem= sky[index].find('p','tem').find('span').text
        low_tem= sky[index].find('p','tem').find('i').text
        win_dir= sky[index].find('p','win').find('span')['title']
        win_power= sky[index].find('p','win').find('i').text
        fore.append(Forecast_7d(date, type, high_tem, low_tem, win_dir, win_power))
    return fore

def getForecast24h(now):
    wea_list = []
    char=now.find('div','todayRight').find('script').text
    hour= char.lstrip().split(';',1)
    str=hour[0].split('=')
    jsonStr=json.loads(str[1])
    for dict in jsonStr[0]:
        time = dict.get('jf')[8:10]
        type = weatherType_map.get(dict.get('ja'))
        tem = dict.get('jb')
        win_dir = windDir[int(dict.get('jd'))]
        win_power = windPower[int(dict.get('jc'))]
        wea_list.append(Forecast_24h(time, type, tem, win_dir, win_power))
    return wea_list


def getWeatherStruct(cityid):
    today = getNowBSoupByCityid(cityid)
    fore = getSevenBSoupByCityid(cityid)
    addr = getAddress(today)
    now = getNowWeather(today)
    fore_24h = getForecast24h(today)
    fore_7d = getForecast7Day(fore)
    res = Result(addr, now)
    res.forecast_7d = fore_7d
    res.forecast_24h = fore_24h
    wea = WeatherJson(100,'成功',res)
    return wea

if __name__ == '__main__':
    bs = getNowBSoupByCityid('101010100')
    wea = getForecast24h(bs)
    bs7 = getSevenBSoupByCityid('101010100')
    seven = getForecast7Day(bs7)
    for w in seven:
        print(w.__dict__)


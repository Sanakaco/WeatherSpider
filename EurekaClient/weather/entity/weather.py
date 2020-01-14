class Life_Coe:
    def __init__(self, dress,  wash, sport, spf):
        self.dress = dress
        self.wash = wash
        self.sport = sport
        self.spf = spf

#未来七天天气信息
class Forecast_7d (object):
    def __init__(self, date, type, high_tem, low_tem, win_dir, win_power):
        self.date = date
        self.type = type
        self.high_tem = high_tem
        self.low_tem = low_tem
        self.win_dir = win_dir
        self.win_power = win_power


#24小时天气预告信息 时间-天气-温度-风向-风力
class Forecast_24h:
    def __init__(self, time, type, tem, win_dir, win_power):
        self._time = time
        self._type = type
        self._tem = tem
        self._win_dir = win_dir
        self._win_power = win_power


#当天的天气信息
class Today:
    def __init__(self, uptime, type, now_tem, high_tem, low_tem, humidity, air_coe, warning):
        self._uptime = uptime
        self._type = type
        self._now_tem = now_tem
        self._high_tem = high_tem
        self._low_tem = low_tem
        self._humidity = humidity
        self._air_coe = air_coe
        self._warning = warning

#地理坐标，省-市-区-镇
class Address:
    def __init__(self, provincial, city, district,town):
        self._provincial = provincial
        self._city = city
        self._district = district
        self._town = town


#API返回json结构
class WeatherJson(object):
    def __init__(self, status, msg, result):
        self._status = status
        self._msg = msg
        self._result = result


#天气数据整体json结构
class Result:
    def __init__(self, addr, today):
        self._place = addr
        self._today = today
        self.forecast_24h = []
        self.forecast_7d = []

from datetime import date, datetime
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
import os
import random

today = datetime.now()
start_date = os.environ['START_DATE']
city = os.environ['CITY']
birthday = os.environ['BIRTHDAY']
birthday_02 = '03-17'


app_id = os.environ["APP_ID"]
app_secret = os.environ["APP_SECRET"]

user_id = os.environ["USER_ID"]
# user_id_02 = 'oXQhR6WI_labGe7SUni7Bd_HXmq8'

# template_id = os.environ["TEMPLATE_ID"] 	
# 女模板
template_id = 'zdASne5hOVn72cWPLh9zD8rYRm45rAdTCmfKkcBpAzE'
# 男模板02
template_id_02 = 'nlvEMEseCYVJ5ZhQ80M1RTwUdV2_4I3kys-FTc7zsPg'


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp']),weather['airQuality'],math.floor(weather['low']),math.floor(weather['high'])

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  print(delta)
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  print((next - today).days)
  return (next - today).days
def get_birthday_02():
  next = datetime.strptime(str(date.today().year) + "-" + birthday_02, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  print((next - today).days)
  return (next - today).days

def get_words():
  words = requests.get("https://api.shadiao.pro/chp")
  if words.status_code != 200:
    return get_words()
  print(words.json()['data']['text'])
  return words.json()['data']['text']

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature,airquality, low, high = get_weather()
data = {"weather":{"value":wea},"airquality":{"value":airquality},"low":{"value":low},"high":{"value":high},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
data_02 = {"weather":{"value":wea},"airquality":{"value":airquality},"low":{"value":low},"high":{"value":high},"temperature":{"value":temperature},"love_days":{"value":get_count()},"birthday_left":{"value":get_birthday_02()},"words":{"value":get_words(), "color":get_random_color()}}

res = wm.send_template(user_id, template_id, data)
# 测试模板02
# res = wm.send_template(user_id, template_id_02, data_02)

print(res)
res02 = wm.send_template(user_id_02, template_id_02, data_2)
print(res02)

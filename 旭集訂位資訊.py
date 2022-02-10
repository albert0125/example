from calendar import c
from distutils.command.config import config
from math import fabs
from ssl import VerifyFlags
import requests
import json
import sys
from bs4 import BeautifulSoup
import datetime

def get_info():
    now = datetime.datetime.now()
    now = now + datetime.timedelta(days=1)
    today_str = now.strftime("%Y-%m-%d")
    proxies = {'http': 'http://localhost:9090', 'https': 'http://localhost:9090'}

    first_url = "https://www.feastogether.com.tw/booking/10"
    target_url = "https://www.feastogether.com.tw/orderAPI/otGetPossible"
    payload = {"bu_code":"res10","city":"9","people":"3","date":today_str,"meal_time":"dinner"}
    my_headers = {'Accept': 'text/plain, */*; q=0.01', 'Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:96.0) Gecko/20100101 Firefox/96.0','X-Requested-With':'XMLHttpRequest'}
    ses = requests.Session()
    ses.headers.update(my_headers)
    res = ses.get(first_url, headers=my_headers, timeout=60,proxies=proxies,verify=False)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text,"lxml")
    csrf_token = soup.find("meta", {"name":"csrf-token"})["content"]
    print(csrf_token)
    my_headers["x-csrf-token"] = csrf_token
    chk_result = []
    print(payload)
    target_res  = ses.post(target_url, data = payload, headers=my_headers,proxies=proxies,verify=False )
    target_res.encoding = 'utf-8'
    has_seat(target_res.text,chk_result)
    
    payload["meal_time"] = "lunch"
    print(payload)
    target_res  = ses.post(target_url, data = payload, headers=my_headers,proxies=proxies,verify=False )
    target_res.encoding = 'utf-8'
    has_seat(target_res.text,chk_result)

    if len(chk_result)>0:
        print(chk_result)
    else:
        print("NO seat!")

def has_seat(str,chk_result):
    mealtime = ""
    j = json.loads(str)
    if "res10" in j and len(j["res10"])>0 and "content" in (j["res10"][0]) and len(j["res10"][0]["content"])>0:
        mealtime = j["res10"][0]["mealTime"]
        calendars = j["res10"][0]["content"][0]["calendar"]
        print("mealtime:{},calendars:{}".format(mealtime, calendars))
        for key in calendars:
            if calendars[key]>0:
                msg = "HAS SEAT:{} at {} for {}".format(calendars[key], key, mealtime)
                chk_result.append(msg)
    

if __name__ == "__main__":
    get_info()

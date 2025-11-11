#!/usr/bin/python3
# -- coding: utf-8 -- 
# -------------------------------
# @Author : github@wd210010 https://github.com/wd210010/just_for_happy
# @Time : 2023/2/27 13:23
# -------------------------------
"""
cron: "1 8 * * *"
new Env('一点万象签到');
"""
import requests
import time
import hashlib
import random
import json
import os
from notify import send

# 登录后搜索 https://app.mixcapp.com/mixc/gateway 域名随意一个 请求体里面的deviceParams，token 多账号填多个单引号里面 用英文逗号隔开
# 青龙变量 ydwx_deviceParams ydwx_token
# ydwx_deviceParams = os.getenv("ydwx_deviceParams").split('&')
# ydwx_token = os.getenv("ydwx_token").split('&')

# 2025-01-14
# 7553
# 9553
ydwx_deviceParams=[
    "eyJwaG9uZSI6IjE4OTA4Njg3NTUzIiwiZGV2aWNlIjoiaVBob25lMTUsNCIsImRldmljZUlkIjoiQkdXS1JvcHk5c1cxUkl6anhoNUdESjhCcDJpRE54bzI0YU5SWEdmUHBobkNnWEtLM1gyRlwvNk50V2ViSlFqeUcrZGc1V0VnWWhZazdsQTVCclB1VWtDdz09IiwibG9jYXRpb24iOnsiZ3BzTG9uZ2l0dWRlIjoiMTE0LjIwMDEiLCJncHNMYXRpdHVkZSI6IjMwLjU1MDMifSwiZGV2aWNlTmFtZSI6ImlQaG9uZSJ9",
    "eyJwaG9uZSI6IjE4Njc0MDA5ODY4IiwiZGV2aWNlIjoiaVBob25lMTYsMSIsImRldmljZUlkIjoiQkFcL2U5em13cXpvdng4WkJJZHJzMVpFMWh5eE9EUm1PM2txSFRnSFNNdldRVlB1T0l3S0pGQlltTVwvWng5NFwvNzNjUmxDdHBCc0xzS3hrWnBCeHVjTlwvUT09IiwibG9jYXRpb24iOnsiZ3BzTG9uZ2l0dWRlIjoiMTE0LjIwMDEiLCJncHNMYXRpdHVkZSI6IjMwLjU1MDMifSwiZGV2aWNlTmFtZSI6ImlQaG9uZSJ9"
]
ydwx_token=[
    "7f0e71b32c29464aa8666f9db6087474",
    "eb50fb3c16fb4a9fa389308744343c9b"
]



print(f'共配置了{len(ydwx_deviceParams)}个账号')
log = []
lastMsg = "err";
for i in range(len(ydwx_deviceParams)):
    print(f'*****第{str(i+1)}个账号*****')
    rand = random.randint(25,120)
    time.sleep(rand)
    timestamp = str(int(round(time.time() * 1000)))
    md5 = hashlib.md5()
    sig = f'action=mixc.app.memberSign.sign&apiVersion=1.0&appId=68a91a5bac6a4f3e91bf4b42856785c6&appVersion=3.53.0&deviceParams={ydwx_deviceParams[i]}&imei=2333&mallNo=20014&osVersion=12.0.1&params=eyJtYWxsTm8iOiIyMDAxNCJ9&platform=h5&timestamp={timestamp}&token={ydwx_token[i]}&P@Gkbu0shTNHjhM!7F'
    md5.update(sig.encode('utf-8'))
    sign = md5.hexdigest()
    url = 'https://app.mixcapp.com/mixc/gateway'
    headers = {
        'Host': 'app.mixcapp.com',
        'Connection': 'keep-alive',
        'Content-Length': '564',
        'Accept': 'application/json, text/plain, */*',
        'Origin': 'https://app.mixcapp.com',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCAM00 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36/MIXCAPP/3.42.2/AnalysysAgent/Hybrid',
        'Sec-Fetch-Mode': 'cors',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'com.crland.mixc',
        'Sec-Fetch-Site': 'same-origin',
        'Referer': 'https://app.mixcapp.com/m/m-20014/signIn?showWebNavigation=true&timestamp=1676906528979&appVersion=3.53.0&mallNo=20014',
        'Accept-Encoding': 'gzip, deflate',
        #'Cookie':'FZ_STROAGE.mixcapp.com=eyJTRUVTSU9OSUQiOiJmNjMzMzNlOGIxZjQ1OWM1IiwiU0VFU0lPTkRBVEUiOjE3MzY4NDQzNTg2MzcsIkFOU0FQUElEIjoiMTFmODI1MzA1NTZjY2VjNiIsIkFOUyRERUJVRyI6MCwiQU5TVVBMT0FEVVJMIjoiaHR0cHM6Ly9kYXRhcy5taXhjYXBwLmNvbS8iLCJGUklTVERBWSI6IjIwMjUwMTE0IiwiRlJJU1RJTUUiOnRydWUsIkFSS19JRCI6IkpTMjA2ZmI5YmQ0Mjc4ODE0NjJjYjIxNTc0MDQ3NGVjZmMyMDZmIn0%3D; .thumbcache_ec7e32560cc6466cbfc6c2019b9bdce8=elry34CLKSMG0jXFfMw1i44YO7HuPheYFbm754UIE8C6dvuL51/0ybodbzD+dENHlUchaPefrSGfpF6Vt94j9Q%3D%3D; ARK_ID=JS206fb9bd427881462cb215740474ecfc206f; smidV2=20250114163312c812ca41da2f16a4ef75d31fceffbeeb005142c5a6ee32f50; acw_tc=2f6a1fc817368434984781269eeb9985663878edb7c84ead337009bb6c8d3e',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
    }
    # data = f'mallNo=20028&appId=68a91a5bac6a4f3e91bf4b42856785c6&platform=h5&imei=E94B93FA-F46A-4B72-9AA2-626D2BBB6908&appVersion=3.64.0&osVersion=17.4&action=mixc.app.memberSign.sign&apiVersion=1.0&timestamp={timestamp}&deviceParams={ydwx_deviceParams[i]}&token={ydwx_token[i]}&params=eyJtYWxsTm8iOiIyMDAyOCJ9&sign={sign}'
    data = f'mallNo=20014&appId=68a91a5bac6a4f3e91bf4b42856785c6&platform=h5&imei=2333&appVersion=3.53.0&osVersion=12.0.1&action=mixc.app.memberSign.sign&apiVersion=1.0&timestamp={timestamp}&deviceParams={ydwx_deviceParams[i]}&token={ydwx_token[i]}&params=eyJtYWxsTm8iOiIyMDAxNCJ9&sign={sign}'
    html = requests.post(url=url, headers=headers, data=data)
    result = f'帐号{i+1}签到结果:' + json.loads(html.text)['message']
    lastMsg = json.loads(html.text)['message']
    print(json.loads(html.text))
    log.append(result)

log2 = '\n'.join(log)
send('一点万象'+lastMsg, log2)
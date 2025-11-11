#!/usr/bin/python3
# -- coding: utf-8 --
# -------------------------------
# @Author : github@wd210010 https://github.com/wd210010/only_for_happly
# @Time : 2024/05/321 9:23
# -------------------------------
"""
cron: "15 8 * * *"
new Env('999会员中心');
"""
import requests
import time
import json
import random
import os
import ssl
import urllib3
from datetime import datetime

# ==================== SSL 绕过设置 ====================
# 禁用 SSL 验证
ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 创建不验证 SSL 的 session
session = requests.Session()
session.verify = False

# 替换默认的 requests 方法
def create_ssl_disabled_session():
    session = requests.Session()
    session.verify = False
    return session

# 使用自定义 session
requests.Session = create_ssl_disabled_session

# 重写 requests 的请求方法
original_request = requests.request
original_get = requests.get
original_post = requests.post

def patched_request(method, url, **kwargs):
    kwargs.setdefault('verify', False)
    return original_request(method, url, **kwargs)

def patched_get(url, **kwargs):
    kwargs.setdefault('verify', False)
    return original_get(url, **kwargs)

def patched_post(url, **kwargs):
    kwargs.setdefault('verify', False)
    return original_post(url, **kwargs)

requests.request = patched_request
requests.get = patched_get
requests.post = patched_post
# ==================== SSL 绕过设置结束 ====================

# 导入sendNotify函数
from notify import send

# 注册登录后抓mc.999.com.cn域名请求头里面的Authorization 变量名为jjjck 多号用#分割
#export jjjck='807b3cc1-3473-4baa-b038-********'
lastMsg = "err"
# jjck = os.getenv("jjjck").split('#')
jjck = 'c6fe6f1e-555d-4b15-b388-a220d177aa22'.split('#')

today = datetime.now().date().strftime('%Y-%m-%d')

for i in range(len(jjck)):
    Authorization = jjck[i]
    headers = {
        "Host": "mc.999.com.cn",
        "Connection": "keep-alive",
        "locale": "zh_CN",
        "Authorization": Authorization,
        "content-type": "application/json",
        "Accept-Encoding": "gzip,compress,br,deflate",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_4_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x18003030) NetType/WIFI Language/zh_CN"
    }

    # rand = random.randint(30,120)
    # time.sleep(rand)

    try:
        resp = session.get('https://mc.999.com.cn/zanmall_diy/ma/personal/point/pointInfo', headers=headers)
        totalpoints = json.loads(resp.text)['data']
        lastMsg = totalpoints;
        print(f'当前拥有总积分:{totalpoints}')
        send(f"999会员", totalpoints)
    except Exception as e:
        print(f'获取总积分失败：{str(e)}')
        send("999", "失败")
        continue

    print('*'*30)
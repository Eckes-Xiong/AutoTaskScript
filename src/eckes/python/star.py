
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
注册链接：http://dd.liangdongkj.cn/index/user/register
环境变量：
    XYD = "账号1#密码1&账号2#密码2"
    READ_TIMES = 60       # 每轮阅读次数（默认60）
    PAUSE_MINUTES = 5     # 每轮后暂停分钟数（默认5）
"""

import os
import sys
import requests
import re
import json
import time

# ==================== 配置区 ====================
BASE_URL = "http://dd.liangdongkj.cn"
LOGIN_PAGE = "/index/user/login.html"
READ_PAGE = "/index/index/read.html"
SETTLE_URL = "/index/index/settleRead"
USER_CENTER = "/index/user/index.html"

# 会员等级配置（名称、所需金币、时长）
MEMBERSHIP_LEVELS = [
    {"name": "青铜会员", "coins": 138, "duration": "30天"},
    {"name": "黄金会员", "coins": 388, "duration": "120天"},
    {"name": "钻石会员", "coins": 888, "duration": "360天"},
]

# 获取登录页用的请求头（普通浏览器）
PAGE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": BASE_URL + "/index/user/index.html",
}

# 登录请求用的请求头（模拟 AJAX）
LOGIN_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
    "Referer": BASE_URL + LOGIN_PAGE,
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
}

# 阅读页面请求头（模拟浏览器）
READ_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/149.0.0.0 Safari/537.36 Edg/149.0.0.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "Referer": BASE_URL + READ_PAGE,
}
# ================================================

def get_token_and_cookie(session):
    """获取登录页面的 token"""
    try:
        resp = session.get(BASE_URL + LOGIN_PAGE, headers=PAGE_HEADERS, timeout=10)
        resp.encoding = 'utf-8'
        if resp.status_code != 200:
            print(f"❌ 获取登录页失败，状态码: {resp.status_code}")
            return None

        html = resp.text
        patterns = [
            r'id="globalToken"[^>]*value="([^"]+)"',
            r'name="__token__"[^>]*value="([^"]+)"',
            r'value="([^"]+)"\s+id="globalToken"',
            r'value="([^"]+)"\s+name="__token__"',
            r'__token__\s*value="([^"]+)"',
        ]
        token = None
        for pat in patterns:
            match = re.search(pat, html)
            if match:
                token = match.group(1)
                break
        if token:
            print(f"✅ 获取到 token: {token}")
            return token
        else:
            print("❌ 未找到 token，可能页面结构已变化。")
            lines = html.split('\n')
            found_lines = [line for line in lines if 'globalToken' in line or '__token__' in line]
            if found_lines:
                print("📄 包含 token 的行：")
                for line in found_lines[:3]:
                    print(line.strip())
            else:
                print("📄 页面中完全没有 globalToken 或 __token__ 关键字。")
                print("📄 页面开头 2000 字符：")
                print(html[:2000])
            return None
    except Exception as e:
        print(f"❌ 请求登录页异常: {e}")
        return None

def login(account, password):
    """执行登录，成功返回 session，失败返回 None"""
    session = requests.Session()
    token = get_token_and_cookie(session)
    if not token:
        return None

    data = {
        "account": account,
        "password": password,
        "__token__": token,
    }

    try:
        resp = session.post(
            BASE_URL + LOGIN_PAGE,
            headers=LOGIN_HEADERS,
            data=data,
            timeout=10
        )
        resp.encoding = 'utf-8'
        try:
            result = resp.json()
        except json.JSONDecodeError:
            print("❌ 登录响应不是 JSON，可能被重定向或需要验证码。")
            return None

        if result.get('code') == 1:
            print(f"✅ 账号 {account} 登录成功：{result.get('msg', '')}")
            return session
        else:
            print(f"❌ 登录失败：{result.get('msg', '未知错误')}")
            return None
    except Exception as e:
        print(f"❌ 登录请求异常: {e}")
        return None

# ==================== 收益 & 会员信息模块 ====================

def get_user_info(session):
    """从个人中心页面提取用户名、余额、金币、团队人数"""
    try:
        resp = session.get(BASE_URL + USER_CENTER, headers=PAGE_HEADERS, timeout=10)
        resp.encoding = 'utf-8'
        if resp.status_code != 200:
            print(f"❌ 获取个人中心失败，状态码: {resp.status_code}")
            return None

        html = resp.text
        balance = re.search(r'<div class="menutopc">\s*<div class="menutopvalue">([\d.]+)</div>\s*<div class="menubottomtext">我的余额</div>', html)
        coins = re.search(r'<div class="menutopc">\s*<div class="menutopvalue">([\d.]+)</div>\s*<div class="menubottomtext">我的金币</div>', html)
        team = re.search(r'<div class="menutopc">\s*<div class="menutopvalue">([\d.]+)</div>\s*<div class="menubottomtext">团队人数</div>', html)
        username_match = re.search(r'id="username"\s+value="([^"]+)"', html)

        info = {
            'username': username_match.group(1) if username_match else '未知',
            'balance': balance.group(1) if balance else 'N/A',
            'coins': coins.group(1) if coins else 'N/A',
            'team': team.group(1) if team else 'N/A',
        }
        return info
    except Exception as e:
        print(f"❌ 获取用户信息异常: {e}")
        return None

def print_user_info(info, prefix=""):
    """打印用户收益信息"""
    if not info:
        print("⚠️ 无法获取用户信息")
        return
    print(f"{prefix} 用户名：{info.get('username', '未知')}")
    print(f"{prefix} 💰 余额：{info.get('balance', 'N/A')} 元")
    print(f"{prefix} 🪙 金币：{info.get('coins', 'N/A')}")
    print(f"{prefix} 👥 团队人数：{info.get('team', 'N/A')}")

def show_membership_gap(balance_str, prefix=""):
    """根据余额（元）折算金币，计算会员差距"""
    try:
        balance = float(balance_str)
    except (ValueError, TypeError):
        print(f"{prefix} ⚠️ 当前余额无效，无法计算会员差距")
        return

    print(f"{prefix} 📊 会员等级差距（按1元=1金币折算，当前余额：{balance}元）：")
    for level in MEMBERSHIP_LEVELS:
        need = level["coins"] - balance
        if need <= 0:
            status = "✅ 可开通"
        else:
            status = f"还差 {need:.2f} 金币"
        print(f"{prefix}   • {level['name']}（{level['duration']}）需 {level['coins']} 金币 → {status}")

# ==================== 阅读任务模块 ====================

def read_one_article(session, timeout=15):
    """执行一次完整的阅读任务，返回 (success, msg)"""
    try:
        resp = session.get(BASE_URL + READ_PAGE, headers=READ_HEADERS, timeout=10)
        resp.encoding = 'utf-8'
        if resp.status_code != 200:
            return False, f"获取阅读页失败，状态码 {resp.status_code}"

        html = resp.text
        url_match = re.search(r"var articleUrl\s*=\s*'([^']+)'", html)
        index_match = re.search(r'id="currentIndex"\s+value="([^"]+)"', html)
        if not url_match or not index_match:
            url_match = re.search(r'articleUrl\s*=\s*"([^"]+)"', html)
            index_match = re.search(r'currentIndex[^"]+"([^"]+)"', html)
            if not url_match or not index_match:
                return False, "未找到文章URL或索引，可能页面已无任务"

        article_url = url_match.group(1)
        current_index = index_match.group(1)
        print(f"📖 当前文章：{article_url}，索引：{current_index}")

        print(f"⏳ 等待 {timeout} 秒模拟阅读...")
        time.sleep(timeout)

        settle_data = {"article_url": article_url, "index": current_index}
        resp_settle = session.post(
            BASE_URL + SETTLE_URL,
            headers=LOGIN_HEADERS,
            data=settle_data,
            timeout=10
        )
        resp_settle.encoding = 'utf-8'
        try:
            result = resp_settle.json()
        except json.JSONDecodeError:
            return False, f"结算响应非 JSON：{resp_settle.text[:100]}"

        if result.get('code') == 1:
            return True, result.get('msg', '结算成功')
        else:
            return False, result.get('msg', '结算失败，未知错误')
    except Exception as e:
        return False, f"阅读任务异常：{e}"

def do_read_loop(session, per_round=60, pause_minutes=5):
    """
    无限循环阅读任务，每 per_round 次后暂停 pause_minutes 分钟
    若遇到“无任务”错误则退出循环
    """
    total_success = 0
    round_count = 0

    while True:
        round_count += 1
        print(f"\n{'='*40}")
        print(f"🔄 第 {round_count} 轮阅读开始（每轮 {per_round} 次）")
        print('='*40)

        success_in_round = 0
        for i in range(1, per_round + 1):
            print(f"\n--- 第 {i}/{per_round} 次阅读 ---")
            ok, msg = read_one_article(session)
            if ok:
                success_in_round += 1
                total_success += 1
                print(f"✅ {msg}")
            else:
                print(f"❌ {msg}")
                # 如果无任务可读，则退出整个循环
                if "未找到文章" in msg or "已无任务" in msg:
                    print("⚠️ 当日任务已完成或无更多文章，退出阅读循环。")
                    return total_success
                # 其他错误（网络等）可继续尝试，不中断本轮
                # 但为避免死循环，加个小延时
                time.sleep(3)

        # 本轮结束，显示本轮收益情况
        print(f"\n📊 本轮成功阅读 {success_in_round} 篇文章，累计成功 {total_success} 篇。")
        # 显示最新收益
        info = get_user_info(session)
        if info:
            print("\n📊 当前收益状态：")
            print_user_info(info, "  ")
            show_membership_gap(info.get('balance', '0'), "  ")
        else:
            print("⚠️ 无法获取最新收益")

        # 暂停
        print(f"\n⏸️  已达到每轮 {per_round} 次，暂停 {pause_minutes} 分钟后继续...")
        for remaining in range(int(pause_minutes * 60), 0, -1):
            if remaining % 60 == 0:
                print(f"  剩余 {remaining//60} 分钟")
            time.sleep(1)
        print("✅ 暂停结束，开始下一轮阅读")

# ==================== 主函数 ====================

def parse_accounts(env_var):
    accounts = []
    if not env_var:
        return accounts
    for item in env_var.split('&'):
        if '#' in item:
            parts = item.split('#', 1)
            if len(parts) == 2:
                accounts.append((parts[0].strip(), parts[1].strip()))
    return accounts

def main():
    xyd_env = "eckes#q123456"
    if not xyd_env:
        print("❌ 未找到环境变量 XYD")
        sys.exit(1)

    accounts = parse_accounts(xyd_env)
    if not accounts:
        print("❌ 环境变量格式错误，正确格式：账号1#密码1&账号2#密码2")
        sys.exit(1)

    # 读取配置
    try:
        per_round = int(os.getenv('READ_TIMES', '60'))
    except:
        per_round = 60
    try:
        pause_minutes = int(os.getenv('PAUSE_MINUTES', '5'))
    except:
        pause_minutes = 5

    print(f"📋 共发现 {len(accounts)} 个账号，每轮阅读 {per_round} 次，每轮后暂停 {pause_minutes} 分钟")

    for idx, (acc, pwd) in enumerate(accounts, 1):
        print(f"\n{'='*60}")
        print(f"🔐 正在处理账号 {idx}: {acc}")
        session = login(acc, pwd)
        if not session:
            print(f"❌ 账号 {acc} 登录失败，跳过")
            continue

        # 登录后显示收益
        print("\n📊 登录后当前收益：")
        info = get_user_info(session)
        if info:
            print_user_info(info, "  ")
            show_membership_gap(info.get('balance', '0'), "  ")
        else:
            print("  ⚠️ 无法获取收益信息")

        # 启动循环阅读
        total_done = do_read_loop(session, per_round, pause_minutes)
        print(f"\n✅ 账号 {acc} 的阅读循环已结束，共成功阅读 {total_done} 篇。")

    print("\n🎉 所有账号处理完毕！")

if __name__ == "__main__":
    main()
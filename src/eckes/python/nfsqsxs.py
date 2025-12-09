# 当前脚本来自于 http://script.345yun.cn 脚本库下载！
# 脚本库官方QQ群: 429274456
# 脚本库中的所有脚本文件均来自热心网友上传和互联网收集。
# 脚本库仅提供文件上传和下载服务，不提供脚本文件的审核。
# 您在使用脚本库下载的脚本时自行检查判断风险。
# 所涉及到的 账号安全、数据泄露、设备故障、软件违规封禁、财产损失等问题及法律风险，与脚本库无关！均由开发者、上传者、使用者自行承担。

import os
import sys
import time
import random
import json
import requests
from datetime import datetime
from urllib.parse import quote


# 青龙推送模块
class QLNotifier:
    @staticmethod
    def send(title: str, content: str):
        try:
            from notify import send as ql_send

            ql_send(title, content)
            print(f"✅ 青龙通知发送成功: {title}")
        except ImportError:
            print(f"📢 {title}")
            print(f"📝 {content}")
        except Exception as e:
            print(f"❌ 发送通知异常: {str(e)}")


BASE_URL = "https://sxs-consumer.nfsq.com.cn"
LOTTERY_API = "/geement.marketinglottery/api/v1/marketinglottery"
RECEIVE_API = "/geement.actjextra/api/v1/act/win/goods/160goods/receive"


TASK_LIST_API = "/geement.marketingplay/api/v1/task"
TASK_JOIN_API = "/geement.marketingplay/api/v1/task/join"
ACT_CHECK_API = "/geement.actjextra/api/v1/act/check"
LOTTERY_COUNT_API = "/geement.actjextra/api/v1/act/lottery/data/todaycount"
WIN_LIST_API = "/geement.actjextra/api/v1/act/win/goods/simple"


SCENE_CODE_1 = "SCENE-2510301508361"
SCENE_CODE_2 = "SCENE-2510301509021"
GROUP_ID = "2510301511011"
ACT_CODE = "ACT2510301507191"
ACT_CODE_2 = "ACT2510301505581"

USER_AGENTS = [
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.42(0x18002a2d) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.43(0x18002b2f) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.38(0x18002626) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 16_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.41(0x18002929) NetType/5G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 13; SM-G9980 Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.42.2480(0x28002A37) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 12; Mi 12 Build/SKQ1.211006.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.40.2420(0x28002829) NetType/4G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 11; HUAWEI P50 Build/HUAWEIANA-AN00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.39.2340(0x28002739) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 14; OPPO Find X6 Pro Build/TP1A.220905.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.43.2501(0x28002B45) NetType/5G Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 13; vivo X90 Pro+ Build/TP1A.220624.014) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.41.2400(0x28002929) NetType/WIFI Language/zh_CN",
    "Mozilla/5.0 (Linux; Android 12; OnePlus 11 Build/SKQ1.221119.001) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/116.0.0.0 Mobile Safari/537.36 MicroMessenger/8.0.38.2340(0x28002626) NetType/4G Language/zh_CN",
]


def parse_custom_locations(location_str):

    if not location_str:
        return []

    locations = []

    lines = location_str.replace("@", "\n").strip().split("\n")

    for line in lines:
        line = line.strip()
        if not line:
            continue

        parts = line.split(",")
        if len(parts) >= 5:
            try:
                lng = float(parts[0].strip())
                lat = float(parts[1].strip())
                province = parts[2].strip()
                city = parts[3].strip()
                area = parts[4].strip()

                locations.append(
                    {
                        "province": province,
                        "city": city,
                        "area": area,
                        "lng_range": (lng - 0.01, lng + 0.01),
                        "lat_range": (lat - 0.01, lat + 0.01),
                    }
                )
            except:
                pass

    return locations


CHINA_CITIES = [
    {
        "province": "湖北省",
        "city": "武汉市",
        "area": "武昌区",
        "lng_range": (114.20, 114.50),
        "lat_range": (30.50, 30.70),
    },
    {
        "province": "湖北省",
        "city": "武汉市",
        "area": "江汉区",
        "lng_range": (114.25, 114.35),
        "lat_range": (30.58, 30.68),
    },
    {
        "province": "湖北省",
        "city": "武汉市",
        "area": "汉阳区",
        "lng_range": (114.21, 114.22),
        "lat_range": (30.55, 30.58),
    },
]


class NongFuShanQuan:
    def __init__(self, unique_identity, apitoken, custom_locations=None):
        self.unique_identity = unique_identity
        self.apitoken = apitoken
        self.session = requests.Session()
        self.log_ids = []
        self.first_prize_count = 0
        self.completed_tasks = 0
        self.task_rewards = 0
        self.prize_list = []
        self.user_agent = random.choice(USER_AGENTS)
        self.custom_locations = custom_locations or []

    def get_headers(self, content_type="application/json"):

        return {
            "unique_identity": self.unique_identity,
            "apitoken": self.apitoken,
            "User-Agent": self.user_agent,
            "Content-Type": content_type,
            "Accept": "*/*",
            "Referer": "https://servicewechat.com/",
        }

    def log(self, msg):

        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {msg}")

    def check_activity(self):

        url = f"{BASE_URL}{ACT_CHECK_API}?act_code={ACT_CODE}"

        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            result = response.json()

            if result.get("success"):
                data = result.get("data", {})
                max_count = data.get("user_max_scan_count_perday", 0)
                self.log(f"✅ 活动进行中, 每日基础次数: {max_count}")
                return max_count
            else:
                self.log(f"❌ 活动检查失败: {result.get('msg')}")
                return 0

        except Exception as e:
            self.log(f"❌ 活动检查异常: {str(e)}")
            return 0

    def get_today_lottery_count(self):

        url = f"{BASE_URL}{LOTTERY_COUNT_API}?act_code={ACT_CODE}"

        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            result = response.json()

            if result.get("success"):
                used_count = result.get("data", 0)
                self.log(f"✅ 基础已使用: {used_count}次")
                return used_count
            else:
                self.log(f"❌ 查询今日抽奖次数失败: {result.get('msg')}")
                return 0

        except Exception as e:
            self.log(f"❌ 查询今日抽奖次数异常: {str(e)}")
            return 0

    def get_task_list(self):

        url = f"{BASE_URL}{TASK_LIST_API}?pageNum=1&pageSize=10&task_status=2&status=1&group_id={GROUP_ID}&is_db=1"

        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            result = response.json()

            if result.get("success"):
                tasks = result.get("data", [])
                self.log(f"✅ 获取任务: {len(tasks)}个")
                return tasks
            else:
                self.log(f"❌ 获取任务列表失败: {result.get('msg')}")
                return []

        except Exception as e:
            self.log(f"❌ 获取任务列表异常: {str(e)}")
            return []

    def join_task(self, task_id, task_name):

        action_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        action_time_encoded = quote(action_time)
        url = f"{BASE_URL}{TASK_JOIN_API}?action_time={action_time_encoded}&task_id={task_id}"

        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            result = response.json()

            if result.get("success"):
                self.log(f"  ✅ 任务完成: {task_name}")
                data = result.get("data", {})
                if isinstance(data, dict):
                    reward_count = data.get("reward_count", 0)
                    if reward_count > 0:
                        self.log(f"  🎁 获得 {reward_count} 次抽奖机会")
                        self.task_rewards += reward_count
                return True
            else:
                msg = result.get("msg", "未知错误")
                if "已完成" in msg or "已参与" in msg:
                    self.log(f"  ℹ️ {task_name}: {msg}")
                else:
                    self.log(f"  ❌ {task_name} 失败: {msg}")
                return False

        except Exception as e:
            self.log(f"  ❌ {task_name} 异常: {str(e)}")
            return False

    def do_all_tasks(self):

        self.log(f"📋 阶段1: 执行任务")

        max_count = self.check_activity()
        if max_count == 0:
            self.log("⚠️ 活动状态异常，跳过任务执行")
            return max_count

        time.sleep(2)

        tasks = self.get_task_list()

        if not tasks:
            self.log("⚠️ 没有可执行的任务")
            return max_count

        self.log(f"🎯 任务总数: {len(tasks)}")

        for task in tasks:
            task_id = task.get("id")
            task_name = task.get("name", "未知任务")
            complete_status = task.get("complete_status", 0)
            complete_count = task.get("complete_count", 0)
            allow_complete_count = task.get("allow_complete_count", 1)

            if complete_status == 0 and complete_count < allow_complete_count:
                self.log(f"▶️ {task_name}...")
                if self.join_task(task_id, task_name):
                    self.completed_tasks += 1
                    self.log(f"  ✅ 完成")

                time.sleep(random.uniform(2, 4))

        if self.completed_tasks > 0:
            self.log(
                f"✅ 完成任务: {self.completed_tasks}个, 增加抽奖次数: +{self.completed_tasks}"
            )
        return max_count

    def generate_random_location(self, use_winning=False):

        if self.custom_locations:
            city_data = random.choice(self.custom_locations)
            self.log(f"📍 使用自定义位置: {city_data['province']} {city_data['city']}")
        else:
            city_data = random.choice(CHINA_CITIES)
        longitude = round(
            random.uniform(city_data["lng_range"][0], city_data["lng_range"][1]), 14
        )
        latitude = round(
            random.uniform(city_data["lat_range"][0], city_data["lat_range"][1]), 14
        )

        street_num = random.randint(1, 999)

        location = {
            "province": city_data["province"],
            "city": city_data["city"],
            "area": city_data["area"],
            "address": f"{city_data['province']} {city_data['city']}{city_data['area']}第{street_num}号",
            "longitude": longitude,
            "latitude": latitude,
        }

        return location

    def lottery(self, location, lottery_count):

        url = BASE_URL + LOTTERY_API

        scene_code = SCENE_CODE_1 if lottery_count <= 3 else SCENE_CODE_2

        data = {
            "code": scene_code,
            "provice_name": location["province"],
            "city_name": location["city"],
            "area_name": location["area"],
            "address": location["address"],
            "longitude": location["longitude"],
            "dimension": location["latitude"],
        }

        scene_type = "SCENE1" if lottery_count <= 3 else "SCENE2"
        self.log(f"📍 {location['city']} {location['area']} [{scene_type}]")

        try:
            response = self.session.post(
                url, json=data, headers=self.get_headers(), timeout=30
            )
            result = response.json()

            if result.get("success"):

                data = result.get("data", {})
                if isinstance(data, dict):

                    prizedto = data.get("prizedto", {})
                    if prizedto:
                        prize_name = prizedto.get("prize_name", "未知奖品")
                        prize_level = prizedto.get("prize_level", "")
                        prize_type = prizedto.get("prize_type", "")

                        goods = prizedto.get("goods", [])
                        if goods and len(goods) > 0:
                            log_id = goods[0].get("log_id")
                            goods_name = goods[0].get("goods_name", prize_name)

                            if log_id:
                                self.log_ids.append(log_id)
                                self.prize_list.append(
                                    f"{prize_name} ({prize_level})"
                                    if prize_level
                                    else prize_name
                                )
                                self.log(f"🎉 {prize_name} ({prize_level})")

                                if "一等奖" in prize_level or "一等奖" in prize_name:
                                    self.first_prize_count += 1
                                    self.log(
                                        f"🏆🏆🏆 一等奖！！！已中 {self.first_prize_count} 次一等奖"
                                    )
                                    QLNotifier.send("农夫山泉一等奖", "已中")


                                    winning_info = location.copy()
                                    winning_info.update(
                                        {
                                            "prize_name": prize_name,
                                            "prize_level": prize_level,
                                            "prize_type": prize_type,
                                            "log_id": log_id,
                                            "time": datetime.now().strftime(
                                                "%Y-%m-%d %H:%M:%S"
                                            ),
                                        }
                                    )

                                return True
                        else:
                            self.log(f"ℹ️ 抽奖结果: {prize_name} ({prize_level})")
                    else:
                        self.log(f"ℹ️ 抽奖结果: {data}")

                return True
            else:
                msg = result.get("msg", "未知错误")

                if "今日活动抽奖次数已经达到最大" in msg or "抽奖次数已用完" in msg:
                    self.log(f"❌ 抽奖失败: {msg}")
                    return "LIMIT_REACHED"
                elif "资格卡券" in msg and "不足" in msg:
                    self.log(f"❌ 抽奖失败: 用户资格卡券不足")
                    return "LIMIT_REACHED"
                else:
                    self.log(f"❌ 抽奖失败: {msg}")

                return False

        except Exception as e:
            self.log(f"❌ 抽奖异常: {str(e)}")
            return False

    def get_win_list(self):

        act_codes = f"{ACT_CODE},{ACT_CODE_2}"
        url = f"{BASE_URL}{WIN_LIST_API}?act_codes={act_codes}"

        try:
            response = self.session.get(url, headers=self.get_headers(), timeout=30)
            result = response.json()

            if result.get("code") == 200:
                data = result.get("data", [])

                unreceived = [item for item in data if item.get("grant_status") == 10]
                return unreceived
            else:
                self.log(f"❌ 查询中奖列表失败: {result.get('msg', '未知错误')}")
                return []
        except Exception as e:
            self.log(f"❌ 查询中奖列表异常: {str(e)}")
            return []

    def receive_prize(self, log_id):

        url = BASE_URL + RECEIVE_API
        data = f"log_ids={log_id}"

        try:
            response = self.session.post(
                url,
                data=data,
                headers=self.get_headers("application/x-www-form-urlencoded"),
                timeout=30,
            )
            result = response.json()

            if result.get("code") == 200:
                self.log(f"✅ 领奖成功")
                return True
            else:
                self.log(f"❌ 领奖失败: {result.get('msg', '未知错误')}")
                return False

        except Exception as e:
            self.log(f"❌ 领奖异常: {str(e)}")
            return False

    def run(self):

        self.log(f"========== 开始执行 ==========")

        max_daily_count = self.do_all_tasks()

        if self.completed_tasks > 0:
            self.log(f"\n⏰ 等待3秒后开始抽奖...\n")
            time.sleep(3)

        self.log(f"📌 阶段2: 查询剩余次数")
        used_count = self.get_today_lottery_count()
        base_remaining = max(0, max_daily_count - used_count)
        max_task_lottery = 4
        total_lottery_count = base_remaining + max_task_lottery

        self.log(
            f"💡 基础: {base_remaining}/{max_daily_count} | 任务: {max_task_lottery} | 总计: {total_lottery_count}次"
        )

        if total_lottery_count == 0:
            self.log(f"⚠️ 无可用次数")
            self.log(f"\n========== 执行完成 ==========\n")
            return

        self.log(f"📌 阶段3: 开始抽奖 ({total_lottery_count}次)")
        lottery_stopped = False
        actual_lottery_count = 0

        for i in range(total_lottery_count):
            current_lottery_num = used_count + i + 1
            self.log(f"[{i+1}/{total_lottery_count}] 第{current_lottery_num}次")

            location = self.generate_random_location()
            result = self.lottery(location, current_lottery_num)
            actual_lottery_count += 1

            if result == "LIMIT_REACHED":
                self.log(f"⚠️ 已达上限，停止")
                lottery_stopped = True
                break

            time.sleep(random.uniform(2, 4))

        unreceived_prizes = self.get_win_list()

        if unreceived_prizes:
            self.log(f"📌 阶段4: 领取奖品 ({len(unreceived_prizes)}个)")

            for idx, prize in enumerate(unreceived_prizes, 1):
                log_id = prize.get("log_id")
                prize_name = prize.get("win_goods_name", "未知奖品")
                self.log(f"[{idx}/{len(unreceived_prizes)}] {prize_name}")
                self.receive_prize(log_id)
                time.sleep(random.uniform(1, 2))
        elif len(self.log_ids) > 0:
            self.log(f"📌 阶段4: 所有奖品已领取")

        self.log(
            f"\n📊 统计: 任务{self.completed_tasks} | 抽奖{actual_lottery_count} | 中奖{len(self.log_ids)}"
        )

        if actual_lottery_count > 0:
            win_rate = (len(self.log_ids) / actual_lottery_count) * 100
            self.log(f"🎯 中奖率: {win_rate:.2f}%")

        if self.prize_list:
            self.log(f"🎁 奖品: {', '.join(self.prize_list)}")

        self.log(f"\n========== 执行完成 ==========\n")


def main():

    tokens = "9d0217f7-a735-4341-824d-8fb7f8bf0679&1c25f9c75be24f0db74dba486dc119a506b0f2790a3d4e1daf9dad21370d9d53"

    if not tokens:
        print("❌ 请设置环境变量 DD_nfsq")
        print("格式: unique_identity&apitoken")
        print("多账号用换行或@分隔")
        print(
            "示例: 2a9d62fd-899e-4981-8b71-44adc739facc&6d412ac633ff4e8f8f642fb234d2fd64a380d4a3568f4fc588fe44dabe1265a2"
        )
        sys.exit(1)

    token_list = tokens.replace("\n", "@").split("@")
    token_list = [t.strip() for t in token_list if t.strip()]

    print(f"\n" + "=" * 60)
    print(f"🚀 山泉启动（任务+抽奖）")
    print(f"=" * 60)
    print(f"共找到 {len(token_list)} 个账号")
    print(f"=" * 60 + "\n")

    for idx, token in enumerate(token_list, 1):
        parts = token.split("&")

        if len(parts) < 2:
            print(f"❌ 账号{idx}格式错误，跳过（需要格式: unique_identity&apitoken）")
            continue

        try:
            unique_identity = parts[0].strip()
            apitoken = parts[1].strip()

            print(f"\n" + "#" * 60)
            print(f"账号 {idx}/{len(token_list)}")
            print(f"#" * 60 + "\n")

            nfsq = NongFuShanQuan(unique_identity, apitoken)
            nfsq.run()

            if idx < len(token_list):
                wait_time = random.randint(5, 10)
                print(f"\n等待 {wait_time} 秒后执行下一个账号...\n")
                time.sleep(wait_time)

        except Exception as e:
            print(f"❌ 账号{idx}执行异常: {str(e)}")
            continue

    print(f"\n{'='*50}")
    print(f"所有账号执行完成")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()

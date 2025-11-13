// ydwx_fetch.js
import crypto from 'crypto';
import notification from "../utils/notification-kit.js";

// # 7553
// # angel
// # 9553
const ydwx_deviceParams=[
    "eyJwaG9uZSI6IjE4OTA4Njg3NTUzIiwiZGV2aWNlIjoiaVBob25lMTUsNCIsImRldmljZUlkIjoiQkdXS1JvcHk5c1cxUkl6anhoNUdESjhCcDJpRE54bzI0YU5SWEdmUHBobkNnWEtLM1gyRlwvNk50V2ViSlFqeUcrZGc1V0VnWWhZazdsQTVCclB1VWtDdz09IiwibG9jYXRpb24iOnsiZ3BzTG9uZ2l0dWRlIjoiMTE0LjIwMDEiLCJncHNMYXRpdHVkZSI6IjMwLjU1MDMifSwiZGV2aWNlTmFtZSI6ImlQaG9uZSJ9",
    "eyJwaG9uZSI6IjE4Njc0MDA5ODY4IiwiZGV2aWNlIjoiaVBob25lMTYsMSIsImRldmljZUlkIjoiQkFcL2U5em13cXpvdng4WkJJZHJzMVpFMWh5eE9EUm1PM2txSFRnSFNNdldRVlB1T0l3S0pGQlltTVwvWng5NFwvNzNjUmxDdHBCc0xzS3hrWnBCeHVjTlwvUT09IiwibG9jYXRpb24iOnsiZ3BzTG9uZ2l0dWRlIjoiMTE0LjIwMDEiLCJncHNMYXRpdHVkZSI6IjMwLjU1MDMifSwiZGV2aWNlTmFtZSI6ImlQaG9uZSJ9",
    "eyJwaG9uZSI6IjE4OTYzNDM5NTUzIiwiZGV2aWNlIjoiaVBob25lOSwxIiwiZGV2aWNlSWQiOiJCVG5HUlZcL1pTT08ybVFyblFUWmR6Q2tET0tna3o0N0t1bHl1V1BcL1FGRmlzNWdEZW9SdHYybWw2RGdtd0RCYldYMFhRSDk2eGZkazhVVEdNV0x6XC8zalE9PSIsImRldmljZU5hbWUiOiJpUGhvbmUgKDIpIn0="
]
const ydwx_token=[
    "7f0e71b32c29464aa8666f9db6087474",
    "eb50fb3c16fb4a9fa389308744343c9b",
    "f0eafd0624b345a38aa25b59abd27970"
]

// 生成签名
function generateSign(deviceParams, token, timestamp) {
  const sig = `action=mixc.app.memberSign.sign&apiVersion=1.0&appId=68a91a5bac6a4f3e91bf4b42856785c6&appVersion=3.53.0&deviceParams=${deviceParams}&imei=2333&mallNo=20014&osVersion=12.0.1&params=eyJtYWxsTm8iOiIyMDAxNCJ9&platform=h5&timestamp=${timestamp}&token=${token}&P@Gkbu0shTNHjhM!7F`;
  return crypto.createHash('md5').update(sig).digest('hex');
}

// 睡眠函数
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));
let err = false;
// 单个账号签到
async function signAccount(deviceParams, token, index) {
  const timestamp = Date.now().toString();
  const sign = generateSign(deviceParams, token, timestamp);

  const data = `mallNo=20014&appId=68a91a5bac6a4f3e91bf4b42856785c6&platform=h5&imei=2333&appVersion=3.53.0&osVersion=12.0.1&action=mixc.app.memberSign.sign&apiVersion=1.0&timestamp=${timestamp}&deviceParams=${deviceParams}&token=${token}&params=eyJtYWxsTm8iOiIyMDAxNCJ9&sign=${sign}`;

  const headers = {
    'Host': 'app.mixcapp.com',
    'Connection': 'keep-alive',
    'Content-Length': Buffer.byteLength(data).toString(),
    'Accept': 'application/json, text/plain, */*',
    'Origin': 'https://app.mixcapp.com',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 10; PCAM00 Build/QKQ1.190918.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/77.0.3865.92 Mobile Safari/537.36/MIXCAPP/3.42.2/AnalysysAgent/Hybrid',
    'Sec-Fetch-Mode': 'cors',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'com.crland.mixc',
    'Sec-Fetch-Site': 'same-origin',
    'Referer': 'https://app.mixcapp.com/m/m-20014/signIn?showWebNavigation=true&timestamp=1676906528979&appVersion=3.53.0&mallNo=20014',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
  };

  console.log(`账号${index + 1} 开始签到...`);

  // 重试机制
  for (let retry = 0; retry < 3; retry++) {
    try {
      console.log(`第${retry + 1}次尝试...`);

      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 30000);

      const response = await fetch('https://app.mixcapp.com/mixc/gateway', {
        method: 'POST',
        headers: headers,
        body: data,
        signal: controller.signal
      });

      clearTimeout(timeoutId);

      console.log(`状态码: ${response.status}`);

      if (response.status === 200) {
        const result = await response.json();
        const message = result.message || '未知结果';
        if (result.code !== 0) {
          err = true;
        }
        console.log(`账号${index + 1} 响应:`, JSON.stringify(result));
        return `帐号${index + 1}签到结果: ${message}`;
      } else if (response.status === 405) {
        console.log(`账号${index + 1} 405错误，请求方法不被允许`);
        if (retry < 2) {
          await sleep(5000);
          continue;
        }
        return `帐号${index + 1}签到失败: HTTP 405 方法不被允许`;
      } else {
        console.log(`账号${index + 1} HTTP错误: ${response.status}`);
        return `帐号${index + 1}签到失败: HTTP ${response.status}`;
      }
    } catch (error) {
      console.log(`账号${index + 1} 请求异常:`, error.name, error.message);

      if (error.name === 'AbortError') {
        console.log('请求超时');
        if (retry < 2) {
          await sleep(10000);
          continue;
        }
        return `帐号${index + 1}签到失败: 请求超时`;
      }

      if (retry < 2) {
        const delay = (retry + 1) * 3000;
        console.log(`等待${delay}ms后重试...`);
        await sleep(delay);
        continue;
      }
      return `帐号${index + 1}签到失败: ${error.message}`;
    }
  }

  return `帐号${index + 1}签到失败: 多次重试后仍失败`;
}

// 主函数
async function main() {
  console.log(`共配置了${ydwx_deviceParams.length}个账号`);
  const log = [];
  let lastMsg = "未知状态";

  for (let i = 0; i < ydwx_deviceParams.length; i++) {
    console.log(`\n*****第${i + 1}个账号*****`);
    const result = await signAccount(ydwx_deviceParams[i], ydwx_token[i], i);
    log.push(result);

    if (result.includes("签到结果:")) {
      lastMsg = result.split("签到结果:")[1].trim();
    }

    // 随机延迟（如果不是最后一个账号）
    if (i < ydwx_deviceParams.length - 1) {
      const delay = Math.floor(Math.random() * (60 - 30 + 1)) + 30;
      console.log(`等待${delay}秒后处理下一个账号...`);
      await sleep(delay * 1000);
    }
  }

  const logText = log.join('\n');
  console.log(`\n最终结果:\n${logText}`);

  // 发送通知
  // await sendNotify('一点万象签到', logText);

  return { title: '签到' + err, content: logText, lastMsg };
}

// 执行
main().then(result => {
  console.log('执行完成:', result);
  setTimeout(() => {
    notification.pushMessage({
      title: "一点万象" + result.title,
      content: "结果:" + result.logText,
      msgtype: "text"
    });
  }, 40);
}).catch(error => {
  console.error('执行失败:', error);
  setTimeout(() => {
    notification.pushMessage({
      title: "原神签到" + title_str,
      content: "结果:" + send_str,
      msgtype: "text"
    });
  }, 40);
});
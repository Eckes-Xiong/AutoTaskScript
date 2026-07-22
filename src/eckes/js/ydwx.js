// ydwx_fetch.js  一点万象
import axios from 'axios';
import https from 'https';
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

// 创建axios实例
function createAxiosInstance() {
    const httpsAgent = new https.Agent({
        keepAlive: true,
        keepAliveMsecs: 30000,
        timeout: 45000,
        rejectUnauthorized: true, // 证书验证通过，可以设为true
        secureProtocol: 'TLSv1_2_method'
    });

    return axios.create({
        baseURL: 'https://app.mixcapp.com',
        timeout: 45000,
        httpsAgent: httpsAgent,
        headers: {
            'Host': 'app.mixcapp.com',
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'Origin': 'https://app.mixcapp.com',
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-Requested-With': 'com.crland.mixc',
            'Referer': 'https://app.mixcapp.com/m/m-20014/signIn?showWebNavigation=true&appVersion=3.53.0&mallNo=20014',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        },
        // 重要：设置验证状态，不抛出HTTP错误
        validateStatus: function (status) {
            return status >= 200 && status < 500; // 接受200-499的状态码
        }
    });
}

// 生成签名
function generateSign(deviceParams, token, timestamp) {
    const sig = `action=mixc.app.memberSign.sign&apiVersion=1.0&appId=68a91a5bac6a4f3e91bf4b42856785c6&appVersion=3.53.0&deviceParams=${deviceParams}&imei=2333&mallNo=20014&osVersion=12.0.1&params=eyJtYWxsTm8iOiIyMDAxNCJ9&platform=h5&timestamp=${timestamp}&token=${token}&P@Gkbu0shTNHjhM!7F`;
    return crypto.createHash('md5').update(sig).digest('hex');
}

// 睡眠函数
const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// 测试服务器连通性
async function testServerConnectivity(instance) {
    try {
        console.log('测试服务器连通性...');
        // 测试OPTIONS方法
        const optionsResponse = await instance.options('/mixc/gateway');
        console.log(`OPTIONS请求状态: ${optionsResponse.status}`);
        return true;
    } catch (error) {
        console.log('OPTIONS请求失败，继续尝试POST请求:', error.message);
        return true; // 即使OPTIONS失败也继续
    }
}

// 单个账号签到
async function signAccount(deviceParams, token, index) {
    const instance = createAxiosInstance();
    const timestamp = Date.now().toString();
    const sign = generateSign(deviceParams, token, timestamp);
    
    const data = `mallNo=20014&appId=68a91a5bac6a4f3e91bf4b42856785c6&platform=h5&imei=2333&appVersion=3.53.0&osVersion=12.0.1&action=mixc.app.memberSign.sign&apiVersion=1.0&timestamp=${timestamp}&deviceParams=${deviceParams}&token=${token}&params=eyJtYWxsTm8iOiIyMDAxNCJ9&sign=${sign}`;

    console.log(`\n账号${index + 1} 开始签到...`);
    console.log(`Timestamp: ${timestamp}`);
    console.log(`Sign: ${sign}`);

    for (let retry = 0; retry < 3; retry++) {
        try {
            console.log(`第${retry + 1}次尝试...`);

            // 更新Referer时间戳
            const currentHeaders = {
                ...instance.defaults.headers.common,
                'Content-Length': Buffer.byteLength(data).toString(),
                'Referer': `https://app.mixcapp.com/m/m-20014/signIn?showWebNavigation=true&timestamp=${timestamp}&appVersion=3.53.0&mallNo=20014`
            };

            const response = await instance.post('/mixc/gateway', data, {
                headers: currentHeaders
            });

            console.log(`HTTP状态码: ${response.status}`);
            
            if (response.status === 200) {
                const result = response.data;
                console.log('响应数据:', JSON.stringify(result, null, 2));
                
                if (result && typeof result === 'object') {
                    const message = result.message || result.msg || '未知结果';
                    const code = result.code || result.status;
                    
                    if (code === 200 || code === '200' || message.includes('成功')) {
                        return `帐号${index + 1}签到结果: ${message}`;
                    } else {
                        return `帐号${index + 1}签到失败: ${message} (代码: ${code})`;
                    }
                } else {
                    return `帐号${index + 1}签到结果: 响应格式异常`;
                }
            } else if (response.status === 405) {
                console.log('405错误: 方法不被允许，可能是请求头问题');
                // 尝试调整请求头
                if (retry === 1) {
                    delete instance.defaults.headers.common['X-Requested-With'];
                }
                await sleep(5000);
                continue;
            } else {
                console.log(`HTTP ${response.status} 错误`);
                return `帐号${index + 1}签到失败: HTTP ${response.status}`;
            }

        } catch (error) {
            console.log(`第${retry + 1}次尝试失败:`, error.message);
            
            if (error.response) {
                // 服务器响应了错误状态码
                console.log(`服务器响应: ${error.response.status}`, error.response.data);
                if (error.response.status >= 500 && retry < 2) {
                    await sleep(8000);
                    continue;
                }
                return `帐号${index + 1}签到失败: HTTP ${error.response.status}`;
            } else if (error.code) {
                console.log(`错误代码: ${error.code}`);
                if (retry < 2) {
                    await sleep(10000);
                    continue;
                }
                return `帐号${index + 1}签到失败: ${error.code}`;
            } else {
                if (retry < 2) {
                    await sleep(5000);
                    continue;
                }
                return `帐号${index + 1}签到失败: ${error.message}`;
            }
        }
    }
    
    return `帐号${index + 1}签到失败: 多次重试后仍失败`;
}

// 主函数
async function main() {
    console.log('🚀 开始一点万象签到任务');
    console.log(`📱 共配置了${ydwx_deviceParams.length}个账号`);
    
    const log = [];
    let lastMsg = "未知状态";

    try {
        // 先测试连通性
        const instance = createAxiosInstance();
        await testServerConnectivity(instance);

        for (let i = 0; i < ydwx_deviceParams.length; i++) {
            console.log(`\n${'='.repeat(40)}`);
            console.log(`第${i + 1}个账号`);
            console.log(`${'='.repeat(40)}`);
            
            const result = await signAccount(ydwx_deviceParams[i], ydwx_token[i], i);
            log.push(result);
            
            if (result.includes("签到结果:")) {
                lastMsg = result.split("签到结果:")[1].trim();
            }
            
            // 随机延迟
            if (i < ydwx_deviceParams.length - 1) {
                const delay = Math.floor(Math.random() * 30) + 30;
                console.log(`⏰ 等待${delay}秒后处理下一个账号...`);
                await sleep(delay * 1000);
            }
        }

        const logText = log.join('\n');
        console.log(`\n🎉 任务完成!\n${logText}`);
        
        return { 
            success: true, 
            title: '一点万象签到', 
            content: logText, 
            lastMsg 
        };
        
    } catch (error) {
        console.error('❌ 任务失败:', error);
        return {
            success: false,
            title: '一点万象签到失败',
            content: `执行失败: ${error.message}`,
            lastMsg: '执行失败'
        };
    }
}

// 执行
main().then(result => {
  console.log('执行完成:', result);
  setTimeout(() => {
    notification.pushMessage({
      title: "一点万象" + result.title,
      content: "结果:" + result.content,
      msgtype: "text"
    });
  }, 40);
}).catch(error => {
  console.error('执行失败:', error);
  setTimeout(() => {
    notification.pushMessage({
      title: "一点万象 err",
      content: "结果: err",
      msgtype: "text"
    });
  }, 40);
});

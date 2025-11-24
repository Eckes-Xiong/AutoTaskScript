/**
 * #小程序://星妈优选/c8Gx0xHeOxwrMUv
 *
 * 抓包 Host：https://www.feihevip.com 获取请求头 token
 * export STAR_MOM_TOKEN = 'eyJ0exxxxxxxxxxx'
 * 多账号用 & 或换行
 *
 * 时效性很短，不建议跑
 *
 * @author Telegram@common
 * @site https://blog.imzjw.cn
 * @date 2024/09/22
 *
 * const $ = new Env('星妈优选')
 * cron: 39 5 * * *
 */
import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
const starMomList = [
    "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJ4bXl4IiwiZXhwIjoxNzUzOTQxMTE1LCJpYXQiOjE3NTM5MzM5MTUsInVzZXIiOiJ4bXl4QWVzVXNlckluZm86cGxRSzNEalhmQXE0NFhCbk9ablZDNUpzb1JzRktEWjRtRVBISlhsUTNKbU9ZWGdjdHY2NTlpczJIN25VR0d1MVFWdFNiMVVVTGZKL1RQQVRoRkJVdnIwZlg4eURpWTJSSGtscm9HSlRLUGpBcWRxOVdhSmJJS0VESWx6VEdqdUlPOUdpanI4ZWNvbmdZRlQxT00wRm5nRkdUb0FmZjlmZTFuSDBlWnA2c0tqRXZHV3lYRm4vMWRWSlovZ2FFRVJ3In0.zzsR9RnvtVouoewvEK9oV9xKWiHxrfmOqdzxYfjfGqA",
];
// 消息推送
let message = '';
// 接口地址
const baseUrl = 'https://www.feihevip.com'
// appId
const appId = 'xmyx';
// appKey
const appKey = 'TwUQ01lKS1Km5zlV2f7amsZc5EQYkTbv'
// 请求头
const headers = {
    'User-Agent': common.getRandomUserAgent(),
    "Host": "www.feihevip.com",
    'Content-Type': "application/json",
    'Referer': 'https://servicewechat.com/wx4205ec55b793245e/271/page-frame.html',
    "fhAppid": appId,
    "source": 1
};
let lastMsg = "err";
// 任务列表
let taskList = [
    {taskName: "爆品好物助成长", taskType: "TZSPXQ5", time: 3},
    // {taskName: "浏览热销爆品1", taskType: "TZSPXQ2", time: 16},
    // {taskName: "浏览热销爆品2", taskType: "TZSPXQ300003", time: 16},
    // {taskName: "浏览热销爆品3", taskType: "TZSPXQ1", time: 16},
    {taskName: "滑动浏览精选超值好物", taskType: "LLQDYSPL", time: 16},
    {taskName: "购买任意商品1次", taskType: "YXXD", time: 3},
    //{taskName: "大转盘抽奖", taskType: "YXDZP", time: 3},
    {taskName: "逛全网最低好物会场", taskType: "LLQWZDJ", time: 16},
    //{taskName: "补签赚积分", taskType: "YXBQ", time: 3},
    //{taskName: "浏览粮油专场10s", taskType: "XXGG", time: 11}
];

!(async () => {
    console.log(`\n已随机分配 User-Agent\n\n${headers['user-agent'] || headers['User-Agent']}`);
    for (let i = 0; i < starMomList.length; i++) {
        const index = i + 1;
        headers.token = starMomList[i];
        // await refreshToken(starMomList[i]);
        console.log(`\n*****第[${index}]个账号*****`);
        message += `📣====账号[${index}]====📣\n`;
        await main();
        await common.wait(common.getRandomWait(2000, 2500));
    }
    if (message) {
        await notification.pushMessage({
          title: "星妈飞鹤wx:"+lastMsg,
          content: "结果:"+message,
          msgtype: "text"
        });
    }
})()

async function main() {
    await sign();
    await common.wait(common.getRandomWait(1e3, 2e3));
    console.log('开始执行任务列表...');
    await common.wait(common.getRandomWait(500, 888));
    const data = await common.sendRequest(`${baseUrl}/api/member/signin/getTaskList`, 'get', Object.assign(headers, getSignature()));
    taskList = data.data;

    for (const task of taskList) {
        await toFinish(task.taskName, task.taskType);
        await common.wait(common.getRandomWait(500, 1888));
        await completeTask(task.taskName, task.taskType);
        await common.wait(common.getRandomWait(1e3, 3e3));
    }
    await getUserInfo();
}

/**
 * 签到
 *
 * @returns {Promise<void>}
 */
async function sign() {
    try {
        const data = await common.sendRequest(`${baseUrl}/api/member/signin/getSignInfo?signType=1`, 'get', Object.assign(headers, getSignature()));
        if ('200' !== data.code) {
            return console.error(data.msg);
        }

        console.log( `签到成功`);
        message += `签到成功\n`;
    } catch (e) {
        console.error('签到时发生异常 ->', e.response.data);
    }
}

/**
 * 执行任务
 *
 * @param taskName 任务名称
 * @param taskType 任务类型
 *
 * @returns {Promise<void>}
 */
async function toFinish(taskName, taskType) {
    try {
        const data = await common.sendRequest(`${baseUrl}/api/member/signin/tofinish?taskType=${taskType}`, 'get', Object.assign(headers, getSignature()));
        if ('200' !== data.code) {
            return console.error(`执行[${taskName}]任务失败 ->`, data.msg);
        }
        console.log(`去执行[${taskName}]任务`);
    } catch (e) {
        console.error(`执行[${taskName}]任务时发生异常 ->`, e.response.data);
    }
}

/**
 * 完成任务
 *
 * @param taskName 任务名称
 * @param taskType 任务类型
 *
 * @returns {Promise<void>}
 */
async function completeTask(taskName, taskType) {
    try {
        const data = await common.sendRequest(`${baseUrl}/api/member/signin/completeTask?taskType=${taskType}`, 'get', Object.assign(headers, getSignature()));
        if ('200' !== data.code) {
            return console.error(`完成[${taskName}]任务失败❌ ->`, data.msg, '\n');
        }
        const point = data.data.awardSendPoints;
        console.log(`完成任务[${taskName}]---成功✅，积分+${point}\n`);
        message += `完成任务[${taskName}]---成功✅，积分+${point}\n`;
    } catch (e) {
        console.error(`完成[${taskName}]任务时发生异常 ->`, e.response.data);
    }
}

/**
 * 获取用户信息\积分
 *
 * @return {Promise<void>}
 */
async function getUserInfo() {
    try {
        const data = await common.sendRequest(`${baseUrl}/api/starMember/getMemberInfo`, 'post', Object.assign(headers, getSignature()));
        if ('200' !== data.code) {
            return console.error(data.msg);
        }
        // 积分
        const score = data.data.memberPoints.scoreValue;
        // 等级
        const level = data.data.memberGrade.currentGrade;
        // 用户名
        const userName = data.data.baseInfo.nickName;
        console.log(`昵称：${userName}(${level})\n当前积分：${score}`);
        message += `昵称：${userName}(${level})\n当前积分：${score}\n\n`;
        lastMsg += (":"+score);
    } catch (e) {
        console.error('获取用户信息时发生异常 ->', e.response.data);
    }
}

async function refreshToken(token) {
    try {
        const {fhNonceStr, fhTimestamp, fhSign} = getRefreshTokenSignature();
        const header = {
            "Host": "mom.feihe.com",
            "token": token,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 15_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.48(0x1800302b) NetType/4G Language/zh_CN",
            "Referer": "https://servicewechat.com/wx4205ec55b793245e/215/page-frame.html",
            "fhAppid": 'xmh',
            "source": 1,
            fhNonceStr,
            fhTimestamp,
            fhSign
        }
        const data = await common.sendRequest('https://mom.feihe.com/program/token/refreshToken', 'get', header);
        console.log(data);

    } catch (e) {
    }
}

function getRefreshTokenSignature() {
    const fhNonceStr = getFhNonceStr({length: 16})
    const fhTimestamp = +String(Date.now()).slice(0, 10);
    const signString = `fhAppidxmhfhNonceStr${fhNonceStr}fhTimestamp${fhTimestamp}98d9fe9b613a479dbcb111ca261e3ce1`
    return {
        fhNonceStr,
        fhTimestamp,
        fhSign: common.md5(signString).toUpperCase()
    }
}

/**
 * 获取签名
 *
 * @param data
 * @returns {{fhSign: string, fhNonceStr: string, fhTimestamp: number}}
 */
function getSignature(data = {}) {
    const json = data ? JSON.stringify(data) : ''
    const fhNonceStr = getFhNonceStr({length: 16})
    const fhTimestamp = +String(Date.now()).slice(0, 10);
    const signString = `fhAppid${appId}fhNonceStr${fhNonceStr}fhTimestamp${fhTimestamp}${json}${appKey}`
    return {
        fhNonceStr,
        fhTimestamp,
        fhSign: common.md5(signString).toUpperCase()
    }
}

/**
 * 生成随机字符串
 *
 * @param t
 * @returns {string}
 */
function getFhNonceStr(t) {
    let e, r, n = "",
        o = (t = function (t) {
            return t || (t = {}), {
                length: t.length || 8,
                numeric: "boolean" != typeof t.numeric || t.numeric,
                letters: "boolean" != typeof t.letters || t.letters,
                special: "boolean" == typeof t.special && t.special,
                exclude: Array.isArray(t.exclude) ? t.exclude : []
            }
        }(t)).length;
    t.exclude;
    const i = function (t) {
        let e = "";
        t.numeric && (e += "0123456789"), t.letters && (e += "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"), t.special && (e += "!$%^&*()_+|~-=`{}[]:;<>?,./");
        for (let r = 0; r <= t.exclude.length; r++) e = e.replace(t.exclude[r], "");
        return e
    }(t);
    for (e = 1; e <= o; e++) n += i.substring(r = Math.floor(Math.random() * i.length), r + 1);
    return n
}

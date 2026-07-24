/**
 * #小程序://雀巢会员/4EpKApLxlhQhsiu
 *
 * 抓包 Host：https://crm.nestlechinese.com 获取请求头 authorization 并且删掉 Bearer
 * export NESTLE_TOKEN = 'eyJhbxxxxXXXXxxxxxXXX'
 * 多账号用 & 或换行
 *
 * @author Telegram@common
 * @site https://blog.imzjw.cn
 * @date 2024/11/27
 * 
 * 7553, 6013, angle
 *
 * const $ = new Env('雀巢会员')
 * cron: 28 8 * * *
 */
import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
const $ = {name: 'wxapp'};

let nestleList = [
    "Bearer eyJhbGciOiJSUzI1NiIsImtpZCI6Ijk1RDNEQzJDRDg0REM5Nzc1MDE0NzhBQkVDQjBBQ0Q5MjU3QjRGMjNSUzI1NiIsInR5cCI6ImF0K2p3dCIsIng1dCI6ImxkUGNMTmhOeVhkUUZIaXI3TENzMlNWN1R5TSJ9.eyJuYmYiOjE3ODQ4NjM5NTQsImV4cCI6MTc4NDg2NzQ1NCwiaXNzIjoiaHR0cDovL2lkZW50aXR5OjgwODAiLCJjbGllbnRfaWQiOiJ3ZWNoYXRNaW5pIiwic3ViIjoib2lySWQxWUFUcmlfN25aYXp5d00yTnJOLXhyZyIsImF1dGhfdGltZSI6MTc4NDg2Mzk1NCwiaWRwIjoibG9jYWwiLCJ1bmlvbmlkIjoib2lySWQxWUFUcmlfN25aYXp5d00yTnJOLXhyZyIsIm1pbmlfb3BlbmlkIjoib050SzE1RW1Mdk5mRTg5SnlCVUllang1M2NsWSIsInVzZXJfaWQiOiIxOTIzMzAxMjQyNzEzMTA0Mzg0IiwianRpIjoiMDc0QTM2Q0E1NDMxOTAxMjFCQTJCRDc4QTNFM0I5NTMiLCJpYXQiOjE3ODQ4NjM5NTQsInNjb3BlIjpbImdhdGV3YXlfYXBpIiwiZ29vZHMiLCJtZW1iZXIiLCJvcmRlcnMiLCJvZmZsaW5lX2FjY2VzcyJdLCJhbXIiOlsid2VjaGF0X2F1dGhfY29kZSJdfQ.gG4EYb0jJQ_zO2Ye4vBMnBCCaCOkxAgek8HSoDMqZcr7W8Kell_BjfroTZ9DK7llyC1R6JaA5vjxKPeWbmQCjxLbwNVa7O5mrruGx2ECpVEYwoPvZDBJTz-f-q7JA7WqvNdHZSjRQK62gLoRbNUCuLhM9fU-dXGzoYlJFqtyicEr5qrr2_4_HRKJbQ0WCp99CccE9x95wPjlF3nKj2cPryD7OFfsrRLiJeyDANuJvgkDFEGTlahW9WdD6K3KPhJZC5r7EFkwgFBwi_k-gqBN1XQ3hCKtIqe_QDeKyd3VLmV_BAJpY_9uCwdPGhYWUGzsitWy3rhic-Ze5b_-QldR4A",
]



let message = '';
// 接口地址
const baseUrl = 'https://crm.nestlechinese.com'
// 请求头
const headers = {
    'User-Agent': common.getRandomUserAgent(),
    'content-type': 'application/json',
    'referer': 'https://servicewechat.com/wxc5db704249c9bb31/353/page-frame.html',
};

!(async () => {
    console.log(`\n已随机分配 User-Agent\n\n${headers['user-agent'] || headers['User-Agent']}`);
    for (let i = 0; i < nestleList.length; i++) {
        const index = i + 1;
        console.log(`\n*****第[${index}]个${$.name}账号*****`);
        headers.authorization = `${nestleList[i]}`;
        message += `📣====${$.name}账号[${index}]====📣\n`;
        await main();
        await common.wait(common.getRandomWait(2000, 2500));
        // await doSign();
    }
    if (message) {
        setTimeout(() => {
          notification.pushMessage({
            title: "雀巢wxapp",
            content: "结果:"+message,
            msgtype: "text"
          });
        }, 40);
    }
})()

async function main() {
    await getUserInfo();
    await common.wait(common.getRandomWait(1e3, 2e3));
    await getTaskList();
    await common.wait(common.getRandomWait(1e3, 2e3));
    await getUserBalance();
}

/**
 * 获取用户信息
 *
 * @return {Promise<void>}
 */
async function getUserInfo() {
    try {
        const data = await common.sendRequest(`${baseUrl}/openapi/member/api/User/GetUserInfo`, 'get', headers);
        if (200 !== data.errcode) {
            return console.error(`获取用户信息失败：${data.errmsg}`);
        }
        const {nickname, mobile} = data.data;
        console.log(`用户：${nickname}(${mobile})`);
        message += `用户：${nickname}(${mobile})\n`;
    } catch (e) {
        console.error(`获取用户信息时发生异常 -> ${e}`);
    }
}

async function getTaskList() {
    try {
        const data = await common.sendRequest(`${baseUrl}/openapi/activityservice/api/task/getlist`, 'post', headers);
        if (200 !== data.errcode) {
            return console.error(`获取任务列表失败：${data.errmsg}`);
        }
        for (const task of data.data) {
            console.log(`开始【${task.task_title}】任务`)

            if(task.task_url==='/pages/signbox/index/index'){
                await doSign()
                await common.wait(common.getRandomWait(2000, 2500));
                continue;
            }

            await doTask(task.task_guid);
            await common.wait(common.getRandomWait(2000, 2500));
        }
    } catch (e) {
        console.error(`获取任务列表时发生异常 -> ${e}`);
    }
}

async function doTask(task_guid) {
    try {
        const data = await common.sendRequest(`${baseUrl}/openapi/activityservice/api/task/add`, 'post', headers, {
            "task_guid": task_guid
        });
        if (200 !== data.errcode) {
            return console.error(`任务失败 -> ${data.errmsg}\n`);
        }
        console.log(`完成任务 -> ${data.errmsg}\n`);
    } catch (e) {
        console.error(`完成任务时发生异常 -> ${e}`);
    }
}

async function doSign() {
    try {
        const data = await common.sendRequest(`${baseUrl}/openapi/activityservice/api/sign2025/sign`, 'post', headers, {"rule_id":1,"goods_rule_id":1});
        if (201 === data.errcode) {
            message += `签到失败 -> ${data.errmsg}\n`;
            return console.error(`签到失败 -> ${data.errmsg}\n`);
        }
        if (200 === data.errcode) {
            message += `签到成功 获得 ${data.data.sign_points}分\n`;
            message += `签到天数 ${data.data.sign_day}天\n`;
            console.log(`签到成功 获得 ${data.data.sign_points}分\n`)
            console.log(`签到天数 ${data.data.sign_day}天\n`)
            return
        }
        
        console.log(`签到任务 -> ${data.errmsg}\n`);
    } catch (e) {
        console.error(`签到时发生异常 -> ${e}`);
    }
}

async function getUserBalance() {
    try {
        const data = await common.sendRequest(`${baseUrl}/openapi/pointsservice/api/Points/getuserbalance`, 'post', headers);
        if (200 !== data.errcode) {
            return console.error(`获取用户积分余额失败：${data.errmsg}`);
        }
        console.log(`当前巢币：${data.data}`);
        message += `当前巢币：${data.data}\n\n`;
    } catch (e) {
        console.error(`获取用户巢币时发生异常 -> ${e}`);
    }
}


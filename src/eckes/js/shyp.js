
/**
 * 上海杨浦APP
 * export SHYP_TOKEN = 'eyJ0eXxx'
 * 多账号用 & 或换行
 * cron: 33 7 * * *
 */
import axios from 'axios';
const shMediaList = [
  "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiJ9.eyJzdWIiOiI2MjQ2NDk4MDlmNjQ0YjY5YmJlZjlkYjFiNTk0YWEzMGJlMzk7MzEwMTEwIiwiaWF0IjoxNzQ1ODEwNjg1LCJleHAiOjI3ODI2MTA2ODV9.s4iMGrAC2jNv0u33bTv4-CL8GelBxiKswSF5p21D7_QXYpU6EKUd8C29FdSaRDvNFK6JD04eJhqN4DaaGPzFJA"
];
import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
const $ = {
  points:''
}
// 消息推送
let message = '';
// 接口地址
const baseUrl = 'https://ypapi.shmedia.tech'
// 请求头
const headers = {
    'User-Agent': 'okhttp/4.10.0',
    'Accept-Encoding': 'gzip',
    'siteid': '310110',
    'content-type': 'application/json; charset=UTF-8'
};
// 请求体
const dataBody = {
    "orderBy": "release_desc",
    "requestType": "2",
    "siteId": "310110"
}
// 映射表用于转换任务 ID
const TASK_ID_MAP = {
    '002': 'read',
    '003': 'video',
    '007': 'share'
};
let lastMsg = "err";

!(async () => {
    for (let i = 0; i < shMediaList.length; i++) {
        const index = i + 1;
        console.log(`\n*****第[${index}]个账号*****`);
        headers.token = shMediaList[i];
        message += `📣====上海杨浦APP账号[${index}]====📣\n`;
        await main();
        await common.wait(common.getRandomWait(2000, 2500));
    }
    if (message) {
      await notification.pushMessage({
        title: "上海杨浦APP:"+lastMsg,
        content: "结果:"+message,
        msgtype: "text"
      });
    }
})()

async function main() {
    await getUserInfo();
    await common.wait(common.getRandomWait(1500, 2500));
    await doTask();
    await common.wait(common.getRandomWait(1500, 2500));
    await getPoints();
    await common.wait(common.getRandomWait(1500, 2500));
    // await getGoodsList();
}

/**
 * 获取用户信息
 *
 * @returns {Promise<void>}
 */
async function getUserInfo() {
    try {
        //const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/personal/get`, 'post', headers);

        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/personal/get`, {}, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            return console.error('获取用户信息失败 ->', data.msg);
        }
        const mobile = data.data.mobile || '1***888****';
        const hiddenMobile = `${mobile.slice(0, 3)}***${mobile.slice(-3)}`;
        console.log(`${data.data.nickname}(${hiddenMobile})`);
        message += `${data.data.nickname}(${mobile})\n`;
    } catch (e) {
        console.error(`获取用户信息时发生异常 -> ${e}`);
    }
}

/**
 * 签到
 *
 * @returns {Promise<void>}
 */
async function sign() {
    try {
        //const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/personal/score/sign`, 'post', headers, dataBody);

        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/personal/score/sign`, dataBody, {
          headers:headers
        });
        const data = res.data;


        if (0 !== data.code) {
            return console.error('签到失败 ->', data.msg);
        }
        if (!data.data.score) {
            return console.error(data.data.title);
        }
        console.log(`签到成功，积分+${data.data.score}`);
        message += `签到成功\n`;
    } catch (e) {
        console.error(`签到时发生异常 -> ${e}`);
    }
}

/**
 * 获取任务列表
 *
 * @returns {Promise<void>}
 */
async function doTask() {
    try {
        //let data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/personal/score/info`, 'post', headers, dataBody);
        
        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/personal/score/info`, dataBody, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            return console.error(`获取任务列表失败 -> ${data.msg}`);
        }
        const tasks = data.data.jobs;
        for (const item of tasks) {
            if (['004', '006'].includes(item.id)) {
                console.log(`\n跳过【${item.title}】`);
                continue;
            }
            // 已获得的任务积分
            let taskScore = item.progress;
            if (taskScore >= item.totalProgress) {
                console.log(`【${item.title}】任务已完成`)
                await common.wait(common.getRandomWait(800, 1300));
                continue;
            }
            console.log(`\n开始【${item.title}】`);
            await common.wait(common.getRandomWait(1e3, 2e3));
            while (taskScore < item.totalProgress) {
                // 获取文章 ID
                const articleId = await getArticleId();
                switch (item.id) {
                    case '001':
                        // 签到
                        await sign();
                        await common.wait(common.getRandomWait(2e3, 3e3));
                        break;
                    case '002': // 阅读
                    case '003': // 视频
                    case '007': // 分享
                        await commonTask(item.id, item.title);
                        break;
                    case '005':
                        // 收藏
                        await favorArticle(articleId);
                        await common.wait(common.getRandomWait(5e3, 8e3));

                        break;
                    default:
                        console.log(`其它任务：${item.title}`);
                        break;
                }
                // 更新 taskScore
                taskScore = await updateTaskScore(item.id);
                await common.wait(common.getRandomWait(1e3, 2e3));
            }
        }
    } catch (e) {
        console.error(`获取任务列表时发生异常 -> ${e}`);
    }
}

/**
 * 通用任务 002
 *        003
 *        007
 *
 * @param taskId
 * @param taskName
 * @returns {Promise<void>}
 */
async function commonTask(taskId, taskName) {
    const taskType = TASK_ID_MAP[taskId];
    const taskUrl = `${baseUrl}/media-basic-port/api/app/points/${taskType}/add`;
    // const taskData = await sudojia.sendRequest(taskUrl, 'post', headers, {
    //     "orderBy": "release_desc",
    //     "requestType": "1",
    //     "siteId": "310110"
    // });
    const res = await axios.post(taskUrl, {
      "orderBy": "release_desc",
      "requestType": "1",
      "siteId": "310110"
    }, {
      headers:headers
    });
    const taskData = res.data;

    if (0 !== taskData.code) {
        throw new Error(`${taskName}任务失败 -> ${taskData.msg}`);
    }
    console.log(`${taskName}任务成功`);
    await common.wait(common.getRandomWait(5e3, 8e3));
}

/**
 * 更新任务积分
 *
 * @param itemId
 * @returns {Promise<*|void>}
 */
async function updateTaskScore(itemId) {
    try {
        // const updatedData = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/personal/score/info`, 'post', headers, dataBody);
        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/personal/score/info`, dataBody, {
          headers:headers
        });
        const updatedData = res.data;

        if (0 !== updatedData.code) {
            return console.error('更新任务列表失败 ->', updatedData.msg);
        }
        const updatedItem = updatedData.data.jobs.find(job => job.id === itemId);
        if (!updatedItem) {
            return console.error(`未找到任务ID: ${itemId}`);
        }
        return updatedItem.progress;
    } catch (e) {
        console.error(`更新任务列表出错 -> ${e}`);
    }
}

/**
 * 获取文章 ID
 *
 * @returns {Promise<*|null>}
 */
async function getArticleId() {
    try {
        // 频道列表
        const channelIds = [
            // 推荐
            'a978f44b3e284e5e86777f9d4e3be7bb',
            // 要闻
            '01ff4b46f6bf4e19af6fe88e6320a6c1',
            // 时政
            'ba1f152e715f4ee99e6e13a02f6a218e',
            // 三区
            '0375dc90023f43ffafaf9bc161c30348',
            // 城事
            '0ea24f917ab54157bcd2cecffbf9bfa2'
        ];
        // 随机选择一个频道
        const channelId = channelIds[Math.floor(Math.random() * channelIds.length)];
        // const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/news/content/list`, 'post', headers, {
        //     "channel": {
        //         "id": channelId
        //     },
        //     "pageNo": 1,
        //     "pageSize": 30,
        //     "orderBy": "release_desc",
        //     "requestType": "1",
        //     "siteId": "310110"
        // });
        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/news/content/list`, {
          "channel": {
              "id": channelId
          },
          "pageNo": 1,
          "pageSize": 30,
          "orderBy": "release_desc",
          "requestType": "1",
          "siteId": "310110"
        }, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            console.error('获取新闻列表失败 ->', data.msg)
            return null;
        }
        const articles = data.data.records[Math.floor(Math.random() * data.data.records.length)];
        return articles.id;
    } catch (e) {
        console.error(`获取文章 ID 时发生异常 -> ${e}`);
        return null;
    }
}

/**
 * 收藏文章
 *
 * @returns {Promise<void>}
 */
async function favorArticle(articleId) {
    try {
        // const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/news/content/favor`, 'post', headers, {
        //     "id": articleId,
        //     "orderBy": "release_desc",
        //     "requestType": "2",
        //     "siteId": "310110"
        // });
        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/news/content/favor`, {
          "id": articleId,
          "orderBy": "release_desc",
          "requestType": "2",
          "siteId": "310110"
        }, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            return console.error('收藏文章失败 ->', data.msg);
        }
        console.log(`收藏文章成功\n`);
    } catch (e) {
        console.error(`收藏文章时发生异常 -> ${e}`);
    }
}

/**
 * 文章评论
 *
 * @returns {Promise<void>}
 */
async function commentArticle(articleId) {
    try {
        // 随机评论句子
        const contentList = [
            '👍',
            '👍👍',
            '👍👍👍',
            '好！！',
            '占个楼',
            '加油！',
            '牛！',
            //'这篇文章让我感到非常温暖和鼓舞',
            //'激荡团结奋斗的强大正能量，汇聚起亿万人民团结奋斗的磅礴之力。'
        ];
        const content = contentList[Math.floor(Math.random() * contentList.length)];
        console.log(`随机获取评论句子：[${content}]`);
        // const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/common/comment/add`, 'post', headers, {
        //     "content": content,
        //     "displayResources": [],
        //     "targetId": articleId,
        //     "targetType": "content",
        //     "pageNo": 0,
        //     "pageSize": 10,
        //     "orderBy": "create_desc",
        //     "requestType": "1",
        //     "siteId": "310110"
        // })

        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/common/comment/add`, {
          "content": content,
          "displayResources": [],
          "targetId": articleId,
          "targetType": "content",
          "pageNo": 0,
          "pageSize": 10,
          "orderBy": "create_desc",
          "requestType": "1",
          "siteId": "310110"
        }, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            return console.error('评论文章失败 ->', data.msg, '\n');
        }
        console.log('评论成功\n');
    } catch (e) {
        console.error(`评论文章时发生异常 -> ${e}`);
    }
}

/**
 * 获取积分
 *
 * @returns {Promise<void>}
 */
async function getPoints() {
    try {
        // const data = await sudojia.sendRequest(`${baseUrl}/media-basic-port/api/app/personal/score/info`, 'post', headers, dataBody);

        const res = await axios.post(`${baseUrl}/media-basic-port/api/app/personal/score/info`, dataBody, {
          headers:headers
        });
        const data = res.data;

        if (0 !== data.code) {
            return console.error('获取任务列表失败 ->', data.msg);
        }
        const tasks = data.data.jobs;
        for (const item of tasks) {
            if (['004'].includes(item.id)) {
                continue;
            }
            if ('1' === item.status) {
                message += `【${item.title}】已完成\n`;
            }
        }
        $.points = data.data.totalScore || 0;
        if (data.data.signTitle) {
            console.log(data.data.signTitle);
            message += `${data.data.signTitle}\n`;
        }
        console.log(`当前积分：${$.points}`);
        lastMsg = $.points;
        message += `当前积分：${$.points}\n`;
    } catch (e) {
        console.error(`获取积分时发生异常 -> ${e}`);
    }
}

/**
 * 获取商品列表
 *
 * @returns {Promise<void>}
 */
// async function getGoodsList() {
//     try {
//         const requests = [
//             {
//                 params: 'seller_id=31011001&page_no=1&page_size=10&shop_cat_id=1544652237932859394&sort=create_desc',
//                 type: '限时商品'
//             },
//             {
//                 params: 'keyword=&page_no=1&page_size=20&sort=create_desc&seller_id=31011001&shop_cat_id=1431136756879056898',
//                 type: '虚拟商品'
//             }
//         ];
//         for (const req of requests) {
//             // let data = await sudojia.sendRequest(`https://xxx.com/goods-service/goods/search?${req.params}`, 'get', headers);

//             const res = await axios.get(`https://mall-api.shmedia.tech/goods-service/goods/search?${req.params}`, {
//               headers: headers
//             });
//             const data = res.data;
//             await common.wait(common.getRandomWait(1e3, 2e3));
//             if (!data || !data.data) {
//                 console.error(`${req.type}: data 数据为空`);
//                 continue;
//             }
//             const promotions = data.data.flatMap(item => item.promotion);
//             let hasExchangeableGoods = false;
//             console.log(`${req.type}:`);
//             message += `${req.type}:\n`;
//             for (const ex of promotions) {
//                 const {goods_name, exchange_point} = ex.exchange;
//                 if ($.points >= exchange_point) {
//                     console.log(`可兑换[${goods_name}], 所需[${exchange_point}]积分`);
//                     message += `可兑换[${goods_name}], 所需[${exchange_point}]积分\n`;
//                     hasExchangeableGoods = true;
//                 }
//             }
//             if (!hasExchangeableGoods) {
//                 message += `当前积分暂无商品可兑换\n\n`;
//                 console.log(`当前积分暂无商品可兑换\n`);
//             }
//         }
//     } catch (e) {
//         console.error(`获取商品列表时发生异常 -> ${e}`);
//     }
// }
async function getGoodsList() {
    try {
        const requests = [
            {
                params: 'seller_id=31011001&page_no=1&page_size=10&shop_cat_id=1391586488730075138&sort=create_desc',
                type: '日用百货'
            },
            {
                params: 'seller_id=31011001&page_no=1&page_size=10&shop_cat_id=1386875324743868488&sort=create_desc',
                type: '数码电子'
            },
            {
                params: 'seller_id=31011001&page_no=1&page_size=10&shop_cat_id=1431136756879056898&sort=create_desc',
                type: '虚拟产品'
            },
            {
                params: 'seller_id=31011001&page_no=1&page_size=10&shop_cat_id=1544652237932859394&sort=create_desc',
                type: '限时福利'
            },
        ];

        const detailUrl = function (goodId){
            return `https://mall-api.shmedia.tech/goods-service/goods/${goodId}?goods_id=${goodId}`;
        }

        for (const req of requests) {
            // let data = await sudojia.sendRequest(`https://xxx.com/goods-service/goods/search?${req.params}`, 'get', headers);

            const res = await axios.get(`https://mall-api.shmedia.tech/goods-service/goods/search?${req.params}`, {
              headers: headers
            });
            const data = res.data;
            await common.wait(common.getRandomWait(1e3, 2e3));
            if (!data || !data.data) {
                console.error(`${req.type}: data 数据为空`);
                continue;
            }
            const promotions = data.data.flatMap(item => item.promotion);
            let hasExchangeableGoods = false;
            console.log(`${req.type}:`);

            message += `${req.type}:\n`;
            for (let ei = 0; ei<promotions.length-1; ei++) {
                const ex = promotions[ei];
                const {goods_name, exchange_point, goods_id} = ex.exchange;
                if ($.points >= exchange_point) {

                    await common.wait(common.getRandomWait(1e3, 2e3));
                    const detailRes = await axios.get(detailUrl(goods_id), {
                        headers: headers
                    });
                    const detailData = detailRes.data;

                    if (!detailData) {
                        console.error(`商品详情数据为空`);
                        continue;
                    }

                    const skus = detailData.sku_list[0];

                    if (!skus || skus.enable_quantity == 0) {
                        console.error(`商品剩余数量为空`);
                        continue;
                    }

                    console.log(`可兑换[${goods_name}],库存[${skus.enable_quantity}], 所需[${exchange_point}]积分`);
                    message += `可兑换[${goods_name}],库存[${skus.enable_quantity}], 所需[${exchange_point}]积分\n`;
                    hasExchangeableGoods = true;

                }
            }
            if (!hasExchangeableGoods) {
                message += `当前积分暂无商品可兑换\n\n`;
                console.log(`当前积分暂无商品可兑换\n`);
            }
        }
    } catch (e) {
        console.error(`获取商品列表时发生异常 -> ${e}`);
    }
}
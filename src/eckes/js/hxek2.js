
/**
 *  鸿星尔克 VX小程序    
 * 
 * 10-15      仅签到,随机延迟
 * 
 * 感谢所有测试人员
 * ========= 青龙--配置文件 =========
 * 变量格式: export hongck=' openid & memberId & unionid '   多账号用 换行 或 @ 分割
 *       如 export hongck='xxxxx&xxxxx&xxxxx'      
 * 抓包    hope.demogic.com  域名下的body    , 找到 openid 、 memberId 、 unionid 即可
 * 
 * 
 * ====================================
 */
//1- 已失效 
//1- 已失效
//1- 已失效
//1- 已失效
//1- 已失效
import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
import Env from "../utils/env_plugin.js";
import dayjs from "dayjs";
const $ = new Env("鸿星尔克 VX小程序");
const now = dayjs().format('YYYY-MM-DD HH:mm:ss')
const hongck = [
  {
    memberId:"ff8080819704f28e01970b97b46d52ca",
    unionid:"o36lGwBthNfk7sb3LSUrI4z_HaQk",
    openid:"oXpsg5bZvu8O37NoT5wyzSh12AyI",
  }
];

const timeout = 15000; //超时时间(单位毫秒)
const host = `https://hope.demogic.com`;
let headers = {};
let message = "";
async function main(index) {
  headers = {
    'user-agent': common.getRandomUserAgent(),
    'accept-encoding': 'gzip, deflate, br',
    "Host":"hope.demogic.com",
    'sign':'ff8080817d9fbda8017dc20674f47fb6',
    'referer': 'https://servicewechat.com/wxa1f1fa3785a47c7d/83/page-frame.html',
    'content-type': 'application/json',
    'accept': '*/*',
  };

  await toSign(index);
  await $.wait(common.getRandomWait(800, 1200));
  await getPoints(index);
}

async function toSign(index){
  try {
    const data = await common.sendRequest(`${host}/gic-wx-app/sign/member_sign.json`, 'post', headers, { ...hongck[index],"source":"wxapp","cliqueId":"-1","cliqueMemberId":"-1","useClique":0,"enterpriseId":"ff8080817d9fbda8017dc20674f47fb6","wxOpenid":"oUIO7jispTDbjbgI135W-huWa-gY","sign":"c5cb3c4a22d73ef438e4278824cbced1","random":6426334,"appid":"wxa1f1fa3785a47c7d","transId":"wxa1f1fa3785a47c7d"+now,"timestamp":now,"gicWxaVersion":"3.9.54","launchOptions":"{\"path\":\"pages/authorize/authorize\",\"query\":{},\"scene\":1256,\"referrerInfo\":{},\"apiCategory\":\"default\"}"}
    );
    if ('0' != data.code) {
      message += `${index}:失败:${data.message||data.errmsg}\n`
      return;
    }
  } catch (e) {
    console.log(e)
      message += `${index}:失败:${e}\n`
  }
}

/**
 * 获取积分https://hope.demogic.com/gic-wx-app/integral_record.json 
 *
 * @return {Promise<void>}
 */
async function getPoints(index) {
  try {
    const data = await common.sendRequest(`${host}/gic-wx-app/integral_record.json`, 'get', headers);
    if ('0' != data.errcode) {
        notification.pushMessage({
          title: "鸿星小程序-失败",
          content: `获取积分失败`,
          msgtype: "text"
        });
        return;
    }
    message += `${index}：${data.response.accumulatPoints}\n`;
  } catch (e) {
    message += `${index}:失败:${data.errmsg||data.message}\n`
  }
}

!(async () => {
  for (let i = 0; i < hongck.length; i++) {
      await main(i);
      await $.wait(common.getRandomWait(2000, 2500));
  }
  if (message) {
    notification.pushMessage({
      title: "鸿星小程序",
      content: `${message}`,
      msgtype: "text"
    });
  }
})().catch((e) => $.logErr(e)).finally(() => $.done());
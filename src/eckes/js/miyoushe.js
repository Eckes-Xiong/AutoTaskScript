import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
// import Env from "../utils/env_plugin.js";
// const $ = new Env("米游社-原神签到");

const timeout = 15000; //超时时间(单位毫秒)
//const ck = process.env.MIHOYO_COOKIE;
//const json = {"act_id":"e202311201442471","region":"cn_gf01","uid":"100631479","lang":"zh-cn"};
const url = `https://api-takumi.mihoyo.com/event/luna/hk4e/sign`;

const jsons = [
    {"act_id":"e202311201442471","region":"cn_gf01","uid":"100631479","lang":"zh-cn"},
    //{"act_id":"e202311201442471","region":"cn_gf01","uid":"134556687","lang":"zh-cn"},
]
const hs = [
    {
        'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 18_7 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) miHoYoBBS/2.94.1',
        'x-rpc-device_model': 'iPhone15,4',
        'x-rpc-device_fp': '38d7f65582eef',
        'x-rpc-app_version': '2.94.1',
        'DS': '1772415137,RhyLtl,fed08764a78b7ec32ecec967d704ffcc',
        'x-rpc-device_id': '01AF9A57F1BB4C77B3A64A6A055F3261',
        'Cookie':"account_id_v2=21872820; account_mid_v2=0auuz7m4ey_mhy; cookie_token_v2=v2_rpzGwfkJpXo-XI1Wvs0nONKNrcNMtD79boZUFb9woMTdzjD2CTW1G9lu9EXXwWwuziprhVGYOi1l5JZvAGN09TSEV0pfYVrFKX3pV2_fP3NDSp17OEBtKA43VNpVhwKxN-1Od0aaGM0cnPm8Nw==.CAE=; ltmid_v2=0auuz7m4ey_mhy; ltoken_v2=v2_zPgc0qS-CgbeASQT36Pp3Jqh9sb83nAQrh0w9C4d7WkQG4k71I7DoVl_vzzVi6XPTuJDrN3IrrRfVtrL4yreh2JyN2MCAEyDlcFuBGkIlYfLTx9prSrqL6OLsmwFw7WMimGgcZsm7wcxFRis.CAE=; ltuid_v2=21872820; DEVICEFP=38d803ce4b4d8; DEVICEFP_SEED_ID=2f287b74782b430a; DEVICEFP_SEED_TIME=1737350518142; _MHYUUID=91844ec3-56d4-473a-9527-528ac3b0d138; aliyungf_tc=e109163d6947322c2098e6d528e4131241fbf158848dcd0bb68e6681860a7f7c; mi18nLang=zh-cn; account_id=21872820; cookie_token=v2_rpzGwfkJpXo-XI1Wvs0nONKNrcNMtD79boZUFb9woMTdzjD2CTW1G9lu9EXXwWwuziprhVGYOi1l5JZvAGN09TSEV0pfYVrFKX3pV2_fP3NDSp17OEBtKA43VNpVhwKxN-1Od0aaGM0cnPm8Nw==.CAE=; login_ticket=dvzfUgaACcnAXqqTlo4jIIa5zmF6fPfm8YLfZzRt; ltoken=v2_zPgc0qS-CgbeASQT36Pp3Jqh9sb83nAQrh0w9C4d7WkQG4k71I7DoVl_vzzVi6XPTuJDrN3IrrRfVtrL4yreh2JyN2MCAEyDlcFuBGkIlYfLTx9prSrqL6OLsmwFw7WMimGgcZsm7wcxFRis.CAE=; ltuid=21872820; _ga=GA1.2.1767840600.1737350518; _gat_gtag_UA_133007358_5=1; _gid=GA1.2.808325486.1772415115; _ga_M91EY72BM9=GS2.1.s1771821486$o8$g0$t1771821486$j60$l0$h0; _ga_K2F0P1NR6Z=GS2.1.s1762348107$o2$g0$t1762348107$j60$l0$h0; _ga_CGERVQ03CP=GS2.1.s1760665363$o1$g1$t1760665370$j53$l0$h0; _ga_QYFFEX7F52=GS2.1.s1760665362$o1$g1$t1760665370$j52$l0$h0; _ga_BD1DQ36T3G=GS2.1.s1749384745$o1$g0$t1749384745$j60$l0$h0; _ga_XCB7DK0YVT=deleted; _ga_VTB4FCEHT7=GS1.1.1738243806.3.1.1738243969.0.0.0",
    },
];

let send_str = "";
let title_str = "";

function sendSign(i){
    return common.sendRequest(url, "post", {
        'Content-Type': 'application/json;charset=utf-8',
        'Host': 'api-takumi.mihoyo.com',
        'Referer': 'https://act.mihoyo.com/',
        'x-rpc-platform': '1',
        'x-rpc-device_name': 'iPhone',
        'Origin': 'https://act.mihoyo.com',
        'x-rpc-signgame': 'hk4e',
        'Sec-Fetch-Site': 'same-site',
        'x-rpc-client_type': '5',
        'Sec-Fetch-Mode': 'cors',
        ...hs[i],
    },jsons[i]) 
}
async function mihoyo_sign(){
    try{
        for(let i=0; i<hs.length; i++){
           const res = await sendSign(i)
            if (data.message === "OK") {
                send_str += `${i+1}:成功。`
                title_str += `${i+1};`
            } else {
                send_str += `${i+1}:失败。`
                title_str += `${i+1}x;`
            }
        }
        notification.pushMessage({
            title: "原神签到" + title_str,
            content: "结果:"+send_str,
            msgtype: "text"
        });
    }catch(e){
        console.log(e);
        notification.pushMessage({
            title: "原神签到失败",
            content: "结果:"+e,
            msgtype: "text"
        });
    }
}
mihoyo_sign()

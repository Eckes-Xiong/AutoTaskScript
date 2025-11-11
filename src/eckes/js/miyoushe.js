import notification from "../utils/notification-kit.js";
import common from "../utils/common.js";
import Env from "../utils/env_plugin.js";
const $ = new Env("米游社-原神签到");

const timeout = 15000; //超时时间(单位毫秒)
//const ck = process.env.MIHOYO_COOKIE;
//const json = {"act_id":"e202311201442471","region":"cn_gf01","uid":"100631479","lang":"zh-cn"};
const url = `https://api-takumi.mihoyo.com/event/luna/hk4e/sign`;

const jsons = [
    {"act_id":"e202311201442471","region":"cn_gf01","uid":"100631479","lang":"zh-cn"},
    {"act_id":"e202311201442471","region":"cn_gf01","uid":"134556687","lang":"zh-cn"},
]
const hs = [
    {
        'x-rpc-device_model': 'iPhone15,4',
        'x-rpc-device_fp': '38d7f65582eef',
        'x-rpc-app_version': '2.75.2',
        'DS': '1735540481,rjHxek,caa1275dfa980a00756c5c446b3af79a',
        'x-rpc-device_id': '01AF9A57F1BB4C77B3A64A6A055F3261',
        'Cookie':"account_id_v2=21872820; account_mid_v2=0auuz7m4ey_mhy; cookie_token_v2=v2_45dK_WtEsNbcGi1DzSWNMfGAuAY7akiTMAalLlCMOVFYTcEoqTkyNgSu7lT6jX4aAgQSm9sT8SHd6-aEhe6K6K_gisRFEpo8ZkYitbHOO8RL10h2zyYttmCtyFnr7bAZdt4LBJvxv47hMq8QRQ==.CAE=; ltmid_v2=0auuz7m4ey_mhy; ltoken_v2=v2_zPgc0qS-CgbeASQT36Pp3Jqh9sb83nAQrh0w9C4d7WkQG4k71I7DoVl_vzzVi6XPTuJDrN3IrrRfVtrL4yreh2JyN2MCAEyDlcFuBGkIlYfLTx9prSrqL6OLsmwFw7WMimGgcZsm7wcxFRis.CAE=; ltuid_v2=21872820; DEVICEFP=38d8001f5b6d9; DEVICEFP_SEED_ID=3742756737c077b2; DEVICEFP_SEED_TIME=1730419266415; _MHYUUID=ae07aee3-1027-41a9-93b6-a800ef3a1562; _ga=GA1.2.2145990939.1730419266; _ga_MRQ1MZMMEE=GS1.1.1735540451.11.0.1735540470.0.0.0; _gid=GA1.2.1480199221.1735460194; account_id=21872820; cookie_token=v2_45dK_WtEsNbcGi1DzSWNMfGAuAY7akiTMAalLlCMOVFYTcEoqTkyNgSu7lT6jX4aAgQSm9sT8SHd6-aEhe6K6K_gisRFEpo8ZkYitbHOO8RL10h2zyYttmCtyFnr7bAZdt4LBJvxv47hMq8QRQ==.CAE=; login_ticket=dvzfUgaACcnAXqqTlo4jIIa5zmF6fPfm8YLfZzRt; ltoken=v2_zPgc0qS-CgbeASQT36Pp3Jqh9sb83nAQrh0w9C4d7WkQG4k71I7DoVl_vzzVi6XPTuJDrN3IrrRfVtrL4yreh2JyN2MCAEyDlcFuBGkIlYfLTx9prSrqL6OLsmwFw7WMimGgcZsm7wcxFRis.CAE=; ltuid=21872820; mi18nLang=zh-cn; aliyungf_tc=6f7b386ff5c22a7d959efb8a6883fdcb66743676a41e92ef9966b0aa6d5b97a4; _gat_gtag_UA_133007358_35=1; _ga_M91EY72BM9=GS1.1.1735260195.8.0.1735260196.0.0.0; _ga_SNHQ9DMDFJ=GS1.1.1734945960.1.0.1734945961.0.0.0; _ga_29PCTL5P98=GS1.1.1734748594.1.0.1734748594.0.0.0; _ga_CXN1FSHKS4=GS1.1.1734748594.1.0.1734748594.0.0.0; _ga_H728700W1R=GS1.1.1734660696.1.1.1734660702.0.0.0; _ga_DNM1PJ22XW=GS1.1.1734660696.1.0.1734660701.0.0.0; _ga_CGERVQ03CP=GS1.1.1734356740.1.0.1734356741.0.0.0; _ga_QYFFEX7F52=GS1.1.1734356740.1.0.1734356741.0.0.0; _ga_EPYDNQRM6D=GS1.1.1731888532.1.1.1731888787.0.0.0; _ga_HB2EBLW929=GS1.1.1730961439.5.0.1730961442.0.0.0; _ga_J1K3VE5FNG=GS1.1.1730961440.5.0.1730961442.0.0.0",
    },
    {
        'x-rpc-device_model': 'iPhone16,1',
        'x-rpc-device_fp': '38d7f1060be87',
        'x-rpc-app_version': '2.80.0',
        'DS': '1736930242,qBlptS,8326e1bba3d1b6a2bc1ed944d04a62e4',
        'x-rpc-device_id': '01AF9A57F1BB4C77B3A64A6A055F3261',
        'Cookie':"account_id_v2=225874162; account_mid_v2=0wulwsjkav_mhy; cookie_token_v2=v2_NoljfNy_BBs6icnFEtmm5eP3uMHn_kMuc4YNoICXpwFqr3wVmtrDL-BzXHCY5Zsugki4kD8WjaJHzV47D1RrRJe7ol2Jt_qAkw_OyHcEWztgN3PkfzZ56qTGaZfpHfFzilnYUXM2r2AtHLI=.CAE=; DEVICEFP=38d7f8b171936; ltmid_v2=0wulwsjkav_mhy; ltoken_v2=v2_9Q8r77286kIxOb2s2lCFsDaSo_XyYVXMglqewv_ObvdNkp0Ap-111Nau7T1JMrT2pUoYEqLPJ2p1gK2VC0-gbPr09oSBqGUizuPMjxNeBh1R3slMuz2bWcyPVgI2N1IBTT6znWtqzHQcMLc=.CAE=; ltuid_v2=225874162; aliyungf_tc=d9810863fda24bdbb168c42aa62dbf743ad49c5f20d9f376bdeca663624a4f5a; DEVICEFP_SEED_ID=2103cdd34fe4b0b0; DEVICEFP_SEED_TIME=1697066751139; _MHYUUID=03b15a65-530a-41ea-998f-20dccb811af5; _ga=GA1.2.138942225.1697030794; _ga_MRQ1MZMMEE=GS1.1.1736930227.383.0.1736930227.0.0.0; _gat_gtag_UA_133007358_35=1; _gid=GA1.2.441291911.1736930224; mi18nLang=zh-cn; account_id=225874162; cookie_token=v2_NoljfNy_BBs6icnFEtmm5eP3uMHn_kMuc4YNoICXpwFqr3wVmtrDL-BzXHCY5Zsugki4kD8WjaJHzV47D1RrRJe7ol2Jt_qAkw_OyHcEWztgN3PkfzZ56qTGaZfpHfFzilnYUXM2r2AtHLI=.CAE=; login_ticket=UXlwyMwlNOtDzIa2JjWWyYMs48UB6lOgnP6JMxYh; ltoken=v2_9Q8r77286kIxOb2s2lCFsDaSo_XyYVXMglqewv_ObvdNkp0Ap-111Nau7T1JMrT2pUoYEqLPJ2p1gK2VC0-gbPr09oSBqGUizuPMjxNeBh1R3slMuz2bWcyPVgI2N1IBTT6znWtqzHQcMLc=.CAE=; ltuid=225874162; _gat_gtag_UA_133007358_5=1; _ga_M91EY72BM9=GS1.1.1736583962.144.0.1736583962.0.0.0; _ga_SNHQ9DMDFJ=GS1.1.1735744829.3.1.1735744884.0.0.0; _ga_3489XT4FH6=GS1.1.1735607683.1.1.1735607879.0.0.0; _ga_BWZ3QXYM9R=GS1.1.1735256028.1.1.1735256043.0.0.0; _ga_00MJSJTX01=GS1.1.1734269896.5.1.1734269933.0.0.0; _ga_9TTX3TE5YL=GS1.1.1733553344.29.1.1733553773.0.0.0; _ga_EPYDNQRM6D=GS1.1.1731676875.1.1.1731677011.0.0.0; _ga_CGERVQ03CP=GS1.1.1728785618.3.0.1728785618.0.0.0; _ga_QYFFEX7F52=GS1.1.1728785618.3.0.1728785618.0.0.0; _ga_BY66DLFS37=GS1.1.1724408088.3.1.1724408241.0.0.0; _ga_29PCTL5P98=GS1.1.1721037704.2.0.1721037705.0.0.0; _ga_CXN1FSHKS4=GS1.1.1721037703.2.0.1721037705.0.0.0; _ga_SS6YDYJ9SQ=GS1.1.1720518980.1.1.1720519228.0.0.0; _ga_FF7GK0SSGX=GS1.1.1717909014.18.0.1717909015.0.0.0; _ga_2HSB7QF0KJ=GS1.1.1717909014.18.0.1717909014.0.0.0; _ga_G77KS31Q0V=GS1.1.1714791816.6.1.1714791923.0.0.0; _ga_TNKZGZ607P=GS1.1.1712034411.2.1.1712034523.0.0.0; _ga_HB2EBLW929=GS1.1.1711967090.8.0.1711967096.0.0.0; _ga_J1K3VE5FNG=GS1.1.1711967091.8.0.1711967096.0.0.0; _ga_ZY0YM68HK0=GS1.1.1709509366.1.1.1709509472.0.0.0; _ga_BGFQM8L1FY=GS1.1.1707845791.5.1.1707845845.0.0.0; _ga_6C02QT42ND=GS1.1.1705919215.8.0.1705919215.0.0.0; _ga_D2HF9XKYED=GS1.1.1704190267.6.1.1704190283.0.0.0; _ga_P308KCCFXP=GS1.1.1703829803.1.0.1703829804.0.0.0; _ga_RE2E3BQ1DH=GS1.1.1703829804.1.0.1703829804.0.0.0; _ga_DNM1PJ22XW=GS1.1.1703567986.1.0.1703567986.0.0.0; _ga_H728700W1R=GS1.1.1703567986.1.1.1703567986.0.0.0; _ga_9Z5R2R4LNF=GS1.1.1702855834.1.1.1702855840.0.0.0; _ga_KKFDZZK28F=GS1.1.1702855834.1.0.1702855840.0.0.0; _ga_K2F0P1NR6Z=GS1.1.1702855832.1.0.1702855832.0.0.0"
    },
    // {
    //     'x-rpc-device_model': 'iPhone11,8',
    //     'x-rpc-device_fp': '38d7ebced4ae1',
    //     'x-rpc-app_version': '2.82.0',
    //     'DS': '1739967118,6SDOME,1b62e2cc260b8927aa9d7c5af9f5d16a',
    //     'x-rpc-device_id': '7BB4838F-7F7F-474D-B5C7-A04B8F274E05',
    //     'Cookie':"account_id_v2=332868108; account_mid_v2=09ux3gcsd0_mhy; cookie_token_v2=v2_oQhjfuXTBVWkxongNn5mEegS8k5bShw72QnNR8tz5GhMBaqlchd08rzpSy0VKQwqQ-YoEoPyu3uCGYhRv9i-bVry0Jm_WU_HnsL-BKiW0Am9pip-CPOL0cKt1MENSWMHedif1XwVlXffUspV.CAE=; DEVICEFP=38d805736373b; ltmid_v2=09ux3gcsd0_mhy; ltoken_v2=v2_CtC1npCeXKBQnS114Ff07iaiqHK_OfxyjK6ws0YF6OsHNvmOn7926K2sgHNLjzVqsQ6WPF_CCkSsF7Q5yKeidi7wYYrz6CGy8lq_3X0ZZGS5moX8woDXoGIsyOi2_JN4z0QkCzBUomkKPGVg.CAE=; ltuid_v2=332868108; aliyungf_tc=6a9b0a0f2484b69b93913c39e0e673d3c3422346cfca7c33706cb57f43a0428f; DEVICEFP_SEED_ID=de7e1eeb63fffd0f; DEVICEFP_SEED_TIME=1739967041572; _MHYUUID=1361d5eb-93f2-42d6-8c66-57b4f7e782be; _ga=GA1.2.1551966345.1739967043; _ga_MRQ1MZMMEE=GS1.1.1739967112.1.0.1739967112.0.0.0; _gat_gtag_UA_133007358_35=1; _gid=GA1.2.780009623.1739967043; mi18nLang=zh-cn; account_id=332868108; cookie_token=v2_oQhjfuXTBVWkxongNn5mEegS8k5bShw72QnNR8tz5GhMBaqlchd08rzpSy0VKQwqQ-YoEoPyu3uCGYhRv9i-bVry0Jm_WU_HnsL-BKiW0Am9pip-CPOL0cKt1MENSWMHedif1XwVlXffUspV.CAE=; login_ticket=DZ9LSwH8Ao55mqPj8e8mfrBeC8Vz4vjANXsSCiwo; ltoken=v2_CtC1npCeXKBQnS114Ff07iaiqHK_OfxyjK6ws0YF6OsHNvmOn7926K2sgHNLjzVqsQ6WPF_CCkSsF7Q5yKeidi7wYYrz6CGy8lq_3X0ZZGS5moX8woDXoGIsyOi2_JN4z0QkCzBUomkKPGVg.CAE=; ltuid=332868108"
    
    // }
];

let send_str = "";
let title_str = "";

async function mihoyo_sign(i) {

  await new Promise( async (resolve) => {
    try {
      const res = await common.sendRequest(url, "post", {
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

      let data = res.data;

      if (err) {
        console.log('调用API失败！！\n');
      } else {
        data = JSON.parse(data);
        if (data.message === "OK") {
          send_str += `${i+1}:🎉。`
        } else {
          send_str += `${i+1}:❎。`
          title_str += `${i+1}x;`
        }
        resolve();
      }
    } catch (e) {
      send_str += `${i+1}:✖。`
      title_str += `${i+1}x;`
    } finally {
      resolve();
    }
  });

  await new Promise(resolve => setTimeout(resolve, Math.random()*12000*(i+1)));

}

for(let i=0; i<hs.length; i++){
    mihoyo_sign(i)
}

setTimeout(() => {
  notification.pushMessage({
    title: "原神签到" + title_str,
    content: send_str,
    msgtype: "text"
  });
}, 40);
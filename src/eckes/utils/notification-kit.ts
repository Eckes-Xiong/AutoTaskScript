import axios from "axios";
import env from "./env";

interface NotificationOptions {
  title: string;
  content: string;
  msgtype?: "text" | "html";
}

interface PushPlusOptions extends NotificationOptions {}

export class NotificationKit {
  /**
   * PushPlus推送
   * @param options
   */
  async pushplus(options: PushPlusOptions) {
    const token: string | unknown = env.PUSHPLUS_TOKEN;
    if (!token || token === "") {
      throw new Error("未配置PushPlus Token。");
    }

    const config = {
      token,
      title: options.title,
      content: options.content,
      topic: "",
      template: "html",
      channel: "wechat",
      webhook: "",
      callbackUrl: "",
      timestamp: ""
    };

    return axios.post("http://www.pushplus.plus/send", config, {
      headers: {
        "Content-Type": "application/json"
      }
    });
  }
  async pushMessage(options: NotificationOptions) {
    const trycatch = async (name: string, fn: Function) => {
      try {
        await fn(options);
        console.log(`[${name}]: 消息推送成功!`);
      } catch (e: any) {
        console.log(`[${name}]: 消息推送失败! 原因: ${e.message}`);
      }
    };

    await trycatch("PushPlus", this.pushplus.bind(this));
  }
}

export default new NotificationKit();
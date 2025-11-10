import axios from "axios";

export class NotificationKit {
  /**
   * PushPlus推送
   * @param options
   */
  async pushplus(options) {
    const token = "a1dfe7a5c3b94a82a4f8e51dd874dbce";
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
  async pushMessage(options) {
    const trycatch = async (name, fn) => {
      try {
        await fn(options);
        console.log(`[${name}]: 消息推送成功!`);
      } catch (e) {
        console.log(`[${name}]: 消息推送失败! 原因: ${e.message}`);
      }
    };

    await trycatch("PushPlus", this.pushplus.bind(this));
  }
}
const notify = new NotificationKit();
export default notify
const nameRules: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) => (v && v.length <= 10) || "Must be less than 10 characters",
];

const emailRules: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) => /.+@.+\..+/.test(v) || "Invalid Email",
];

const numberRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) => Number.isInteger(Number(v)) || "Value must be a positive integer",
  (v) => v > 0 || "Value must be greater than zero",
];

const emptyRule: Array<(v: any) => any> = [(v) => !!v || "Required"];

const titleRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) => (v && v.length <= 15) || "Must be less than 15 characters",
];

const telegramUrlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp(
      "^https?://api\\.telegram\\.org/bot\\d{4,}:[\\w_]{4,}/sendMessage\\?chat_id=-\\d{4,}$"
    ).test(v) || "Invalid Telegram webhook",
];

const slackUrlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp(
      "^https?://hooks\\.slack\\.com/services/[\\d\\w]{4,}/[\\d\\w]{4,}/[\\d\\w]{4,}$"
    ).test(v) || "Invalid Slack webhook",
];

const discordUrlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp(
      "^https?://discord\\.com/api/webhooks/\\d{4,}/[\\d\\w_-]{4,}$"
    ).test(v) || "Invalid Discord webhook",
];

const gotifyUrlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp("^https?://[\\w\\d.:-]*/message\\?token=[\\d\\w-]{4,}$").test(
      v
    ) || "Invalid Gotify webhook",
];

const webhookUrlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp(
      "^(https?:\\/\\/)?" + // protocol
        "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
        "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
        "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
        "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
        "(\\#[-a-z\\d_]*)?$",
      "i"
    ).test(v) || "Invalid webhook",
];

const urlRule: Array<(v: any) => any> = [
  (v) => !!v || "Required",
  (v) =>
    new RegExp(
      "^(https?:\\/\\/)?" + // protocol
        "((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|" + // domain name
        "((\\d{1,3}\\.){3}\\d{1,3}))" + // OR ip (v4) address
        "(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*" + // port and path
        "(\\?[;&a-z\\d%_.~+=-]*)?" + // query string
        "(\\#[-a-z\\d_]*)?$",
      "i"
    ).test(v) || "Invalid URL",
];

const rules = {
  nameRules,
  emailRules,
  numberRule,
  emptyRule,
  titleRule,
  telegramUrlRule,
  slackUrlRule,
  discordUrlRule,
  gotifyUrlRule,
  webhookUrlRule,
  urlRule,
};

export default rules;

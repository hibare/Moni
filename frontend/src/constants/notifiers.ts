import rules from "../utils/rules";

export const NotifierTypeMap: Record<string, Record<string, any>> = {
  slack: {
    icon: "fa-brands fa-slack",
    color: "red",
    rule: rules.slackUrlRule,
  },
  telegram: {
    icon: "fa-brands fa-telegram",
    color: "light-blue-6",
    rule: rules.telegramUrlRule,
  },
  discord: {
    icon: "fa-brands fa-discord",
    color: "indigo-13",
    rule: rules.discordUrlRule,
  },
  gotify: {
    icon: "chat_bubble_outline",
    color: "green-8",
    rule: rules.gotifyUrlRule,
  },
  webhook: {
    icon: "webhook",
    color: "brown-8",
    rule: rules.webhookUrlRule,
  },
};

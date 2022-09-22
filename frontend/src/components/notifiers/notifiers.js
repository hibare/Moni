import { slackUrlRule } from "@/mixins/rulesMixin";

const notifiersMap = {
    slack: {
        icon: "mdi-slack",
        name: "Slack",
        fields: [{
            name: "url",
            type: "text",
            rule: slackUrlRule
        }]
    },
    telegram: {
        icon: "mdi-send-circle",
        name: "Telegram",
    },
    discord: {
        icon: "mdi-discord",
        name: "Discord",
    },
    gotify: {
        icon: "mdi-message",
        name: "Gotify",
    },
    webhook: {
        icon: "mdi-webhook",
        name: "Webhook",
    }
}

export default notifiersMap
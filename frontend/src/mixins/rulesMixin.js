/* eslint-disable no-useless-escape */
export default {
    data: () => ({

        // Validate name of 10 chars
        nameRules: [
            (v) => !!v || "Required",
            (v) => (v && v.length <= 10) || "Must be less than 10 characters",
        ],

        // Validate email
        emailRules: [
            (v) => !!v || "Required",
            (v) => /.+@.+\..+/.test(v) || "Invalid Email",
        ],

        // Validate password
        emptyRule: [(v) => !!v || "Required"],

        // Valid title
        titleRule: [
            (v) => !!v || "Required",
            (v) => (v && v.length <= 15) || "Must be less than 15 characters",
        ],

        // Telegram webhook rule
        telegramUrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp(
                "^https?:\/\/api\\.telegram\\.org\/bot\\d{4,}:[\\w_]{4,}\/sendMessage\\?chat_id=-\\d{4,}$"
            ).test(v) || "Invalid Telegram webhook",
        ],

        // Slack webhook rule
        slackUrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp(
                "^https?:\/\/hooks\\.slack\\.com\/services\/[\\d\\w]{4,}\/[\\d\\w]{4,}\/[\\d\\w]{4,}$"
            ).test(v) || "Invalid Slack webhook",
        ],

        // Discord webhook rule
        discordUrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp(
                "^https?:\/\/discord\\.com\/api\/webhooks\/\\d{4,}\/[\\d\\w_-]{4,}$"
            ).test(v) || "Invalid Discord webhook",
        ],

        // Gotify webhook rule
        gotifyUrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp(
                "^https?:\/\/[\\w\\d.:-]*\/message\\?token=[\\d\\w-]{4,}$"
            ).test(v) || "Invalid Gotify webhook",
        ],

        // webhook  rule
        webhookUrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp('^(https?:\\/\\/)?' + // protocol
                '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
                '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
                '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
                '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
                '(\\#[-a-z\\d_]*)?$', 'i').test(v) || "Invalid webhook",
        ],

        // URL rule
        UrlRule: [
            (v) => !!v || "Required",
            (v) => new RegExp('^(https?:\\/\\/)?' + // protocol
                '((([a-z\\d]([a-z\\d-]*[a-z\\d])*)\\.)+[a-z]{2,}|' + // domain name
                '((\\d{1,3}\\.){3}\\d{1,3}))' + // OR ip (v4) address
                '(\\:\\d+)?(\\/[-a-z\\d%_.~+]*)*' + // port and path
                '(\\?[;&a-z\\d%_.~+=-]*)?' + // query string
                '(\\#[-a-z\\d_]*)?$', 'i').test(v) || "Invalid URL",
        ],
    }),
    methods: {}
};
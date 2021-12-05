export default {
    data: () => ({
    }),
    methods: {
        getPrettyDate(d) {
            // Convert zulu date string to pretty date string (local)

            if (Object.prototype.toString.call(d) !== "[object Date]")
                d = new Date(d)

            const today = new Date()
            const yesterday = new Date(today)

            yesterday.setDate(yesterday.getDate() - 1)

            if (today.toDateString() === d.toDateString()) { // Today
                return "Today " + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
            } else if (yesterday.toDateString() === d.toDateString()) { // Yesterday
                return "Yesterday " + d.toLocaleTimeString('en-US', { hour: 'numeric', minute: 'numeric', hour12: true })
            } else {
                return d.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric', hour: 'numeric', minute: 'numeric', hour12: true })
            }
        }
    }
};
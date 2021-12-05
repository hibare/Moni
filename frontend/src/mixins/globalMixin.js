import { mapGetters } from 'vuex'

export default {
    data: () => ({
        appName: 'Moni',
        githubBaseURL: "https://github.com/",
        githubAPIBaseURL: "https://api.github.com/repos/",
    }),

    computed: {

        ...mapGetters({
            getGitOwner: 'git/getGitOwner',
            getGitRepo: 'git/getGitRepo',
            getGitStars: 'git/getGitStars',
            getGitForks: 'git/getGitForks'
        }),


    },

    methods: {
        getAppName() {
            return this.appName;
        },

        setGitData() {
            var url = this.getGitAPIURL();
            this.$http.get(url).then((result) => {
                this.$store.dispatch('git/updateGitRepoData', result['data'])
            });
        },

        getGitURL() {
            return this.githubBaseURL + this.getGitOwner + "/" + this.getGitRepo;
        },

        getGitAPIURL() {
            return this.githubAPIBaseURL + this.getGitOwner + "/" + this.getGitRepo;
        },

        getCurrentYear() {
            return new Date().getFullYear();
        },

        getPrettyStatusIcon(val) {
            return val ? "mdi-check" : "mdi-close";
        },

        getStatusColor(val) {
            return val ? "green accent-3" : "pink accent-2";
        },

        fillEmptyValue(val) {
            return val ? val : "-";
        },
    }
}
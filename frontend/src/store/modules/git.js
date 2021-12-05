
// Initial state
const state = () => ({
    gitOwner: 'hibare',
    gitRepo: 'moni',
    gitStars: '',
    gitForks: '',
    gitRepoData: null,
})

// getters
const getters = {
    getGitStars: (state) => {
        return state.gitStars;
    },

    getGitForks: (state) => {
        return state.gitForks;
    },

    getGitOwner: (state) => {
        return state.gitOwner;
    },

    getGitRepo: (state) => {
        return state.gitRepo;
    }
}

// actions
const actions = {
    updateGitRepoData({ commit }, data) {
        var stars = data["stargazers_count"]
        var forks = data["forks"]

        commit('setGitRepoData', data)
        commit('setRepoStars', stars)
        commit('setRepoForks', forks)
    }
}

// mutations
const mutations = {
    setGitRepoData(state, data) {
        state.gitRepoData = data
    },

    setRepoStars(state, val) {
        state.gitStars = val
    },

    setRepoForks(state, val) {
        state.gitForks = val
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
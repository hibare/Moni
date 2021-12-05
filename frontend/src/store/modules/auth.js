// Initial state
const state = () => ({
    accessToken: null,
    refreshToken: null,
    firstname: null,
    lastname: null,
    fullname: null,
    email: null,
    isLoggedin: false,
})

// getters

const getters = {
    getAccessToken: (state) => state.accessToken,

    getFirstname: (state) => state.firstname,

    getLastname: (state) => state.lastname,

    getFullname: (state) => state.fullname,

    getEmail: (state) => state.email,

    isLoggedin: (state) => state.isLoggedin,
}

// actions
const actions = {
    login({ commit }, payload) {
        var data = {
            isLoggedin: true,
            accessToken: payload.access,
            refreshToken: payload.refresh,
            firstname: payload.firstname,
            lastname: payload.lastname,
            fullname: payload.fullname,
            email: payload.email,
        }
        commit('setAuth', data)
    },

    logout({ commit }) {
        var data = {
            isLoggedin: false,
            accessToken: null,
            refreshToken: null,
            firstname: null,
            lastname: null,
            fullname: null,
            email: null,
        }
        commit('setAuth', data)
    }
}

// mutations
const mutations = {
    setAuth(state, data) {
        state.isLoggedin = data.isLoggedin;
        state.accessToken = data.accessToken;
        state.refreshToken = data.refreshToken;
        state.firstname = data.firstname;
        state.lastname = data.lastname;
    }
}

export default {
    namespaced: true,
    state,
    getters,
    actions,
    mutations
}
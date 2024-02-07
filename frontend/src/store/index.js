import { createStore } from "vuex"
import { verifyResponse } from "../utils"

const store = createStore({
  state() {
    return {
      loggedUser: null,
      initialDataLoaded: false,
    }
  },
  mutations: {
    setLoggedUser(state, user) {
      state.loggedUser = user
    },
    setInitialDataLoaded(state) {
      state.initialDataLoaded = true
    },
  },
  actions: {
    fetchInitialData(context) {
      return context.dispatch("fetchLoggedUser").then(() => context.commit("setInitialDataLoaded"))
    },
    fetchLoggedUser(context) {
      return fetch("/api/v1/loggedUser/")
        .then(verifyResponse)
        .then((response) => {
          context.commit("setLoggedUser", response || null)
        })
        .catch((e) => {
          console.error("fetchLoggedUser", e)
        })
    },
  },
})
export default store

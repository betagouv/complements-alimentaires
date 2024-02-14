import { defineStore } from "pinia"
import { verifyResponse } from "../utils"
import { ref } from "vue"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)

  function fetchInitialData() {
    return fetchLoggedUser().then(() => (initialDataLoaded.value = true))
  }
  function fetchLoggedUser() {
    return fetch("/api/v1/loggedUser/")
      .then(verifyResponse)
      .then((response) => {
        loggedUser.value = response || null
      })
      .catch((e) => {
        console.error("fetchLoggedUser", e)
      })
  }

  return { loggedUser, initialDataLoaded, fetchInitialData, fetchLoggedUser }
})

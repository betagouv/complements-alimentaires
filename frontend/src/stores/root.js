import { defineStore } from "pinia"
import { verifyResponse } from "../utils/custom-errors"
import { ref } from "vue"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)

  const fetchInitialData = () => {
    return fetchLoggedUser().then(() => (initialDataLoaded.value = true))
  }
  const fetchLoggedUser = () => {
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

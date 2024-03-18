import { defineStore } from "pinia"
import { verifyResponse } from "../utils/custom-errors"
import { useFetch } from "@vueuse/core"
import { ref } from "vue"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const populations = ref(null)
  const conditions = ref(null)
  const plantParts = ref(null)

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
  const resetInitialData = () => {
    loggedUser.value = null
    initialDataLoaded.value = null
  }

  const fetchPopulations = async () => {
    const { data } = await useFetch("/api/v1/populations/").json()
    populations.value = data.value
  }
  const fetchConditions = async () => {
    const { data } = await useFetch("/api/v1/conditions/").json()
    conditions.value = data.value
  }
  const fetchPlantParts = async () => {
    const { data } = await useFetch("/api/v1/plantParts/").json()
    plantParts.value = data.value
  }
  return {
    loggedUser,
    initialDataLoaded,
    fetchInitialData,
    resetInitialData,
    fetchLoggedUser,
    fetchPopulations,
    fetchConditions,
    fetchPlantParts,
    plantParts,
    populations,
    conditions,
  }
})

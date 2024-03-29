import { defineStore } from "pinia"
import { useFetch } from "@vueuse/core"
import { ref } from "vue"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const populations = ref(null)
  const conditions = ref(null)
  const plantParts = ref(null)
  const units = ref(null)

  const fetchInitialData = async () => {
    await fetchLoggedUser()
    initialDataLoaded.value = true
  }

  const fetchLoggedUser = async () => {
    const { data } = await useFetch("/api/v1/loggedUser/").json()
    loggedUser.value = data.value ? data.value : null
    // TODO: add error handling here, but weird bug with await and response
  }

  const resetInitialData = () => {
    loggedUser.value = null
    initialDataLoaded.value = false
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
  const fetchUnits = async () => {
    const { data } = await useFetch("/api/v1/units/").json()
    units.value = data.value
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
    fetchUnits,
    plantParts,
    populations,
    conditions,
    units,
  }
})

import { defineStore } from "pinia"
import { useFetch } from "@vueuse/core"
import { ref } from "vue"
import { otherFieldsAtTheEnd } from "@/utils/forms"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const populations = ref(null)
  const conditions = ref(null)
  const effects = ref(null)
  const galenicFormulation = ref(null)
  const plantParts = ref(null)
  const units = ref(null)

  const fetchInitialData = async () => {
    await fetchLoggedUser()
    initialDataLoaded.value = true
  }

  const setLoggedUser = (userData) => {
    loggedUser.value = userData ? userData : null
  }

  const fetchLoggedUser = async () => {
    const { data } = await useFetch("/api/v1/get-logged-user/").json()
    setLoggedUser(data.value)
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
  const fetchEffects = async () => {
    const { data } = await useFetch("/api/v1/effects/").json()
    effects.value = otherFieldsAtTheEnd(data.value)
  }
  const fetchGalenicFormulation = async () => {
    const { data } = await useFetch("/api/v1/galenic-formulation/").json()
    galenicFormulation.value = otherFieldsAtTheEnd(data.value)
  }
  const fetchPlantParts = async () => {
    const { data } = await useFetch("/api/v1/plant-parts/").json()
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
    setLoggedUser,
    fetchLoggedUser,
    fetchPopulations,
    fetchConditions,
    fetchEffects,
    fetchGalenicFormulation,

    fetchPlantParts,
    fetchUnits,
    plantParts,
    populations,
    conditions,
    effects,
    galenicFormulation,
    units,
  }
})

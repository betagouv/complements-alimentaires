import { defineStore } from "pinia"
import { useFetch } from "@vueuse/core"
import { ref, computed } from "vue"
import { pushOtherChoiceFieldAtTheEnd } from "@/utils/forms"

export const useRootStore = defineStore("root", () => {
  const loggedUser = ref(null)
  const initialDataLoaded = ref(false)
  const populations = ref(null)
  const conditions = ref(null)
  const effects = ref(null)
  const galenicFormulations = ref(null)
  const preparations = ref(null)
  const plantParts = ref(null)
  const plantFamilies = ref(null)
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

  const companies = computed(() => loggedUser.value?.companies)

  const resetInitialData = () => {
    loggedUser.value = null
    initialDataLoaded.value = false
  }

  // TODO : Management d'erreur pour tous ces appels
  const fetchPopulations = async () => {
    const { data } = await useFetch("/api/v1/populations/").json()
    populations.value = data.value
  }
  const fetchConditions = async () => {
    const { data } = await useFetch("/api/v1/conditions/").json()
    conditions.value = pushOtherChoiceFieldAtTheEnd(data.value)
  }
  const fetchEffects = async () => {
    const { data } = await useFetch("/api/v1/effects/").json()
    effects.value = pushOtherChoiceFieldAtTheEnd(data.value)
  }
  const fetchGalenicFormulations = async () => {
    const { data } = await useFetch("/api/v1/galenic-formulations/").json()
    galenicFormulations.value = pushOtherChoiceFieldAtTheEnd(data.value)
  }
  const fetchPreparations = async () => {
    const { data } = await useFetch("/api/v1/preparations/").json()
    preparations.value = data.value
  }
  const fetchPlantParts = async () => {
    const { data } = await useFetch("/api/v1/plant-parts/").json()
    plantParts.value = data.value
  }
  const fetchPlantFamilies = async () => {
    const { data } = await useFetch("/api/v1/plant-families/").json()
    plantFamilies.value = data.value
  }
  const fetchUnits = async () => {
    const { data } = await useFetch("/api/v1/units/").json()
    units.value = data.value
  }
  // Appel groupé des fieldDdata
  const fetchDeclarationFieldsData = async () => {
    const { data } = await useFetch("/api/v1/declarationFieldData/").json()
    populations.value = data.value.populations
    conditions.value = pushOtherChoiceFieldAtTheEnd(data.value.conditions)
    effects.value = pushOtherChoiceFieldAtTheEnd(data.value.effects)
    galenicFormulations.value = pushOtherChoiceFieldAtTheEnd(data.value.galenicFormulations)
    preparations.value = data.value.preparations
    plantParts.value = data.value.plantParts
    units.value = data.value.units
  }
  return {
    loggedUser,
    companies,
    initialDataLoaded,
    fetchInitialData,
    resetInitialData,
    setLoggedUser,
    fetchLoggedUser,
    fetchPopulations,
    fetchConditions,
    fetchEffects,
    fetchGalenicFormulations,
    fetchPreparations,
    fetchDeclarationFieldsData,
    fetchPlantParts,
    fetchPlantFamilies,
    fetchUnits,
    plantParts,
    plantFamilies,
    populations,
    conditions,
    effects,
    galenicFormulations,
    preparations,
    units,
  }
})

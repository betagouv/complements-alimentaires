import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants
  const country = ref(undefined)
  const siret = ref(undefined)

  const setCreateCompanyStore = (newCountry, newSiret) => {
    country.value = newCountry
    siret.value = newSiret
  }

  return { storedCountry: country, storedSiret: siret, setCreateCompanyStore }
})

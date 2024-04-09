import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants "frères"
  const country = ref(undefined)
  const siret = ref(undefined)
  const socialName = ref(undefined) // fourni par le back-end quand l'entreprise existe

  const setCompanyCountry = (newCountry) => (country.value = newCountry)

  const setCompanySiretAndName = (newSiret, newSocialName) => {
    siret.value = newSiret
    socialName.value = newSocialName
  }

  return {
    storedCountry: country,
    storedSiret: siret,
    storedSocialName: socialName,
    setCompanyCountry,
    setCompanySiretAndName,
  }
})

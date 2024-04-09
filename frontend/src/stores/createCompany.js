import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants "frères"
  const country = ref(undefined)
  const identifier = ref(undefined)
  const identifierType = ref(undefined)
  const socialName = ref(undefined) // fourni par le back-end, uniquement quand l'entreprise existe déjà

  const setCompanyCountry = (newCountry) => (country.value = newCountry)

  const setCompanyIdentifierAndName = (newIdentifier, newIdentifierType, newSocialName) => {
    identifier.value = newIdentifier
    identifierType.value = newIdentifierType
    socialName.value = newSocialName
  }

  const resetCompany = () => {
    identifier.value = undefined
    identifierType.value = undefined
    socialName.value = undefined
  }

  return {
    storedCountry: country,
    storedIdentifier: identifier,
    storedIdentifierType: identifierType, // `siret` ou `vat`
    setCompanyCountry,
    setCompanyIdentifierAndName,
    resetCompany,
  }
})

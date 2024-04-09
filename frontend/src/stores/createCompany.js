import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants "frères"
  const country = ref(undefined)
  const identifier = ref(undefined)
  const identifierType = ref(undefined)
  const socialName = ref(undefined) // fourni par le back-end, uniquement quand l'entreprise existe déjà

  const setCompanyCountryAndIdentifierType = (newCountry, newIdentifierType) => {
    country.value = newCountry
    identifierType.value = newIdentifierType
  }

  const setCompanyIdentifierAndName = (newIdentifier, newSocialName) => {
    identifier.value = newIdentifier
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
    setCompanyCountryAndIdentifierType,
    setCompanyIdentifierAndName,
    resetCompany,
  }
})

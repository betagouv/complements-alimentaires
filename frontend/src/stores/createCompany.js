import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants "frères"
  const country = ref(undefined)
  const identifier = ref(undefined) // un identifiant qui est soit un SIRET, soit un VAT
  const identifierType = ref(undefined) // `siret` ou `vat`
  const socialName = ref(undefined) // fourni par le back-end, uniquement quand l'entreprise existe déjà
  const id = ref(undefined) // fourni par le back-end, quand l'entreprise existe déjà ou est créée

  const setCompanyCountry = (newCountry) => {
    country.value = newCountry
  }

  const setCompanyIdentifierType = (newIdentifierType) => {
    identifierType.value = newIdentifierType
  }

  const setCompanyIdentifier = (newIdentifier) => {
    identifier.value = newIdentifier
  }

  const setCompanySocialName = (newSocialName) => {
    socialName.value = newSocialName
  }

  const setCompanyId = (newId) => {
    id.value = newId
  }

  const resetCompany = () => {
    country.value = undefined
    identifier.value = undefined
    identifierType.value = undefined
    socialName.value = undefined
    id.value = undefined
  }

  return {
    // getters
    storedCountry: country,
    storedIdentifier: identifier,
    storedIdentifierType: identifierType,
    storedSocialName: socialName,
    storedId: id,
    // setters
    setCompanyCountry,
    setCompanyIdentifierType,
    setCompanyIdentifier,
    setCompanySocialName,
    setCompanyId,
    // resetter
    resetCompany,
  }
})

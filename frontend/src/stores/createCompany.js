import { defineStore } from "pinia"
import { ref } from "vue"

export const useCreateCompanyStore = defineStore("createCompany", () => {
  // Ce store est utilisé temporairement lors de la création d'une entreprise pour faciliter le transit des informations entre des composants "frères"
  const country = ref(undefined)
  const identifier = ref(undefined) // un identifiant qui est soit un SIRET, soit un VAT
  const identifierType = ref(undefined) // `siret` ou `vat`
  const socialName = ref(undefined) // fourni par le back-end, uniquement quand l'entreprise existe déjà
  const id = ref(undefined) // fourni par le back-end, quand l'entreprise existe déjà ou est créée

  const setCompanyCountryAndIdentifierType = (newCountry, newIdentifierType) => {
    country.value = newCountry
    identifierType.value = newIdentifierType
  }

  const setCompanyIdentifierAndName = (newIdentifier, newSocialName) => {
    identifier.value = newIdentifier
    socialName.value = newSocialName
  }

  const setCompanyId = (newId) => {
    id.value = newId
  }

  // TODO: rationnaliser, et peut être faire qu'une action à la fois même si c'est verbeux
  const setCompanySocialName = (newSocialName) => {
    socialName.value = newSocialName
  }

  const resetCompany = () => {
    country.value = undefined
    identifier.value = undefined
    identifierType.value = undefined
    socialName.value = undefined
    id.value = undefined
  }

  return {
    storedCountry: country,
    storedIdentifier: identifier,
    storedIdentifierType: identifierType,
    storedSocialName: socialName,
    storedId: id,
    setCompanyCountryAndIdentifierType,
    setCompanyIdentifierAndName,
    setCompanyId,
    setCompanySocialName,
    resetCompany,
  }
})

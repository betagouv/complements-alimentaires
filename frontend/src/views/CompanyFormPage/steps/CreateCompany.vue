<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise dont le SIRET est
      <strong>{{ state.siret }}</strong>
      n'est pas encore enregistrée dans notre base de données. Pour ce faire, veuillez vérifier ou compléter les
      informations ci-dessous. À l'issue, vous en deviendrez automatiquement son gestionnaire.
      <FormWrapper class="mx-auto">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'socialName')">
          <DsfrInput v-model="state.socialName" label="Dénomination sociale" labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'commercialName')">
          <DsfrInput v-model="state.commercialName" label="Nom commercial" labelVisible />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'address')">
          <DsfrInput v-model="state.address" label="Adresse" labelVisible hint="Numéro et voie" />
        </DsfrInputGroup>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'additionalDetails')">
          <DsfrInput
            v-model="state.additionalDetails"
            label="Complément d’adresse (optionnel)"
            labelVisible
            hint="Bâtiment, immeuble, escalier et numéro d’appartement"
          />
        </DsfrInputGroup>
        <div class="flex gap-x-4 justify-between">
          <DsfrInputGroup :error-message="firstErrorMsg(v$, 'postalCode')">
            <DsfrInput v-model="state.postalCode" label="Code postal" labelVisible />
          </DsfrInputGroup>
          <DsfrInputGroup class="grow" :error-message="firstErrorMsg(v$, 'city')">
            <DsfrInput v-model="state.city" label="Ville" labelVisible />
          </DsfrInputGroup>
        </div>
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'cedex')">
          <DsfrInput v-model="state.cedex" label="Cedex (optionnel)" labelVisible />
        </DsfrInputGroup>
        <DsfrButton label="Enregistrer l'entreprise" @click="submitCompany" :disabled="isFetching" />
      </FormWrapper>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useCreateCompanyStore } from "@/stores/createCompany"

// Form state & rules

const { storedCountry, storedSiret } = useCreateCompanyStore()

const state = ref({
  socialName: "",
  commercialName: "",
  address: "",
  additionalDetails: "",
  postalCode: "",
  city: "",
  cedex: "",
  country: storedCountry,
  siret: storedSiret,
})

const rules = {
  socialName: errorRequiredField,
  commercialName: errorRequiredField,
  address: errorRequiredField,
  additionalDetails: {},
  postalCode: errorRequiredField,
  city: errorRequiredField,
  cedex: {},
  // `country` et `siret` ne sont pas affichés dans le formulaire car déjà entrés plus tôt
}

const $externalResults = ref({})
const v$ = useVuelidate(rules, state, { $externalResults })

// Request definition
const { response, execute, isFetching } = useFetch(
  `/api/v1/companies/`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(state)
  .json()

// Request execution
const submitCompany = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    // ??
  }
}
</script>

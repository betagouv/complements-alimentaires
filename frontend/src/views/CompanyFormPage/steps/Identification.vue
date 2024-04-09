<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'country')">
        <CountryField v-model="state.country" description="Dans quel pays l'entreprise est-elle immatriculée ?" />
      </DsfrInputGroup>
      <template v-if="state.country === 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'siret')">
          <DsfrInput v-model="state.siret" label="Numéro de SIRET" required labelVisible @input="removeSpaces" />
          <div class="mt-2">
            <a class="fr-link" target="_blank" rel="noopener" href="https://annuaire-entreprises.data.gouv.fr/">
              Annuaire des entreprises
            </a>
          </div>
        </DsfrInputGroup>
        <DsfrButton
          label="Vérifier le SIRET"
          icon="ri-arrow-right-line"
          iconRight
          @click="submitSiret"
          :disabled="isFetching"
        />
      </template>

      <template v-if="state.country && state.country !== 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'vatIdNumber')">
          <DsfrInput v-model="state.vatIdNumber" label="Numéro de TVA intracommunautaire" required labelVisible />
        </DsfrInputGroup>
        <DsfrButton label="Vérifier le n° de TVA" icon="ri-arrow-right-line" iconRight />
      </template>
    </FormWrapper>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import FormWrapper from "@/components/FormWrapper"
import CountryField from "@/components/fields/CountryField"
import { errorRequiredField, firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { required, minLength, maxLength, helpers } from "@vuelidate/validators"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useCreateCompanyStore } from "@/stores/createCompany"

// Props & emits
const emit = defineEmits(["changeStep"])

// Form state & rules
const state = ref({
  country: undefined,
  siret: "",
  vatIdNumber: "",
})

const rules = {
  country: errorRequiredField,
  siret: {
    required: helpers.withMessage("Ce champ doit être rempli", required),
    minLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", minLength(14)),
    maxLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", maxLength(14)),
  },
  vatIdNumber: {}, // errorRequiredField TODO: remettre, bug validation croisée
}

const v$ = useVuelidate(rules, state)

// Request definition
const url = computed(() => `/api/v1/companies/${state.value.siret}/check-siret`)
const { data, response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

const submitSiret = async () => {
  // TODO: pb avec validation croisée !
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  await handleError(response)
  if (response.value.ok) {
    const { setCreateCompanyStore } = useCreateCompanyStore()
    setCreateCompanyStore(state.value.country, state.value.siret, data.value.socialName) // stored data to be use in another component later

    switch (data.value.companyStatus) {
      case "unregistered_company":
        emit("changeStep", {
          index: 1,
          name: "Enregistrement d'une nouvelle entreprise",
          component: "CreateCompany",
          goToNextStep: true,
        })
        break
      case "registered_and_supervised_by_me":
        emit("changeStep", {
          index: 1,
          name: "L'entreprise existe déjà !",
          component: "NothingToDo",
          goToNextStep: true,
        })
        break
      case "registered_and_supervised_by_other":
        emit("changeStep", {
          index: 1,
          name: "Demande d'accès à une entreprise existante",
          component: "RequestAccess",
          goToNextStep: true,
        })
        break
      case "registered_and_unsupervised":
        emit("changeStep", {
          index: 1,
          name: "Revendication d'une entreprise existante",
          component: "ClaimSupervision",
          goToNextStep: true,
        })
        break
    }
  }
}

const removeSpaces = (event) => (event.target.value = event.target.value.replace(/\s/g, ""))
</script>

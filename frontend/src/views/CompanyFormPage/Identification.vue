<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'identifier')">
        <DsfrInput
          :label="`Numéro de ${company.identifierType.toUpperCase()}`"
          :hint="company.identifierType.toUpperCase() !== 'SIRET' ? 'Merci d\'utiliser des majuscules' : ''"
          v-model="identifier"
          required
          labelVisible
          @input="removeSpaces"
        />
        <div v-if="company.identifierType == 'siret'" class="mt-2">
          <a
            class="fr-link"
            target="_blank"
            rel="noopener external"
            href="https://annuaire-entreprises.data.gouv.fr/"
            title="Annuaire des entreprises - nouvelle fenêtre"
          >
            Annuaire des entreprises
          </a>
        </div>
      </DsfrInputGroup>
      <DsfrButton icon="ri-arrow-right-line" iconRight @click="submitIdentifier" :disabled="isFetching">
        Vérifier le n° de {{ company.identifierType.toUpperCase() }}
      </DsfrButton>
    </FormWrapper>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import { firstErrorMsg, errorRequiredField } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"

// Props & emits
const company = defineModel()
company.value.siretData = null // RAZ du state si l'utilisateur a cliqué sur précédent
const emit = defineEmits(["changeStep"])

// Form state & rules
const identifier = ref("")

const rules = { identifier: errorRequiredField } // la plupart des règles sont laissées côté back

const $externalResults = ref({})
const v$ = useVuelidate(rules, { identifier: identifier }, { $externalResults })

// Request definition
const url = computed(
  () => `/api/v1/companies/${identifier.value}/check-identifier/?identifierType=${company.value.identifierType}`
)
const { data, response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

const submitIdentifier = async () => {
  v$.value.$clearExternalResults()
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    company.value.identifier = identifier.value
    if (data.value.company) {
      company.value.socialName = data.value.company.socialName
      company.value.id = data.value.company.id
    }
    if (data.value.companySiretData) {
      company.value.siretData = data.value.companySiretData
    }

    switch (data.value.companyStatus) {
      case "unregistered_company":
        emit("changeStep", {
          name: "Enregistrement d'une nouvelle entreprise",
          component: "CreateCompany",
        })
        break
      case "registered_and_supervised_by_me":
        emit("changeStep", {
          name: "L'entreprise existe déjà",
          component: "NothingToDo",
          deleteStepAfter: true,
        })
        break
      case "registered_and_supervised_by_other":
        emit("changeStep", {
          name: "Demande d'accès à une entreprise existante",
          component: "ClaimCompanyAccess",
        })
        break
      // ce cas correspond notamment aux entreprises importées de TeleIcare
      case "registered_and_unsupervised":
        emit("changeStep", {
          name: "Demande de gestion d'une entreprise existante",
          component: "ClaimSupervision",
        })
    }
  }
}

// Outil pour permettre un copier coller sans erreur d'un numéro d'identification
const removeSpaces = (event) => (event.target.value = event.target.value.replace(/\s/g, ""))
</script>

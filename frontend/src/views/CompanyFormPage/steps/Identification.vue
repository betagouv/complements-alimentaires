<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'identifier')">
        <DsfrInput
          :label="`Numéro de ${storedIdentifierType.toUpperCase()}`"
          v-model="identifier"
          required
          labelVisible
          @input="removeSpaces"
        />
        <div v-if="storedIdentifierType == 'siret'" class="mt-2">
          <a class="fr-link" target="_blank" rel="noopener" href="https://annuaire-entreprises.data.gouv.fr/">
            Annuaire des entreprises
          </a>
        </div>
      </DsfrInputGroup>
      <DsfrButton icon="ri-arrow-right-line" iconRight @click="submitIdentifier" :disabled="isFetching">
        Vérifier le n° de {{ storedIdentifierType.toUpperCase() }}
      </DsfrButton>
    </FormWrapper>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import { firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { required, minLength, maxLength, helpers } from "@vuelidate/validators"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useCreateCompanyStore } from "@/stores/createCompany"

const emit = defineEmits(["changeStep"])
const { storedIdentifierType, setCompanyIdentifier, setCompanySocialName, setCompanyId } = useCreateCompanyStore()

// Form state & rules
const identifier = ref("")

const rules = {
  identifier: {
    // règle de base
    required: helpers.withMessage("Ce champ doit être rempli", required),
    // règles uniquement pour le siret
    ...(storedIdentifierType == "siret"
      ? {
          minLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", minLength(14)),
          maxLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", maxLength(14)),
        }
      : {}),
  },
}

const v$ = useVuelidate(rules, { identifier: identifier })

// Request definition
const url = computed(
  () => `/api/v1/companies/${identifier.value}/check-identifier?identifierType=${storedIdentifierType}`
)
const { data, response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

const submitIdentifier = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  await handleError(response)
  if (response.value.ok) {
    setCompanyIdentifier(identifier.value)
    setCompanySocialName(data.value.company.socialName)
    setCompanyId(data.value.company.id)

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
          name: "Demande de co-gestion d'une entreprise existante",
          component: "ClaimCoSupervision",
        })
        break
      case "registered_and_unsupervised":
        emit("changeStep", {
          name: "Revendication d'une entreprise existante",
          component: "ClaimSupervision",
        })
    }
  }
}

// Outil pour permettre un copier coller sans erreur d'un numéro d'identification
const removeSpaces = (event) => (event.target.value = event.target.value.replace(/\s/g, ""))
</script>

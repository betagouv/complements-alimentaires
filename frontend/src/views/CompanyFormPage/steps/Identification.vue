<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <template v-if="storedCountry == 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'siret')">
          <DsfrInput v-model="siret" label="Numéro de SIRET" required labelVisible @input="removeSpaces" />
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

      <!-- TODO: gérer -->
      <template v-if="storedCountry != 'FR'">
        <DsfrInputGroup :error-message="firstErrorMsg(v$, 'siret')">
          <DsfrInput v-model="siret" label="Numéro de TVA intracommunautaire" required labelVisible />
        </DsfrInputGroup>
        <DsfrButton label="Vérifier le n° de TVA" icon="ri-arrow-right-line" iconRight />
      </template>
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

// Props & emits
const emit = defineEmits(["changeStep"])

const { storedCountry } = useCreateCompanyStore()

// Form state & rules
const siret = ref("")

const rules = {
  siret: {
    required: helpers.withMessage("Ce champ doit être rempli", required),
    minLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", minLength(14)),
    maxLength: helpers.withMessage("Un SIRET doit contenir exactement 14 chiffres", maxLength(14)),
  },
}

const v$ = useVuelidate(rules, { siret: siret })

// Request definition
const url = computed(() => `/api/v1/companies/${siret.value}/check-siret`)
const { data, response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

const submitSiret = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return // prevent API call if there is a front-end error
  }
  await execute()
  await handleError(response)
  if (response.value.ok) {
    useCreateCompanyStore().setCompanySiretAndName(siret.value, data.value.socialName)

    switch (data.value.companyStatus) {
      case "unregistered_company":
        emit("changeStep", {
          index: 2,
          name: "Enregistrement d'une nouvelle entreprise",
          component: "CreateCompany",
          goToNextStep: true,
        })
        break
      case "registered_and_supervised_by_me":
        emit("changeStep", {
          index: 2,
          name: "L'entreprise existe déjà !",
          component: "NothingToDo",
          goToNextStep: true,
        })
        break
      case "registered_and_supervised_by_other":
        emit("changeStep", {
          index: 2,
          name: "Demande de co-gestion d'une entreprise existante",
          component: "ClaimCoSupervision",
          goToNextStep: true,
        })
        break
      case "registered_and_unsupervised":
        emit("changeStep", {
          index: 2,
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

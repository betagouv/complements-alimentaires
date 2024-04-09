<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
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
import { getEmitIdentificationData } from "../getEmitIdentificationData"

const emit = defineEmits(["changeStep"])

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
const url = computed(() => `/api/v1/companies/${siret.value}/check-identifier?identifierType=siret`)
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
    useCreateCompanyStore().setCompanyIdentifierAndName(siret.value, "siret", data.value.socialName)
    emit("changeStep", getEmitIdentificationData(data.value))
  }
}

const removeSpaces = (event) => (event.target.value = event.target.value.replace(/\s/g, ""))
</script>

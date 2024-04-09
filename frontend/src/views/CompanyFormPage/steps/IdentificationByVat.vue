<template>
  <div>
    <FormWrapper class="max-w-xl mx-auto">
      <DsfrInputGroup :error-message="firstErrorMsg(v$, 'vat')">
        <DsfrInput v-model="vat" label="Numéro de TVA intracommunautaire" required labelVisible />
      </DsfrInputGroup>
      <DsfrButton
        label="Vérifier le n° de TVA"
        icon="ri-arrow-right-line"
        :disabled="isFetching"
        iconRight
        @click="submitVat"
      />
    </FormWrapper>
  </div>
</template>

<script setup>
import { computed, ref } from "vue"
import FormWrapper from "@/components/FormWrapper"
import { firstErrorMsg } from "@/utils/forms"
import { useVuelidate } from "@vuelidate/core"
import { required, helpers } from "@vuelidate/validators"
import { headers } from "@/utils/data-fetching"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { useCreateCompanyStore } from "@/stores/createCompany"
import { getEmitIdentificationData } from "../getEmitIdentificationData"

// Props & emits
const emit = defineEmits(["changeStep"])

// Form state & rules
const vat = ref("")

const rules = {
  vat: {
    required: helpers.withMessage("Ce champ doit être rempli", required),
  },
}

const v$ = useVuelidate(rules, { vat: vat })

// Request definition
const url = computed(() => `/api/v1/companies/${vat.value}/check-identifier?identifierType=vat`)
const { data, response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

const submitVat = async () => {
  v$.value.$validate()
  if (v$.value.$error) {
    return
  }
  await execute()
  await handleError(response)
  if (response.value.ok) {
    useCreateCompanyStore().setCompanyIdentifierAndName(vat.value, "vat", data.value.socialName)
    emit("changeStep", getEmitIdentificationData(data.value))
  }
}
</script>

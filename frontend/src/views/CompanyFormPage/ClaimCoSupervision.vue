<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise
      <strong>{{ modelValue.socialName }}</strong>
      avec le n° {{ modelValue.identifierType.toUpperCase() + " " }}
      <strong>{{ modelValue.identifier }}</strong>
      est présente dans notre base de données, et dispose déjà d'un gestionnaire. Vous pouvez cependant demander à
      devenir vous-même gestionnaire en envoyant une demande à l'ensemble des gestionnaires actuels.
      <DsfrInputGroup>
        <DsfrInput v-model="message" label="Message (optionnel)" labelVisible isTextarea />
      </DsfrInputGroup>
      <div class="flex gap-x-4">
        <DsfrButton
          label="Demander la co-gestion"
          icon="ri-key2-line"
          @click="submitClaimCoSupervision"
          :disabled="isFetching"
        />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref, computed } from "vue"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

// Props & emits
const props = defineProps({ modelValue: Object })
const emit = defineEmits(["changeStep"])

// Form state & rules
const message = ref("")

const $externalResults = ref({})
const v$ = useVuelidate({}, { message: message }, { $externalResults })

// Request definition
const url = computed(
  () =>
    `/api/v1/companies/${props.modelValue.identifier}/claim-co-supervision?identifierType=${props.modelValue.identifierType}`
)
const { response, execute, isFetching } = useFetch(
  url,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

// Request execution
const submitClaimCoSupervision = async () => {
  v$.value.$validate()
  // pas besoin de vérifier les erreurs fronts, car pas possible sur le seul champ message
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    emit("changeStep", {
      name: `Demande de co-gestion effectuée`,
      component: "EndClaimDone",
    })
  }
}
</script>

<template>
  <div>
    <DsfrAlert>
      <p>
        L'entreprise
        <strong>{{ company.socialName }}</strong>
        avec le n° {{ company.identifierType.toUpperCase() + " " }}
        <strong>{{ company.identifier }}</strong>
        est présente dans notre base de données, mais ne dispose actuellement d'aucun gestionnaire. Si vous souhaitez
        revendiquer la gestion de cette entreprise, veuillez nous envoyer une demande :
      </p>
      <DsfrInputGroup>
        <DsfrInput v-model="message" label="Message (optionnel)" labelVisible isTextarea />
      </DsfrInputGroup>
      <div class="flex gap-x-4">
        <DsfrButton
          label="Demander la gestion"
          icon="ri-key-2-line"
          @click="submitClaimSupervision"
          :disabled="isFetching"
        />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

// Props & emits
const company = defineModel()
const emit = defineEmits(["changeStep"])

// Form state & rules
const message = ref("")

const $externalResults = ref({})
const v$ = useVuelidate({}, { message: message }, { $externalResults })

// Request definition

const { response, execute, isFetching } = useFetch(
  `/api/v1/companies/${company.value.identifier}/claim-supervision/?identifierType=${company.value.identifierType}`,
  {
    headers: headers(),
  },
  { immediate: false }
)
  .post(() => ({
    message: message.value,
  }))
  .json()

// Request execution
const submitClaimSupervision = async () => {
  v$.value.$validate()
  // pas besoin de vérifier les erreurs fronts, car pas possible sur le seul champ message
  await execute()
  $externalResults.value = await handleError(response)
  if (response.value.ok) {
    emit("changeStep", {
      name: `Demande de gestion effectuée`,
      component: "EndClaimDone",
    })
  }
}
</script>

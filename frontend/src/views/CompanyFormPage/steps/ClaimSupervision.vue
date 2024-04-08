<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise dont le SIRET est
      <strong>{{ storedSiret }}</strong>
      est présente dans notre base de données, mais ne dispose actuellement d'aucun gestionnaire. Si vous souhaitez
      revendiquer la gestion de cette entreprise, veuillez nous envoyer une demande :
      <DsfrInputGroup>
        <DsfrInput v-model="message" label="Message (optionnel)" labelVisible isTextarea />
      </DsfrInputGroup>
      <div class="flex gap-x-4">
        <DsfrButton
          label="Demander la gestion"
          icon="ri-key2-line"
          @click="submitClaimSupervision"
          :disabled="isFetching"
        />
      </div>
    </DsfrAlert>
  </div>
</template>

<script setup>
import { ref } from "vue"
import { useCreateCompanyStore } from "@/stores/createCompany"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

const { storedSiret } = useCreateCompanyStore()

// Form state & rules
const message = ref("")

const $externalResults = ref({})
const v$ = useVuelidate({}, { message: message }, { $externalResults })

// Request definition

const { response, execute, isFetching } = useFetch(
  `/api/v1/claim-company-supervision/${storedSiret}`,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

// Request execution
const submitClaimSupervision = async () => {
  v$.value.$validate()
  // pas besoin de vérifier les erreurs fronts, car pas possible sur le seul champ message
  await execute()
  $externalResults.value = await handleError(response)
}
</script>

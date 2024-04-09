<template>
  <div>
    <DsfrAlert size="sm">
      L'entreprise
      <strong>{{ storedSocialName }}</strong>
      avec le SIRET
      <strong>{{ storedSiret }}</strong>
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
import { ref } from "vue"
import { useCreateCompanyStore } from "@/stores/createCompany"
import { useFetch } from "@vueuse/core"
import { useVuelidate } from "@vuelidate/core"
import { headers } from "@/utils/data-fetching"
import { handleError } from "@/utils/error-handling"

const { storedSiret, storedSocialName } = useCreateCompanyStore()

// Form state & rules
const message = ref("")

const $externalResults = ref({})
const v$ = useVuelidate({}, { message: message }, { $externalResults })

// Request definition
const { response, execute, isFetching } = useFetch(
  `/api/v1/companies/${storedSiret}/claim-co-supervision`,
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
}
</script>

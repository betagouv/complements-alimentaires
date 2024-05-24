<template>
  <SolicitationsHolder
    v-if="solicitations"
    title="Invitations envoyées"
    icon="ri-chat-upload-line"
    description="Visualisez les invitations envoyées par les co-gestionnaires à rejoindre votre entreprise."
    :solicitations="solicitations"
    emptyText="Il n'y a aucune invitation en cours"
    :actions="[]"
    showRecipientEmail
  />
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { onMounted } from "vue"
import SolicitationsHolder from "./SolicitationsHolder"

const props = defineProps({ companyId: Number })

const {
  data: solicitations,
  response,
  execute,
} = useFetch(
  `/api/v1/companies/${props.companyId}/collaboration-invitations/`,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})
</script>

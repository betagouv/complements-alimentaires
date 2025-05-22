<template>
  <SolicitationsHolder
    v-if="solicitations"
    @process="process"
    title="Demandes reçues"
    icon="ri-chat-download-line"
    :solicitations="solicitations"
    emptyText="Vous n'avez actuellement aucune demande en cours."
    :actions="[
      { name: 'accept', label: 'Accepter', primary: true, icon: 'ri-check-fill' },
      { name: 'refuse', label: 'Refuser', secondary: true, icon: 'ri-close-fill' },
    ]"
  />
</template>

<script setup>
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import useToaster from "@/composables/use-toaster"
import SolicitationsHolder from "./SolicitationsHolder"

const emit = defineEmits(["process"])
defineProps({ solicitations: Array })

const process = async (solicitationId, actionName) => {
  const url = `/api/v1/company-access-claims/${solicitationId}/process/`
  const { response } = await useFetch(url, { headers: headers() }).post({ actionName: actionName }).json()
  await handleError(response)
  if (response.value.ok) {
    emit("process")
    useToaster().addMessage({
      type: "success",
      description: "La demande a bien été traitée.",
    })
  }
}
</script>

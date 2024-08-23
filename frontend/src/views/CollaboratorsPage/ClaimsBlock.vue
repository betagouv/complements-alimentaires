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
import { onMounted } from "vue"
import useToaster from "@/composables/use-toaster"
import SolicitationsHolder from "./SolicitationsHolder"

const props = defineProps({ companyId: Number, collaboratorsExecute: Function })

const {
  data: solicitations,
  response,
  execute,
} = useFetch(
  `/api/v1/companies/${props.companyId}/company-access-claims/`,
  {
    headers: headers(),
  },
  { immediate: false }
).json()

onMounted(async () => {
  await execute()
  await handleError(response)
})

const process = async (solicitationId, actionName) => {
  const url = `/api/v1/company-access-claims/${solicitationId}/process/`
  const { response } = await useFetch(url, { headers: headers() }).post({ actionName: actionName }).json()
  await handleError(response)
  if (response.value.ok) {
    await props.collaboratorsExecute() // met à jour les collaborateurs existants, car ils peuvent avoir changé
    useToaster().addMessage({
      type: "success",
      description: "La demande a bien été traitée.",
    })
    // Mise à jour de l'UI en retirant la ligne (une action traitée n'a plus de raison d'apparaitre plus ici)
    solicitations.value = solicitations.value.filter((item) => item.id !== solicitationId)
  }
}
</script>

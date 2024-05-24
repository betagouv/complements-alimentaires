<template>
  <div v-if="solicitations">
    <SectionTitle title="Demandes reçues" icon="ri-chat-download-line" />
    <p>Visualisez et traitez vos demandes reçues pour rejoindre votre entreprise.</p>
    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="flex items-center">
        <v-icon class="size-4" name="ri-chat-download-line" />

        <div class="ml-2">
          <div>{{ solicitation.senderName }}</div>
          <div class="text-xs">
            {{ isoToPrettyDate(solicitation.creationDate, dateOptions) }}
            à {{ isoToPrettyTime(solicitation.creationDate) }}
          </div>
        </div>

        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <div class="italic">{{ solicitation.description }}</div>
          <div class="flex gap-x-2">
            <DsfrButton
              v-for="action in actions"
              :key="action.label"
              :label="action.label"
              :icon="action.icon"
              :primary="action.primary"
              :secondary="action.secondary"
              size="sm"
              @click="process(solicitation.id, action.name)"
            />
          </div>
        </div>
      </div>
      <hr class="mt-4 -mb-2 border" />
    </div>
    <div v-if="solicitations.length === 0">
      <p class="italic">Vous n'avez actuellement aucune demande en cours.</p>
    </div>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import { useFetch } from "@vueuse/core"
import { handleError } from "@/utils/error-handling"
import { headers } from "@/utils/data-fetching"
import { onMounted } from "vue"
import { isoToPrettyDate, isoToPrettyTime } from "@/utils/date"
import useToaster from "@/composables/use-toaster"

const props = defineProps({ companyId: Number, collaboratorsExecute: Function })

const dateOptions = {
  weekday: "short",
  month: "short",
  day: "numeric",
}

// Pour le moment, les actions possibles sont identiques entre toutes les solicitations, donc on garde ça hardcodé.
// A terme, on pourra imaginer un mapping côté front, ou même que le back-end retourne les différentes actions possibles.
const actions = [
  { name: "accept", label: "Accepter", primary: true, icon: "ri-check-fill" },
  { name: "refuse", label: "Refuser", secondary: true, icon: "ri-close-fill" },
]

const {
  data: solicitations,
  response,
  execute,
} = useFetch(
  `/api/v1/companies/${props.companyId}/co-supervision-claims/`,
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
  const url = `/api/v1/co-supervision-claims/${solicitationId}/process/`
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

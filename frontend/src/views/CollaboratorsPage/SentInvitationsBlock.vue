<template>
  <div v-if="solicitations">
    <SectionTitle title="Invitations envoyées" icon="ri-chat-upload-line" />
    <p>Visualisez les invitations envoyées par les co-gestionnaires à rejoindre votre entreprise.</p>
    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="flex items-center">
        <v-icon class="size-4" name="ri-chat-upload-line" />

        <div class="ml-2">
          <div>{{ solicitation.senderName }}</div>
          <div class="-mt-1.5">à {{ solicitation.recipientEmail }}</div>
          <div class="text-xs">
            {{ isoToPrettyDate(solicitation.creationDate, dateOptions) }}
            à {{ isoToPrettyTime(solicitation.creationDate) }}
          </div>
        </div>

        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <div class="italic">{{ solicitation.description }}</div>
        </div>
      </div>
      <hr class="mt-4 -mb-2 border" />
    </div>
    <div v-if="solicitations.length === 0">
      <p class="italic">Il n'y a aucune invitation en cours.</p>
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

const props = defineProps({ companyId: Number })

const dateOptions = {
  weekday: "short",
  month: "short",
  day: "numeric",
}

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
  if (!solicitations.value) {
    solicitations.value = []
  }
})
</script>

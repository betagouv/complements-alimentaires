<template>
  <div>
    <SectionTitle title="Demandes en cours" icon="ri-chat-3-line" />
    <h6>Vos demandes reçues</h6>

    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="flex items-center">
        <v-icon class="size-4" name="ri-chat-3-line" />

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
            <DsfrButton label="Accepter" size="sm" icon="ri-check-fill" />
            <DsfrButton label="Refuser" secondary size="sm" icon="ri-close-fill" />
          </div>
        </div>
      </div>
      <hr class="mt-4 -mb-2 border" />
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
import { useRootStore } from "@/stores/root"
import { storeToRefs } from "pinia"

const store = useRootStore()
const { company } = storeToRefs(store)

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
  `/api/v1/companies/${company.value.id}/solicitations`,
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

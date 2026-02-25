<template>
  <div>
    <SectionTitle :title="title" :icon="icon" />
    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="sm:flex items-center">
        <v-icon class="size-4" :name="icon" />

        <h3 class="ml-2 fr-text--md font-normal mb-0">
          <span class="block">{{ solicitation.senderName }}</span>
          <span class="-mt-1.5 block" v-if="showRecipientEmail">à {{ solicitation.recipientEmail }}</span>
          <span class="text-xs block">
            {{ isoToPrettyDate(solicitation.creationDate, dateOptions) }}
            à {{ isoToPrettyTime(solicitation.creationDate) }}
          </span>
        </h3>

        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <p class="italic mb-0">{{ solicitation.description }}</p>
          <div v-if="actions.length > 0" class="flex gap-x-2">
            <DsfrButton
              v-for="action in actions"
              :key="action.label"
              :label="action.label"
              :icon="action.icon"
              :primary="action.primary"
              :secondary="action.secondary"
              size="sm"
              @click="emit('process', solicitation.id, action.name)"
            />
          </div>
        </div>
      </div>
      <hr class="mt-4 -mb-2" />
    </div>
    <p class="italic" v-if="solicitations.length === 0">{{ emptyText }}</p>
  </div>
</template>

<script setup>
import SectionTitle from "@/components/SectionTitle"
import { isoToPrettyDate, isoToPrettyTime } from "@/utils/date"

defineProps({
  title: String,
  icon: String,
  solicitations: Array,
  emptyText: String,
  actions: Array,
  showRecipientEmail: { type: Boolean, default: false }, // spécifique
})

const emit = defineEmits(["process"])

const dateOptions = {
  weekday: "short",
  month: "short",
  day: "numeric",
}
</script>

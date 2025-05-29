<template>
  <div>
    <SectionTitle :title="title" :icon="icon" />
    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="flex items-center">
        <v-icon class="size-4" name="ri-chat-download-line" />

        <div class="ml-2">
          <div>{{ solicitation.senderName }}</div>
          <div class="-mt-1.5" v-if="showRecipientEmail">à {{ solicitation.recipientEmail }}</div>
          <div class="text-xs">
            {{ isoToPrettyDate(solicitation.creationDate, dateOptions) }}
            à {{ isoToPrettyTime(solicitation.creationDate) }}
          </div>
        </div>

        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <div class="italic">{{ solicitation.description }}</div>
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
    <div v-if="solicitations.length === 0">
      <p class="italic">{{ emptyText }}</p>
    </div>
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

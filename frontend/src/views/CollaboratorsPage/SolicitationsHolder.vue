<template>
  <div>
    <SectionTitle :title="title" :icon="icon" />
    <div v-for="solicitation in solicitations" :key="solicitation.id">
      <div class="sm:flex items-center">
        <v-icon class="size-4" :name="icon" />

        <div class="ml-2">
          <h3 class="fr-text--md font-normal mb-0">{{ solicitation.senderName }}</h3>
          <p class="-mt-1.5 mb-0" v-if="showRecipientEmail">à {{ solicitation.recipientEmail }}</p>
          <p class="text-xs mb-0">
            {{ isoToPrettyDate(solicitation.creationDate, dateOptions) }}
            à {{ isoToPrettyTime(solicitation.creationDate) }}
          </p>
        </div>

        <div class="ml-2 md:ml-8 flex flex-col gap-y-1">
          <p class="italic mb-0">{{ solicitation.description }}</p>
          <ul v-if="actions.length > 0" class="list-none pl-0 my-0 flex gap-x-2" role="list">
            <li v-for="action in actions" :key="action.label">
              <DsfrButton
                :label="action.label"
                :icon="action.icon"
                :primary="action.primary"
                :secondary="action.secondary"
                size="sm"
                @click="emit('process', solicitation.id, action.name)"
              />
            </li>
          </ul>
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

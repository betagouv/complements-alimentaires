<template>
  <component :is="headerTag" :class="`fr-${sizeTag} flex gap-x-2`">
    <v-icon class="mt-[4px]" v-if="icon" :name="icon" />
    <div>
      {{ title }}
    </div>
    <HistoryBadge v-if="withHistoryBadge" />
  </component>
</template>

<script setup>
import HistoryBadge from "@/components/History/HistoryBadge"

defineProps({
  title: { type: String },
  icon: { type: String, default: undefined },
  headerTag: { type: String, default: "h2" },
  sizeTag: { type: String, default: "h5" },
  withHistoryBadge: { type: Boolean, default: false },
})
</script>

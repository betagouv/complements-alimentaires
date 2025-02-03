<template>
  <div>
    <router-link :to="props.to" :text="props.text" class="mr-2"></router-link>
    <HistoryBadge v-if="props.withHistoryBadge" />
  </div>
</template>

<script setup>
import HistoryBadge from "@/components/History/HistoryBadge.vue"

const props = defineProps({
  withHistoryBadge: { type: Boolean, default: false },
  to: { type: Object },
  text: { type: String },
})
</script>

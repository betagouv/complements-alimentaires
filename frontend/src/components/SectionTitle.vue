<template>
  <h2 class="fr-h5 flex gap-x-2">
    <v-icon class="mt-[4px]" v-if="icon" :name="icon" />
    <div>{{ title }}</div>
  </h2>
</template>

<script setup>
defineProps({
  title: { type: String },
  icon: { type: String, default: undefined },
})
</script>

<template>
  <div v-if="lowercase" class="fr-text--sm mb-0!">{{ text }}</div>
  <div v-else class="fr-text--sm mb-0! capitalize">{{ text }}</div>
</template>

<script setup>
defineProps({
  text: String,
  lowercase: Boolean,
})
</script>

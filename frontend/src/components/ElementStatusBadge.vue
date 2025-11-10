<template>
  <DsfrBadge v-if="text === 'autorisé'" :label="text" small type="success" />
  <DsfrBadge v-else-if="text === 'non autorisé'" :label="text" small type="error" />
  <DsfrBadge v-else-if="text === 'retiré par l\'administration'" :label="text" small type="error" />
</template>

<script setup>
defineProps({
  text: String,
})
</script>

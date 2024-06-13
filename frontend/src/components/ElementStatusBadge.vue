<template>
  <DsfrBadge v-if="text === 'autorisé'" :label="text" small type="success" />
  <DsfrBadge v-if="text === 'non autorisé'" :label="text" small type="error" />
</template>

<script setup>
defineProps({
  text: String,
})
</script>

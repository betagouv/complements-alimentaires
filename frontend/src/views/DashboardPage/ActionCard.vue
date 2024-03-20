<template>
  <DsfrCard :title="props.action.title" :description="props.action.description" :link="props.action.link" />
</template>

<script setup>
const props = defineProps({ action: { type: Object, required: true } })
</script>

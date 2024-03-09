<template>
  <div v-if="props.value" class="sm:flex border-b last:border-0 py-1 gap-4">
    <div class="sm:flex-[0_0_30%] font-bold sm:text-right">{{ props.label }}</div>
    <div class="sm:flex-auto">{{ props.value }}</div>
  </div>
</template>

<script setup>
const props = defineProps({ label: String, value: String })
</script>

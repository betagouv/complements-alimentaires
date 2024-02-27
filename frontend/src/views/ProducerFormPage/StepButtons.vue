<template>
  <div class="p-3 flex justify-end border rounded-md">
    <DsfrButton
      icon="ri-arrow-left-line"
      class="mr-3"
      label="Précedent"
      @click="$emit('previous')"
      size="small"
      :disabled="disablePrevious"
    />
    <DsfrButton
      icon="ri-arrow-right-line"
      label="Suivant"
      @click="$emit('next')"
      size="small"
      :disabled="disableNext"
    />
  </div>
</template>

<script setup>
defineProps(["disablePrevious", "disableNext"])
</script>

<template>
  <div>
    <DsfrInput :modelValue="dateField" @update:modelValue="updateFn" label-visible type="date" :label="label" />

    <DsfrButton
      icon="ri-close-line"
      v-if="dateField"
      tertiary
      size="small"
      label="Effacer"
      class="mt-2"
      @click="updateFn('')"
    />
  </div>
</template>

<script setup>
defineProps({ dateField: { type: String }, updateFn: { type: Function }, label: { type: String } })
</script>

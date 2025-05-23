<template>
  <DsfrInputGroup>
    <DsfrSelect
      label="Déclarations par page"
      :options="options"
      @update:modelValue="(val) => emit('update:modelValue', val)"
      :modelValue="limit"
      class="text-sm!"
    />
  </DsfrInputGroup>
</template>

<script setup>
const limit = defineModel()
const emit = defineEmits("update:modelValue")
const options = ["10", "20", "30", "40", "50"]
</script>

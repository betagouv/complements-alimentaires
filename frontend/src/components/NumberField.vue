<template>
  <DsfrInput v-model="model" />
</template>

<script setup>
const [model] = defineModel({
  set(value) {
    if (value === "") return null
    const parseableNumber = value.indexOf(",") > -1 ? value.replace(",", ".") : value
    const parsedResult = parseFloat(parseableNumber)
    return isNaN(parsedResult) ? value : parsedResult
  },
})
</script>

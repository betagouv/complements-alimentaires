<template>
  <DsfrInputGroup class="max-w-2xl mt-6 pt-8" v-if="listOfChoices && listOfChoices.indexOf(otherChoiceId) > -1">
    <DsfrInput v-model="model" label-visible :label="label" :required="true" />
  </DsfrInputGroup>
</template>
<script setup>
defineProps({ listOfChoices: { type: Array }, otherChoiceId: { type: Number }, label: { type: String } })
const model = defineModel()
</script>

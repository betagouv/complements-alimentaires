<template>
  <div v-if="listOfChoices && listOfChoices.indexOf(otherChoiceId) > -1" class="mt-6">
    <DsfrInputGroup>
      <DsfrInput v-model="model" label-visible :label="label" :required="true" />
    </DsfrInputGroup>
  </div>
</template>
<script setup>
defineProps({ listOfChoices: { type: Array }, otherChoiceId: { type: Number }, label: { type: String } })
const model = defineModel()
</script>

<template>
  <div class="mt-6">
    <DsfrInputGroup v-if="listOfChoices && listOfChoices.indexOf(otherChoiceId) > -1">
      <DsfrInput v-model="model" label-visible :label="label" :required="true" />
    </DsfrInputGroup>
  </div>
</template>
<script setup>
defineProps({ listOfChoices: { type: Array }, otherChoiceId: { type: Number }, label: { type: String } })
const model = defineModel()
</script>

<template>
  <div v-if="showOtherField" class="mt-6">
    <DsfrInputGroup>
      <DsfrInput v-model="model" label-visible :label="label" :required="true" ref="other-input" />
    </DsfrInputGroup>
  </div>
</template>
<script setup>
import { computed, watch, useTemplateRef } from "vue"

const props = defineProps({ listOfChoices: { type: Array }, otherChoiceId: { type: Number }, label: { type: String } })
const model = defineModel()

const otherInput = useTemplateRef("other-input")

const showOtherField = computed(() => {
  return props.listOfChoices && props.listOfChoices.indexOf(props.otherChoiceId) > -1
})

watch(showOtherField, (newValue, oldValue) => {
  if (newValue !== oldValue && newValue) {
    // sans timeout, otherInput.value est null
    setTimeout(() => {
      if (otherInput.value) otherInput.value.focus()
    }, 10)
  }
})
</script>

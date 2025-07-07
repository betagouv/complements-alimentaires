<template>
  <div class="mb-6">
    <h3>Proposition à viser / signer</h3>
    <VisaValidationSegment :modelValue="declaration" @decision-done="notifySuccess" />
  </div>
</template>

<script setup>
import VisaValidationSegment from "@/components/NewBepiasViews/VisaValidationSegment.vue"

const declaration = defineModel()

const emit = defineEmits(["decision-done"])
const notifySuccess = () => emit("decision-done")
</script>

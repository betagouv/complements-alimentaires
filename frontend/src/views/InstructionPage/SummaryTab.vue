<template>
  <DeclarationSummary :readonly="true" v-model="declaration" />
</template>

<script setup>
import DeclarationSummary from "@/components/DeclarationSummary"

const declaration = defineModel()
</script>
